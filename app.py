from flask import Flask, render_template,  request
import pandas as pd

app = Flask(__name__)

movie_data = 'movies.xlsx'

def get_movies():
    return pd.read_excel(movie_data).to_dict(orient='records')

def get_movie(name):
    for movie in get_movies():
        if movie['name'] == name:
            return movie
    

@app.route("/")
def show_all_movies():
    movies = get_movies()
    return render_template('all_movies.html', movies=movies)

@app.route('/<string:name>')
def display_movie(name):
    movie = get_movie(name)
    return render_template('movie.html', movie=movie)

@app.route('/admin')
def add_data():
    global movies_df

    name = request.args.get('name')
    director = request.args.get('director')
    date = request.args.get('date')
    genre = request.args.get('genre')
    image = request.args.get('image')

    if not name or not director or not date or not genre or not image:
        return render_template('admin.html', inp=False)

    new_movie = {'name':[name], 'director':[director], 'date':[date], 'genre':[genre], 'image':[image]}
    new_movie_df = pd.DataFrame(new_movie)
    old_movie_df = pd.read_excel(movie_data)
    movies_df = pd.concat([old_movie_df, new_movie_df], ignore_index=True)
    movies_df.to_excel(movie_data, index=False)

    return render_template('admin.html', inp=False)
    