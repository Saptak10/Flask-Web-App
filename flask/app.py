from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///note.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):    # table name creation
    sno = db.Column(db.Integer, primary_key=True)   #columns creation
    title = db.Column(db.String(200), nullable=False)   #columns creation
    desc = db.Column(db.String(500), nullable=False)   #columns creation
    date_created = db.Column(db.DateTime, default=datetime.utcnow)   #columns creation

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        # print(request.form['title'])
        # print(request.form['desc'])
        title = request.form['title']
        desc = request.form['desc']
        note = Note(title=title, desc=desc)   #made an object containing the first list
        db.session.add(note)   #adding the object to the session
        db.session.commit()   #commiting the addition
    allNote = Note.query.all()
    return render_template('index.html', allNote=allNote)
    # return "<h1>Hello, World!</h1>"

@app.route('/show')
def products():
    allNote = Note.query.all()
    print(allNote)
    return "<h1>This is product page</h1>"

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
        if request.method=='POST':
            title = request.form['title']   #getting the note title from the form
            desc = request.form['desc']   #getting the note desc from the form
            updateNote = Note.query.filter_by(sno=sno).first()   #getting the note of that sno
            updateNote.title = title   #updating the new title
            updateNote.desc = desc   #updating the new desc
            db.session.add(updateNote)   #update the object to the session
            db.session.commit()   #commiting the update
            return redirect("/")

        updateNote = Note.query.filter_by(sno=sno).first()
        return render_template('update.html', note=updateNote)

@app.route('/delete/<int:sno>')
def delete(sno):
    delNote = Note.query.filter_by(sno=sno).first()   #getting the note of that sno
    db.session.delete(delNote)   #delete the object to the session
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port =3000)