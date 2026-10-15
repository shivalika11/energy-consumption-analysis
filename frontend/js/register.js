document.addEventListener("DOMContentLoaded", () => {

    const registerForm = document.getElementById("registerForm");

    registerForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const fullName =
            document.getElementById("fullName").value.trim();

        const email =
            document.getElementById("email").value.trim();

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;


        // Check passwords
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }


        try {

            const response = await fetch(
                "http://127.0.0.1:8000/api/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        full_name: fullName,
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {
                alert("Registration failed.");
                return;
            }


            alert(data.message);

            console.log("Server response:", data);

        } catch (error) {

            console.error("Registration error:", error);

            alert(
                "Could not connect to the backend. " +
                "Make sure FastAPI is running."
            );

        }

    });

});