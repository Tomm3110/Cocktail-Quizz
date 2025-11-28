from flask import Blueprint, render_template, redirect, url_for, request, session
from app.timer import start_timer, get_remaining_time, is_time_over
from app.database import get_connection
from app.api_cocktails import get_random_cocktail
from app.play import Play

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/play', methods=['GET', 'POST'])
def play() :
    return Play.play()

@main.route('/game_over')
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

            return redirect(url_for('main.scores'))

    return render_template('game_over.html', score=score)


@main.route('/scores')
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


