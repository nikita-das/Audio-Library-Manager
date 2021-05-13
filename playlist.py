import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:abcd@localhost/myDB'

db=SQLAlchemy(app)

class Playlist(db.Model):
    s_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)
    album = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    def __init__(self, s_no, name, artist, album, genre):
 
        self.s_no = s_no
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre

@app.route('/')
def Index():
    playlist = Playlist.query.all()
    return render_template("index.html", playlist = playlist)

@app.route("/insert", methods=["POST"])
def insert():
    if request.method == 'POST':
        s_no = request.form['s_no']
        name = request.form['name']
        artist = request.form['artist']
        album = request.form['album']
        genre = request.form['genre']

        my_song = Playlist(s_no, name, artist, album, genre)
        db.session.add(my_song)
        db.session.commit()
        flash("Song added successfully!")
        return redirect(url_for('Index'))

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == 'POST':
        my_song = Playlist.query.get(request.form.get('s_no'))
        
        my_song.name = request.form['name']
        my_song.artist = request.form['artist']
        my_song.album = request.form['album']
        my_song.genre = request.form['genre']
        db.session.commit()
        flash("Playlist updated successfully!")
        return redirect(url_for('Index'))

@app.route("/delete/<s_no>", methods=["GET", "POST"])
def delete(s_no):
    playlist = Playlist.query.get(s_no)
    db.session.delete(playlist)
    db.session.commit()
    flash("Song deleted successfully!")
    return redirect(url_for('Index'))
  
if __name__ == "__main__":
    app.run(debug=True)