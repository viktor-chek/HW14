from flask import Flask, jsonify, render_template
from DataFilms import FilmsData
import re

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route("/movie/<title>")
def page_by_title(title):
    return jsonify(FilmsData().get_film_by_title(title))


@app.route("/movie/<int:year_one>/to/<int:year_two>")
def page_by_years(year_one, year_two):
    return jsonify(FilmsData().get_film_by_years(year_one, year_two))


@app.route("/rating/children")
def page_by_rating_by_children():
    return jsonify(FilmsData().get_film_by_rating(["G"]))


@app.route("/rating/family")
def page_by_rating_by_family():
    return jsonify(FilmsData().get_film_by_rating(["G", "PG", "PG-13"]))


@app.route("/rating/adult")
def page_by_rating_by_adult():
    return jsonify(FilmsData().get_film_by_rating(["R", "NC-17"]))


@app.route("/genre/<genre>")
def page_by_genre(genre):
    return jsonify(FilmsData().get_film_by_genre(genre))


@app.route("/actors/<one_actor>/and/<two_actor>")
def page_by_actors(one_actor, two_actor):
    new_one_actor = re.sub(r"([A-Z])", r" \1", one_actor).split()
    new_s_one = " ".join(new_one_actor)
    new_two_actor = re.sub(r"([A-Z])", r" \1", two_actor).split()
    new_s_two = " ".join(new_two_actor)
    result = (FilmsData().get_film_by_two_actors(new_s_one, new_s_two))
    return render_template("actors.html", all=result)


@app.route("/film/<types>/<int:year>/<genre>")
def page_by_title_year_genre(types, year, genre):
    if types == "TVShow":
        types = "TV Show"
    return jsonify(FilmsData().get_film_by_type_year_genre(types, year, genre))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True)
