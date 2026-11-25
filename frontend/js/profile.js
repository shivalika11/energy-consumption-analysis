document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("profileForm");

    if (!form) return;

    const message = document.createElement("div");

    message.className = "alert d-none";
    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");

    form.prepend(message);

    const fieldIds = [
        "businessName",
        "businessType",
        "openingTime",
        "closingTime",
        "lowOccupancy",
        "equipment"
    ];

    function showMessage(text, type) {
        message.textContent = text;
        message.className = `alert alert-${type}`;
    }

    // Load existing profile
    async function loadProfile() {
        try {
            const response = await fetch("/api/profile");

            if (response.status === 401) {
                window.location.href = "/";
                return;
            }

            const data = await response.json();

            if (!response.ok) {
                showMessage(
                    data.message || "Could not load profile.",
                    "danger"
                );
                return;
            }

            const profile = data.profile || {};

            fieldIds.forEach((id) => {
                const field = document.getElementById(id);

                if (field) {
                    field.value = profile[id] || "";
                }
            });

        } catch (error) {
            console.error("Profile loading error:", error);

            showMessage(
                "Could not connect to Flask.",
                "danger"
            );
        }
    }

    // Save profile
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const button = form.querySelector(
            'button[type="submit"]'
        );

        button.disabled = true;
        button.textContent = "Saving...";

        const profile = {};

        fieldIds.forEach((id) => {
            profile[id] = document.getElementById(id).value.trim();
        });

        try {
            const response = await fetch("/api/profile", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify(profile)
            });

            const data = await response.json();

            if (response.status === 401) {
                window.location.href = "/";
                return;
            }

            if (!response.ok) {
                showMessage(
                    data.message || "Could not save profile.",
                    "danger"
                );
                return;
            }

            showMessage(
                data.message || "Profile saved successfully!",
                "success"
            );

        } catch (error) {
            console.error("Profile saving error:", error);

            showMessage(
                "Could not connect to Flask.",
                "danger"
            );

        } finally {
            button.disabled = false;

            button.innerHTML =
                '<i class="bi bi-check-circle me-2"></i> Save Business Profile';
        }
    });

    loadProfile();
});