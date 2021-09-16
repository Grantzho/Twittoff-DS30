from flask import Flask
from flask import request
from flask import render_template
from .models import db, User, Tweet
import os


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    @app.route("/", methods=["GET", "POST"])
    def home():
        name = request.form.get("name")
        
        if name:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()

        users = User.query.all()
        return render_template("home.html", users=users)

    @app.route("/", methods=["GET", "POST"])
    def home2():
        text = request.form.get("text")
        
        if text:
            tweet = Tweet(text=text)
            db.session.add(tweet)
            db.session.commit()

        texts = Tweet.query.all()
        return render_template("home.html", texts=texts)

    @app.route('/about')
    def about():
        return 'This is the best app ever'

    @app.route('/iris')
    def iris():  
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression  
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                            multi_class='multinomial').fit(X, y)

        return str(clf.predict(X[:2, :]))

    return app
    

