import os
from flask import flash, Flask, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from traitify import TraitifyModel, Traitify, Deck

app = Flask(__name__)


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
        personality = request.form["personality"]

        new_user = User(fname=fname, lname=lname, email=email, password=password, zipcode=zipcode, personality=personality)

        db.session.add(new_user)
        db.session.commit()

        flash("User created!")

    else:
        flash("User already registered!")


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

    session["user_id"] = user.user_id

    flash("Hello, %s!" % user.fname)

    print session["user_id"], "********************************"

    return render_template("session-login.html", session=session)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]

    flash("Logged Out.")
    return redirect("/")

##########################################################################




if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/json")
# def jsonify_result():

#     personality_types = traitify.get_personality_types(assessment.id)
#     print personality_types
