import sqlite3


class FilmsData:
    def __init__(self, path="netflix.db"):
        self.path = path
        self.name = 'netflix'

        with sqlite3.connect(self.path) as connection:
            self.cursor = connection.cursor()

    def get_film_by_title(self, title):
        """Возвращает самую свежую картину по её названию"""
        self.cursor.execute("""
        SELECT title, country, release_year, listed_in, description FROM {} 
        WHERE title = '{}'
        ORDER BY release_year DESC
        """.format(self.name, title))

        return dict(zip(["title", "country", "release_year", "genre", "description"], self.cursor.fetchone()))

    def get_film_by_years(self, year_one, year_two):
        """Возвращает 100 фильмов в заданном диапазоне лет выпуска year/to/year"""
        self.cursor.execute("""
        SELECT title, release_year FROM {}
        WHERE release_year BETWEEN {} AND {}  
        LIMIT 100 
        """.format(self.name, year_one, year_two))

        return list(dict(zip(["title", "release_year"], result)) for result in self.cursor.fetchall())

    def get_film_by_rating(self, rating: list):
        """Возвращает 100 фильмов по заданному возрастному рейтингу"""
        if len(rating) > 1:
            new_rating = tuple(rating)
            self.cursor.execute("""
            SELECT title, rating, description FROM {}
            WHERE rating IN {}
            LIMIT 100
            """.format(self.name, new_rating))

        elif len(rating) == 1:
            new_rating = str(rating[0])
            self.cursor.execute("""
            SELECT title, rating, description FROM {}
            WHERE rating = '{}'
            LIMIT 100
            """.format(self.name, new_rating))

        return list(dict(zip(["title", "rating", "description"], result)) for result in self.cursor.fetchall())

    def get_film_by_genre(self, genre):
        """Возвращает 10 самых свежих фильмов выбранного жанра"""
        self.cursor.execute("""
        SELECT title, description FROM {}
        WHERE listed_in LIKE '%{}%'
        ORDER BY release_year DESC 
        LIMIT 10
        """.format(self.name, genre))

        return list(dict(zip(["title", "description"], result)) for result in self.cursor.fetchall())

    def get_film_by_two_actors(self, actor_one, actor_two):
        """Возвращает актёров, которые играли с выбранными двумя актёрами более чем в 1й картине"""
        self.cursor.execute("""
        SELECT "cast" FROM {}
        WHERE "cast" LIKE '%{}%' 
        AND "cast" LIKE '%{}%'
        """.format(self.name, actor_one, actor_two))

        all_actors = []
        for i in self.cursor.fetchall():
            all_actors += i[0].split(", ")

        result = []
        for item in set(all_actors):
            if all_actors.count(item) > 1 and item not in [actor_one, actor_two]:
                result.append(item)

        return result

    def get_film_by_type_year_genre(self, types, year, genre):
        """Возвращает картины, по выбранному типу (Movie, TV Show), году выпуска и жанру"""
        self.cursor.execute("""
        SELECT title, description FROM {}
        WHERE "type" = '{}'
        AND release_year = {}
        AND listed_in LIKE '%{}%'
        """.format(self.name, types, year, genre))

        return list(dict(zip(["title", "description"], result)) for result in self.cursor.fetchall())
