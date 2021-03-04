from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

import pg8000.native as postgres
import credentials

import datetime

@app.route('/')
def main_page():
    conn = postgres.Connection(credentials.user, **credentials.auth)
    query = 'SELECT title, author, date, text, status FROM suggestions;'
    res = conn.run(query)
    for row in res:
        row[2] = row[2].strftime('%d/%m/%Y %H:%M')
    conn.close()
    print(res)
    return render_template('main.html', suggestions=res)


@app.route('/insert', methods=['post'])
def insert_suggestion():
    params = {
        'author': request.form['author'].rstrip(),
        'text': request.form['text'],
        'title': request.form['title'].rstrip(),
        'date': datetime.datetime.now().isoformat(sep=' ')
    }

    conn = postgres.Connection(credentials.user, **credentials.auth)
    query = """
        INSERT INTO suggestions 
        (title, author, text, date, status) 
        VALUES (:title, :author, :text, :date, 'new')
    """
    conn.run(query, **params)
    conn.close()

    return render_template('suggestion_sent.html')


# CREATE TYPE status AS ENUM ('new', 'approved', 'rejected', 'done', 'discarded');
# CREATE TABLE suggestions (id serial PRIMARY KEY, title text, author text, text text, date timestamp, status status);

# TODO: remove remote access https://bigbinary.com/blog/configure-postgresql-to-allow-remote-connection