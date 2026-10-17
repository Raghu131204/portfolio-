
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort
)

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

# Project information
projects = {
    "camouflage-detection": {
        "title": "Camouflaged Object Segmentation",
        "description": (
            "A computer vision project for identifying camouflaged "
            "objects in complex backgrounds."
        ),
        "technologies": [
            "Python", "PyTorch", "Vision Transformer", "SegNet"
        ],
        "objective": (
            "Improve object segmentation when foreground objects "
            "blend into their surroundings."
        ),
        "results": (
            "Evaluated using segmentation metrics such as IoU "
            "and binary cross-entropy."
        )
    },

    "afdx-simulator": {
        "title": "AFDX Simulator",
        "description": (
            "A network simulation project exploring virtual links "
            "and frame transmission."
        ),
        "technologies": ["C++", "UDP", "Networking", "CMake"],
        "objective": (
            "Simulate virtual-link-based communication and frame encoding."
        ),
        "results": (
            "Implemented virtual-link management and basic "
            "frame encode/decode testing."
        )
    },

    "house-price-prediction": {
        "title": "Bengaluru House Price Prediction",
        "description": (
            "A machine learning model for estimating residential "
            "property prices."
        ),
        "technologies": [
            "Python", "Pandas", "Scikit-learn", "Gradient Boosting"
        ],
        "objective": "Predict house prices using property-related features.",
        "results": "The reported model achieved an R² score of 0.85."
    }
}


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Projects page
@app.route("/projects")
def project_list():
    return render_template("projects.html", projects=projects)


# Individual project page
@app.route("/projects/<slug>")
def project_detail(slug):
    project = projects.get(slug)

    if project is None:
        abort(404)

    return render_template("project_detail.html", project=project)


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        # Validate required fields
        if not all([name, email, subject, message]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))

        # Validate field lengths
        if len(name) > 100 or len(email) > 254:
            flash("Name or email is too long.", "error")
            return redirect(url_for("contact"))

        if len(subject) > 150 or len(message) > 5000:
            flash("Subject or message is too long.", "error")
            return redirect(url_for("contact"))

        # Basic email validation
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("contact"))

        # Read email settings from .env
        smtp_username = os.getenv("SMTP_USERNAME")
        smtp_password = os.getenv("SMTP_APP_PASSWORD")
        receiver_email = os.getenv("CONTACT_RECEIVER")

        if not all([smtp_username, smtp_password, receiver_email]):
            app.logger.error("Email configuration is incomplete.")
            flash(
                "Email service is not configured. Please try again later.",
                "error"
            )
            return redirect(url_for("contact"))

        # Construct the email
        email_message = EmailMessage()
        email_message["Subject"] = f"Portfolio Contact: {subject}"
        email_message["From"] = smtp_username
        email_message["To"] = receiver_email
        email_message["Reply-To"] = email

        email_message.set_content(
            f"You received a new message from your portfolio website.\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}\n"
        )

        # Connect, authenticate, and send before closing the connection
        try:
            print("Connecting to Gmail...")

            with smtplib.SMTP(
                "smtp.gmail.com",
                587,
                timeout=30
            ) as server:

                server.ehlo()
                server.starttls()
                server.ehlo()

                print("Authenticating with Gmail...")

                server.login(
                    smtp_username,
                    smtp_password.replace(" ", "")
                )

                print("Login successful. Sending email...")

                server.send_message(email_message)

                print("Email sent successfully.")

            flash(
                "Your message has been sent successfully!",
                "success"
            )

        except (smtplib.SMTPException, OSError):
            app.logger.exception("Unable to send contact email")
            flash(
                "Sorry, your message could not be sent. Please try again later.",
                "error"
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
