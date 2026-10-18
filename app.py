
import os

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    abort
)

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


# Project information
projects = {
    "camouflage-detection": {
        "title": "Camouflaged Military Object Detection",
        "description": (
            "A deep learning-based computer vision system using YOLOv8 "
            "to detect camouflaged military objects against complex "
            "backgrounds. The project includes a Flask web application "
            "for image uploads and live webcam detection."
        ),
        "technologies": [
            "Python",
            "YOLOv8",
            "PyTorch",
            "Flask",
            "OpenCV",
            "HTML",
            "CSS",
            "JavaScript"
        ],
        "objective": (
            "Explore deep learning-based object detection for "
            "identifying camouflaged objects in complex scenes."
        ),
        "results": (
            "Provides a web interface for image-based and webcam-based "
            "detection."
        ),
        "github": (
            "https://github.com/Yogesh-Rebari/"
            "Camouflaged-Object-Detection-using-Deep-Learning"
        )
    },

    "afdx-simulator": {
        "title": "AFDX Simulator",
        "description": (
            "An ongoing C++ project focused on simulating "
            "AFDX network communication and virtual links."
        ),
        "technologies": [
            "C++",
            "UDP",
            "Networking",
            "CMake"
        ],
        "objective": (
            "Explore AFDX communication concepts, virtual-link "
            "management, and frame encoding and decoding."
        ),
        "results": (
            "Currently under development."
        )
    },

    "house-price-prediction": {
        "title": "Bengaluru House Price Prediction",
        "description": (
            "A machine learning project that predicts house prices "
            "using property-related features. The project includes "
            "exploratory data analysis, model training, and a Flask "
            "web application for generating price predictions."
        ),
        "technologies": [
            "Python",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Flask",
            "Flask-WTF",
            "Joblib"
        ],
        "objective": (
            "Develop a machine learning solution to estimate "
            "Bengaluru house prices from property features and "
            "make predictions accessible through a web interface."
        ),
        "results": (
            "Developed an end-to-end prediction workflow covering "
            "data analysis, model training, model serialization, "
            "and web-based price prediction. The reported model "
            "achieved an R² score of 0.85."
        ),
        "github": (
            "https://github.com/Raghu131204/Houseprice_project"
        )
    }
}


# Home page
@app.route("/")
def home():
    featured_projects = [
        ("camouflage-detection", projects["camouflage-detection"]),
        ("afdx-simulator", projects["afdx-simulator"]),
        ("house-price-prediction", projects["house-price-prediction"])
    ]

    return render_template(
        "index.html",
        featured_projects=featured_projects
    )


# Projects page
@app.route("/projects")
def project_list():
    return render_template(
        "projects.html",
        projects=projects
    )


# Individual project page
@app.route("/projects/<slug>")
def project_detail(slug):
    project = projects.get(slug)

    if project is None:
        abort(404)

    return render_template(
        "project_detail.html",
        project=project
    )


# About page
@app.route("/about")
def about():
    return render_template("about.html")


# Contact page
# Web3Forms handles contact form submissions directly.
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


# Run the application locally
if __name__ == "__main__":
    app.run(debug=True)
