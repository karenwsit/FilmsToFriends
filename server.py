import os
from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from traitify import TraitifyModel, Traitify, Deck

app = Flask(__name__)


traitify_public = os.environ["TRAITIFY_PUBLIC_KEY"]
traitify_secret = os.environ["TRAITIFY_SECRET"]
assessment_id = os.environ["ASSESSMENT_ID"]


@app.route("/")
def index():

    traitify = Traitify(traitify_secret)
    assessment = traitify.create_assessment("movies")

    return render_template('index.html', traitifyPublic=traitify_public, traitifySecret=traitify_secret, assessmentId=assessment.id)


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/json")
def jsonify_result():
    
    personality_types = traitify.get_personality_types(assessment.id)
    print personality_types
