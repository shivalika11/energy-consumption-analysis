import os
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
    session,
    redirect,
)
from werkzeug.security import generate_password_hash, check_password_hash


# ==================================================
# 1. PROJECT PATHS
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ==================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ==================================================
load_dotenv(BACKEND_DIR / ".env")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
USERS_TABLE_NAME = os.getenv("USERS_TABLE", "EnergyUsers")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing. Please configure it in backend/.env"
    )


# ==================================================
# 3. FLASK CONFIGURATION
# ==================================================
app = Flask(__name__)

app.config.update(
    SECRET_KEY=SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",

    # Local development only.
    # Enable secure cookies when deployed over HTTPS.
    SESSION_COOKIE_SECURE=False,

    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
)


# ==================================================
# 4. AWS DYNAMODB CONNECTION
# ==================================================
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
)

users_table = dynamodb.Table(USERS_TABLE_NAME)


# ==================================================
# 5. HOME PAGE
# ==================================================
@app.route("/")
def home():
    return send_from_directory(
        FRONTEND_DIR,
        "index.html",
    )


# ==================================================
# 6. HEALTH CHECK
# ==================================================
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Flask backend is working correctly",
    }), 200


# ==================================================
# 7. SERVE CSS FILES
# ==================================================
@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(
        FRONTEND_DIR / "css",
        filename,
    )


# ==================================================
# 8. SERVE JAVASCRIPT FILES
# ==================================================
@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(
        FRONTEND_DIR / "js",
        filename,
    )


# ==================================================
# 9. SERVE FRONTEND PAGES
# ==================================================
@app.route("/pages/<path:filename>")
def serve_pages(filename):

    protected_pages = {
        "dashboard.html",
        "profile.html",
        "upload.html",
    }

    page_name = Path(filename).name

    # Require login before serving protected pages.
    if page_name in protected_pages and "user_email" not in session:
        return redirect("/")

    return send_from_directory(
        FRONTEND_DIR / "pages",
        filename,
    )


# ==================================================
# 10. USER REGISTRATION
# ==================================================
@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid registration data.",
        }), 400

    full_name = str(
        data.get("full_name") or ""
    ).strip()

    email = str(
        data.get("email") or ""
    ).strip().lower()

    password = data.get("password")

    if not isinstance(password, str):
        password = ""

    # Validate name.
    if not full_name:
        return jsonify({
            "success": False,
            "message": "Full name is required.",
        }), 400

    # Validate email.
    if not email or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email,
    ):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address.",
        }), 400

    # Validate password.
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters.",
        }), 400

    # Store only a password hash, never the plain-text password.
    password_hash = generate_password_hash(password)

    user_item = {
        "email": email,
        "full_name": full_name,
        "password_hash": password_hash,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        users_table.put_item(
            Item=user_item,

            # Prevent overwriting an existing account.
            ConditionExpression="attribute_not_exists(email)",
        )

        return jsonify({
            "success": True,
            "message": "Registration successful.",
        }), 201

    except ClientError as error:

        error_code = error.response.get(
            "Error", {}
        ).get("Code")

        if error_code == "ConditionalCheckFailedException":
            return jsonify({
                "success": False,
                "message": "An account with this email already exists.",
            }), 409

        app.logger.exception("DynamoDB registration error")

        return jsonify({
            "success": False,
            "message": "Could not register your account. Please try again.",
        }), 500

    except Exception:
        app.logger.exception("Unexpected registration error")

        return jsonify({
            "success": False,
            "message": "An unexpected error occurred.",
        }), 500


# ==================================================
# 11. USER LOGIN
# ==================================================
@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid login data.",
        }), 400

    email = str(
        data.get("email") or ""
    ).strip().lower()

    password = data.get("password")

    if not isinstance(password, str):
        password = ""

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required.",
        }), 400

    try:
        # Find the registered user in DynamoDB.
        response = users_table.get_item(
            Key={"email": email},
            ConsistentRead=True,
        )

        user = response.get("Item")

        # Verify the supplied password against its stored hash.
        if not user or not check_password_hash(
            user.get("password_hash", ""),
            password,
        ):
            return jsonify({
                "success": False,
                "message": "Invalid email or password.",
            }), 401

        # Start a fresh authenticated session.
        session.clear()

        session["user_email"] = email
        session["full_name"] = user.get("full_name", "")
        session.permanent = True

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "redirect_url": "/pages/dashboard.html",
        }), 200

    except Exception:
        app.logger.exception("Login error")

        return jsonify({
            "success": False,
            "message": "A server error occurred during login.",
        }), 500


# ==================================================
# 12. CURRENT USER
# ==================================================
@app.route("/api/me", methods=["GET"])
def current_user():

    if "user_email" not in session:
        return jsonify({
            "authenticated": False,
        }), 401

    return jsonify({
        "authenticated": True,
        "email": session["user_email"],
        "full_name": session.get("full_name", ""),
    }), 200


# ==================================================
# 13. BUSINESS PROFILE
# ==================================================
@app.route("/api/profile", methods=["GET", "POST"])
def business_profile():

    if "user_email" not in session:
        return jsonify({
            "message": "Please log in first.",
        }), 401

    email = session["user_email"]

    # ----------------------------------------------
    # GET: Load the saved business profile.
    # ----------------------------------------------
    if request.method == "GET":

        try:
            response = users_table.get_item(
                Key={"email": email},
                ConsistentRead=True,
            )

            user = response.get("Item", {})

            return jsonify({
                "profile": {
                    "businessName": user.get(
                        "business_name", ""
                    ),
                    "businessType": user.get(
                        "business_type", ""
                    ),
                    "openingTime": user.get(
                        "opening_time", ""
                    ),
                    "closingTime": user.get(
                        "closing_time", ""
                    ),
                    "lowOccupancy": user.get(
                        "low_occupancy", ""
                    ),
                    "equipment": user.get(
                        "equipment", ""
                    ),
                }
            }), 200

        except Exception:
            app.logger.exception(
                "Could not load business profile"
            )

            return jsonify({
                "message": "Could not load the profile.",
            }), 500

    # ----------------------------------------------
    # POST: Save the business profile.
    # ----------------------------------------------
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "message": "Invalid profile data.",
        }), 400

    # These keys must match the existing profile.js.
    business_name = str(
        data.get("businessName") or ""
    ).strip()

    business_type = str(
        data.get("businessType") or ""
    ).strip()

    opening_time = str(
        data.get("openingTime") or ""
    ).strip()

    closing_time = str(
        data.get("closingTime") or ""
    ).strip()

    low_occupancy = str(
        data.get("lowOccupancy") or ""
    ).strip()

    equipment = str(
        data.get("equipment") or ""
    ).strip()

    # Validate required fields.
    if not business_name or not business_type:
        return jsonify({
            "message": "Business name and type are required.",
        }), 400

    if len(business_name) > 150 or len(equipment) > 3000:
        return jsonify({
            "message": "Business name or equipment information is too long.",
        }), 400

    try:
        # Save the profile to the existing user's DynamoDB record.
        users_table.update_item(
            Key={"email": email},

            UpdateExpression="""
                SET business_name = :bn,
                    business_type = :bt,
                    opening_time = :ot,
                    closing_time = :ct,
                    low_occupancy = :lo,
                    equipment = :eq,
                    profile_updated_at = :updated
            """,

            ExpressionAttributeValues={
                ":bn": business_name,
                ":bt": business_type,
                ":ot": opening_time,
                ":ct": closing_time,
                ":lo": low_occupancy,
                ":eq": equipment,
                ":updated": datetime.now(
                    timezone.utc
                ).isoformat(),
            },

            # Only update an existing registered user's record.
            ConditionExpression="attribute_exists(email)",
        )

        return jsonify({
            "success": True,
            "message": "Business profile saved successfully.",
        }), 200

    except Exception:
        app.logger.exception(
            "Could not save business profile"
        )

        return jsonify({
            "message": "Could not save the profile. Please try again.",
        }), 500


# ==================================================
# 14. USER LOGOUT
# ==================================================
@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect("/")


# ==================================================
# 15. RUN FLASK APPLICATION
# ==================================================
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )