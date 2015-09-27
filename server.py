import os

from flask import flash, Flask, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from traitify import Deck, Traitify, TraitifyModel 
from model import connect_to_db, db, Movie, User

app = Flask(__name__)

app.secret_key = "ABC"

traitify_public = os.environ["TRAITIFY_PUBLIC_KEY"]
traitify_secret = os.environ["TRAITIFY_SECRET"]
assessment_id = os.environ["ASSESSMENT_ID"]

###################################
# General registration and login #
###################################

@app.route("/")
def index():

    traitify = Traitify(traitify_secret)
    assessment = traitify.create_assessment("movies")

    session['assessment'] = assessment.id

    return render_template('index.html', traitifyPublic=traitify_public, traitifySecret=traitify_secret, assessmentId=assessment.id)

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template('registration-form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    user_email = request.form['email']
    user = User.query.filter(User.email == user_email).first()

    if user is None:
        # Get form variables
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]
        zipcode = request.form["zipcode"]

        new_user = User(fname=fname, lname=lname, email=email, password=password, zipcode=zipcode, personality=None)

        db.session.add(new_user)
        db.session.commit()

        return render_template("registration-confirm.html", error_message = "New user %s added." % email)

    else:
        return render_template("error-dialog.html", error_message = "This email is already Registered.\n Please login or register with a different email.")



@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login-form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user. Please register an account.")
        return redirect("/register")

    # if user.password != password:
    if not user.check_password(password):
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id #store user id in session


    print "session is: ", session, "********************************"

    return render_template("session-login.html", session=session)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]

    flash("Logged Out.")
    return redirect("/")


@app.route("/movies")
def commit_personality_load_movies():

    assessment_id = session.get('assessment',"")
    user_id = session.get('user_id',"")
    traitify = Traitify(traitify_secret)

    # Get an assessment's results (personality types)
    personality_types = traitify.get_personality_types(assessment_id)

    # Get an assessment's results (personality type traits)
    personality_type = personality_types["personality_types"][0].personality_type
    print "personality type:", personality_type.attributes['name'], "$$$$$$$$$"


    this_user = User.query.filter(User.user_id == user_id).first()

    if this_user:
        this_user.personality = personality_type.attributes['name']
        db.session.commit()


    # movies = session.get("movies",[])
    movies = db.session.query(Movie.movie_id, Movie.title, Movie.genre, Movie.length, Movie.image_link)

    if this_user.personality == "Beliver":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Action%'),
                                    Movie.genre.like('%Adventure%'),
                                    Movie.genre.like('%Fantasy%'),
                                    Movie.genre.like('%Sci-Fi%')
                                    )).all() 

    elif this_user.personality == "Dramatic":
        by_genre = movies.filter(db.or_(Movie.genre.like('Biography%'),
                                    Movie.genre.like('%Crime%'),
                                    Movie.genre.like('%Drama%'),
                                    Movie.genre.like('%History%'),
                                    Movie.genre.like('%Mystery%'),
                                    Movie.genre.like('%Western%')
                                    )).all()

    elif this_user.personality == "Indie":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Documentary%'),
                                    Movie.genre.like('%History%'),
                                    Movie.genre.like('%Mystery%')
                                    )).all()

    elif this_user.personality == "Laughaholic":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Comedy%'),
                                    Movie.genre.like('%Family%')
                                    )).all()

    elif this_user.personality == "Romantic":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Romance%'),
                                    Movie.genre.like('%Comedy%')
                                    )).all()

    elif this_user.personality == "Nail Biter":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Horror%'),
                                    Movie.genre.like('%Crime%'),
                                    Movie.genre.like('%Mystery%'),
                                    Movie.genre.like('%Thriller%')
                                    )).all()

    elif this_user.personality == "Stunt Double":
        by_genre = movies.filter(db.or_(Movie.genre.like('%Action%'),
                                    Movie.genre.like('%War%'),
                                    Movie.genre.like('%Adventure%'),
                                    Movie.genre.like('%Western%')
                                    )).all()

    print "by_genre is", by_genre
    return render_template("results.html", session=session, movies=by_genre)

###############################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

else:
    connect_to_db(app)
