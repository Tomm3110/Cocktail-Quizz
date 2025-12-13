from flask import Flask, Blueprint, flash, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from game_timer import start_timer, get_remaining_time, is_time_over, reset_timer
from database import get_connection, init_db
from api_cocktails import get_random_cocktail
from play import Play
import sqlite3

app = Flask(__name__)

init_db()

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

@app.route('/play', methods=['GET', 'POST'])
def play() :
    return Play.play()


@app.route('/ff')
def ff() :
    reset_timer()
    session.pop("score", None)
    session.pop("cocktail_name", None)
    return redirect(url_for('home'))


@app.route('/game_over', methods=['GET', 'POST'])
def game_over():
    score = session.get('score', 0)
    reset_timer()

    if request.method == 'POST':
        player_name = request.form.get('player_name', '').strip()
        user_id = session.get('user_id')

        if player_name:
            conn = get_connection()
            conn.execute(
                "INSERT INTO scores (pseudo, score, user_id) VALUES (?, ?, ?)",
                (player_name, score, user_id)
            )
            conn.commit()
            conn.close()

            # Reset pour la prochaine partie
            session.pop('score', None)

            return redirect(url_for('scores'))

    return render_template('game_over.html', score=score)


@app.route('/scores')
def scores():
    conn = get_connection()
    cur = conn.execute(
        "SELECT pseudo, score FROM scores ORDER BY score DESC"
    )
    scores = cur.fetchall()
    conn.close()

    return render_template('scores.html', scores=scores)

@app.route('/login',  methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_connection()
        user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home')) 
        else:
            flash("Email ou mot de passe incorrect.", 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash("Les mots de passe ne correspondent pas !", 'error')
            return redirect(url_for('register'))
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        conn = get_connection()
        try:
            conn.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conn.commit()
            flash("Inscription réussie ! Veuillez vous connecter.", 'success')
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            flash("Ce pseudo ou cet email est déjà utilisé !", 'error')            
            return redirect(url_for('register'))        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/mes-scores')
def my_scores():
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour voir vos scores.", 'error')
        return redirect(url_for('login'))

    user_id = session['user_id']
    username = session['username']

    conn = get_connection()
    cur = conn.execute("SELECT pseudo, score FROM scores WHERE user_id = ? ORDER BY score DESC", (user_id,))
    personal_scores = cur.fetchall()
    conn.close()

    return render_template('my_scores.html', scores=personal_scores, username=username)


if __name__ == '__main__':
    app.run(debug=True)
