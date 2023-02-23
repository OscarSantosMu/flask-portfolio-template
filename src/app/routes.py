import os
import statistics

import folium
from flask import render_template, url_for, request
from playhouse.shortcuts import model_to_dict

from app import app
from .models.experience import Experience
from .models.education import Education
from .models.hobbies import Hobbies
from .models.about import About
from .models.locations import Locations
from .models.timelinepost import TimelinePost
from .static.sample_data.data import data


@app.route("/")
def index():
    return render_template(
        "layout.html",
        title="MLH Fellow",
        photoUrl=data["John Doe"]["photourl"],
        url=os.getenv("URL"),
    )


@app.route("/<name>")
def about(name):
    aboutme = []
    for about in data[name]["about"]:
        aboutme.append(
            About(
                about["email"],
                about["twitter"],
                about["linkedin"],
                about["description"],
            )
        )
    return render_template(
        "main.html",
        title="MLH Fellow",
        name=name,
        photoUrl=data[name]["photourl"],
        url=os.getenv("URL"),
        type="About",
        elements=aboutme,
    )


@app.route("/experience/<name>")
def experience(name):
    experiences = []
    for experience in data[name]["experience"]:
        experiences.append(
            Experience(
                experience["company"],
                experience["position"],
                experience["duration"],
                experience["description"],
            )
        )
    return render_template(
        "main.html",
        title="MLH Fellow",
        name=name,
        photoUrl=data[name]["photourl"],
        url=os.getenv("URL"),
        type="Experience",
        elements=experiences,
    )


@app.route("/education/<name>")
def education(name):
    educations = []
    for education in data[name]["education"]:
        educations.append(
            Education(
                education["institution"],
                education["degree"],
                education["tenure"],
                education["description"],
            )
        )
    return render_template(
        "main.html",
        title="MLH Fellow",
        name=name,
        photoUrl=data[name]["photourl"],
        url=os.getenv("URL"),
        type="Education",
        elements=educations,
    )


@app.route("/hobbies/<name>")
def hobbie(name):
    hobbies = []
    for hobbie in data[name]["hobbies"]:
        hobbies.append(
            Hobbies(
                hobbie["name"],
                hobbie["description"],
                hobbie["url"],
                hobbie["alt"],
                hobbie["textcolor"],
            )
        )
    return render_template(
        "main.html",
        title="MLH Fellow",
        name=name,
        photoUrl=data[name]["photourl"],
        url=os.getenv("URL"),
        type="Hobbies",
        elements=hobbies,
    )


@app.route("/map/<name>")
def tourism(name):
    locations = []
    for location in data[name]["locations"]:
        locations.append(Locations(location["cityname"], location["coordinates"]))
    create_map(locations)
    return render_template(
        "main.html",
        title="MLH Fellow",
        name=name,
        photoUrl=data[name]["photourl"],
        url=os.getenv("URL"),
        type="Map",
        elements=[],
    )


@app.route("/map")
def folium_map():
    return render_template("map.html")


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form["name"]
    email = request.form["email"]
    content = request.form["content"]
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/api/timeline_post/<id>", methods=["DELETE"])
def delete_time_line_post(id):
    timeline_post = TimelinePost.get(TimelinePost.id == id)
    record = model_to_dict(timeline_post)
    number_of_records = timeline_post.delete_instance()
    record["status"] = "Deleted"
    return record


def create_map(locations):

    # Convert the list of Locations to a list of coordinates
    coordinates_str = [location.coordinates.split(",") for location in locations]

    # Convert the strings to floats
    coordinates = [(float(lat), float(lon)) for lat, lon in coordinates_str]

    # Calculate the mean of the coordinates
    mean_lat = statistics.mean(lat for lat, lon in coordinates)
    mean_lon = statistics.mean(lon for lat, lon in coordinates)

    start_coords = (mean_lat, mean_lon)
    m = folium.Map(location=start_coords, zoom_start=4)
    tooltip = "Click here!"
    for i, location in enumerate(locations):

        folium.Marker(
            coordinates_str[i], popup=location.cityname, tooltip=tooltip
        ).add_to(m)

    m.save("app/templates/map.html")
