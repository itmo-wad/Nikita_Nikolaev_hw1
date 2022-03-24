from flask import Flask, render_template, send_from_directory, redirect, flash, request
from flask.wrappers import Request
from flask_pymongo import PyMongo
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/general"
mongo = PyMongo(app)

@app.route('/')
@app.route('/home/')
def home():
    online_users = mongo.db.users.find({});
    return render_template("list.html", users = online_users)


@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('form.html')
    else:
        login = request.form.get("login")
        password = request.form.get("password")
        if mongo.db.users.count_documents({'login':login}) != 0:
            flash('login exists!')
            return redirect('/signup')
        else:
            mongo.db.users.insert_one({
                'login': login,
                'password': password
            })
            flash('Signed up!')
            return redirect('/authentification')

@app.route('/authentification', methods = ["GET", "POST"])
def auth():
    if request.method == 'GET':
        return render_template('authentification.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        user = mongo.db.users.find_one({'login': login})


        if user and password:
            return render_template('/open.html')
        else:
            flash('Login or password is not correct!')
            return render_template('authentification.html')



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)