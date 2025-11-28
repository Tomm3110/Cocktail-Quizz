from flask import Flask, Blueprint, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from timer import start_timer, get_remaining_time, is_time_over
from database import get_connection
from api_cocktails import get_random_cocktail
from play import Play
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('cocktail.db', check_same_thread=False)
cur = con.cursor()

app.secret_key = 'dev-cocktail'

@app.route("/")
def home():
    content = {
        "titre": "Bienvenue sur Cocktail Quiz 🍸",
        "accroche": "Teste tes connaissances sur les cocktails les plus célèbres (et les plus insolites).",
        "description": "Réponds aux questions, découvre de nouvelles recettes et deviens le roi du bar ! Prêt à jouer ? Clique et secoue ton cerveau !",
        "bouton": "Play"
    }
    return render_template('home.html', data=content)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/play', methods=['GET', 'POST'])
def play() :
    return Play.play()

@app.route('/game_over')
def game_over():
    score = session.get('score', 0)

    if request.method == 'POST':
        player_name = request.form.get('player_name', '').strip()

        if player_name:
            conn = get_connection()
            conn.execute(
                "INSERT INTO scores (player_name, score) VALUES (?, ?)",
                (player_name, score)
            )
            conn.commit()
            conn.close()

            # Reset pour la prochaine partie
            session.pop('start_time', None)
            session.pop('score', None)

            return redirect(url_for('scores'))

    return render_template('game_over.html', score=score)


@app.route('/scores')
def scores():
    conn = get_connection()
    cur = conn.execute(
        "SELECT player_name, score, created_at "
        "FROM scores "
        "ORDER BY score DESC, created_at ASC"
    )
    scores = cur.fetchall()
    conn.close()

    return render_template('scores.html', scores=scores)
