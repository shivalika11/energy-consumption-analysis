// --------------------------------------------------
// Login form
// --------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");

    // Other pages, such as the dashboard, don't have this form.
    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const email = document
            .getElementById("email")
            .value
            .trim()
            .toLowerCase();

        const password = document
            .getElementById("password")
            .value;

        try {

            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Login failed.");
                return;
            }

            window.location.href =
                data.redirect_url || "/pages/dashboard.html";

        } catch (error) {

            console.error("Login error:", error);

            alert(
                "Could not connect to Flask. " +
                "Please make sure the server is running."
            );
        }

    });

});