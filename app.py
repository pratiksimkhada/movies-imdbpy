from flask import Flask, render_template, url_for, redirect, request
import csv
import operator
from datetime import datetime




app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        category = request.form.get('category')
        start_year= request.form.get('start_year')
        end_year = request.form.get('end_year')
        return redirect(url_for("genre", category=category, start_year=start_year, end_year=end_year))
    
    return render_template('home.html')


@app.route("/movies/")
def genre():
    
    category = request.args.get('category').capitalize()
    start_year = request.args.get('start_year')    
    end_year = request.args.get('end_year')    
    
    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        sorted_list = sorted(reader, key=operator.itemgetter(4), reverse=True)
        genre_list =[]

        for row in sorted_list:
            genre_col = row[2]

            year = row[4]

            if category in genre_col and int(year) > int(start_year) and int(year) < int(end_year):
                    genre_list.append(row)


    return render_template('genre.html', genre = genre_list, genre_col=genre_col, year=year)


@app.route("/movies/add", methods=["POST", "GET"])
def add_movie():

    current_year = datetime.now().year
    new_row=[]
    last_index=[]
    last_sn=[]
    genres = []
    errmsg=""

    with open('test.csv', 'r') as file:
            read = csv.reader(file)
            last_index = len(list(read))
            last_index = last_index+1
            last_sn = last_index

    if request.method == "POST":
        movie_title = request.form["movie_title"]
        genre = request.form['genre']
        year = request.form.get('released_year')            
        genres = '|'.join(genre.split())

        if year.isdigit() and int(year)<current_year:
            new_row=[last_index, last_sn, genres, movie_title, year]

            with open('test.csv', 'a', newline='') as file:
                write= csv.writer(file)
                write.writerow(new_row)

            return redirect(url_for('movies_list'))
        else:
            errmsg = "Invalid year"

    return render_template('add_movie.html', new_row=new_row, errmsg=errmsg)


@app.route("/movies_delete/<movie_id>")
def delete_movie(movie_id):
    id=movie_id
    new_list =[]

    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id:
                pass
            else:
                new_list.append(row)

    with open('test.csv', 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerows(new_list)


    return redirect(url_for('movies_list'))


@app.route("/allmovies/")
def movies_list():
    
    with open('test.csv', 'r') as file:
        reader = csv.reader(file)
        sorted_list = sorted(reader, key=operator.itemgetter(4), reverse=True)
        

    return render_template('movies.html', movies = sorted_list)







if __name__ == '__main__':
    app.rundebug=True
