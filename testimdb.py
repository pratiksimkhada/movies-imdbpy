from flask import Flask, render_template, url_for, redirect, request
from imdb import IMDb



app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
	if request.method=="POST":
		query = request.form.get('search')
		return redirect(url_for("search_result", query=query))

	return render_template('imdb.html')

@app.route("/result", methods=["GET","POST"])
def search_result():
	query = request.args.get('query')    

	ia = IMDb()
	movies = ia.search_movie(query)
	
	film_list=[]	

	for i in movies:
		id = i.getID()
		film = ia.get_movie(id)

		film_list.append(film)

	return render_template('imdb_result.html', film_list=film_list)

@app.route("/single_movie/<movie_id>")
def single_movie(movie_id):
	movie_id = movie_id

	ia = IMDb()
	movie = ia.get_movie(movie_id)

	return render_template('single_movie.html', movie=movie)






