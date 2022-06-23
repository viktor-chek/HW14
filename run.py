from flask import Flask, jsonify
from DataFilms import FilmsData

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


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


#                Для тестов функций без вьюшки
# print(FilmsData().get_film_by_two_actors("Jack Black", "Dustin Hoffman"))
# print(FilmsData().get_film_by_type_year_genre("Movie", 1971, "Dramas"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000, debug=True)
