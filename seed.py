import json
import urllib
from model import User, Movie, connect_to_db, db
from server import app


def load_movies():

    my_results = json.load(urllib.urlopen("https://www.kimonolabs.com/api/6vk1k5hu?apikey=f2jrKtObW1sW7y1aJxhCHwTqiTCMzSYR"))

    collection1_list = my_results['results']['collection1']

    for i in collection1_list:
        title = i['title']['text']
        genre = i['genre']
        length = i['length']
        image_link = i['image']['src']

        new_movie = Movie(
            title=title,
            genre=genre,
            length=length,
            image_link=image_link)

        db.session.add(new_movie)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_movies()
