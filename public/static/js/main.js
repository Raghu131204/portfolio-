
document.addEventListener("DOMContentLoaded", function () {
    console.log("Portfolio website loaded successfully.");

    const form = document.getElementById("contact-form");

    if (!form) {
        return;
    }

    const status = document.getElementById("form-status");
    const submitButton = document.getElementById("submit-button");

    form.addEventListener("submit", async function (event) {
        // Stop the browser from navigating to Web3Forms.
        event.preventDefault();

        console.log("Contact form submission intercepted.");

        if (submitButton.disabled) {
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Sending...";

        status.hidden = true;
        status.textContent = "";
        status.className = "flash-message";

        try {
            const response = await fetch(
                "https://api.web3forms.com/submit",
                {
                    method: "POST",
                    body: new FormData(form)
                }
            );

            const result = await response.json();

            if (response.ok && result.success) {
                status.textContent =
                    "Thank you for contacting me! Your message has been sent successfully.";

                status.classList.add("success");
                form.reset();
            } else {
                status.textContent =
                    result.message ||
                    "Sorry, your message could not be sent. Please try again.";

                status.classList.add("error");
            }
        } catch (error) {
            console.error("Contact form error:", error);

            status.textContent =
                "Unable to send your message. Please try again.";

            status.classList.add("error");
        } finally {
            status.hidden = false;
            submitButton.disabled = false;
            submitButton.textContent = "Send Message →";
        }
    });
});
