document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    if (!registerForm) {
        console.error("Registration form not found!");
        return;
    }

    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Get values using the IDs from register.html
        const fullName = document.getElementById("fullName").value.trim();
        const email = document.getElementById("registerEmail").value.trim();
        const password = document.getElementById("registerPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        // Check whether passwords match
        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            // Send registration data to Flask
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_name: fullName,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Registration failed.");
                return;
            }

            alert(data.message);
            console.log("Server response:", data);

            registerForm.reset();

        } catch (error) {
            console.error("Registration error:", error);

            alert(
                "Could not connect to Flask. " +
                "Make sure the Flask server is running."
            );
        }
    });
});