from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, String


app = Flask(__name__)
app.secret_key = "SKey"

#SqlAlchemy Database Configuration With Mysql database, 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/appasst' # database is called appasst
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for the database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    login = db.Column(db.String(100))


    def __init__(self, name="a", email="b", login="c"):
        self.name = name
        self.email = email
        self.login = login



# rendering all users with their data 
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", students = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        login = request.form['login']


        my_data = Data(name, email, login)
        db.session.add(my_data)
        db.session.commit()

        flash("Added the frosh student")

        return redirect(url_for('Index'))


#Student profile update route
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.login = request.form['login']

        db.session.commit()
        flash("Updated the frosh' profile")

        return redirect(url_for('Index'))




#To delete a student's profile
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted the frosh's profile")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)