from flask import Blueprint, render_template, redirect, url_for, request, session
from app.timer import start_timer, get_remaining_time, is_time_over
from app.database import get_connection
from app.api_cocktails import get_random_cocktail

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/play', methods=['GET', 'POST'])
def play():
    # Nouvelle partie ?
    if 'start_time' not in session:
        start_timer()
        session['score'] = 100

        # Charger un cocktail aléatoire depuis l'API
        cocktail = get_random_cocktail()
        session['cocktail_name'] = cocktail["name"]
        session['cocktail_image'] = cocktail["image"]
        session['ingredients'] = cocktail["ingredients"]

    # Temps restant
    remaining_time = get_remaining_time()
    if remaining_time <= 0:
        return redirect(url_for('main.game_over'))

    message = None
    current_score = session.get('score', 100)

    # Gestion du formulaire
    if request.method == 'POST':
        guess = request.form.get('guess', '').strip().lower()

        # Données du cocktail
        cocktail_name = session['cocktail_name'].lower()
        ingredients = [i.lower() for i in session['ingredients']]

        # Condition de réussite
        correct = (guess == cocktail_name) or (guess in ingredients)

        if correct:
            return redirect(url_for('main.game_over'))
        else:
            current_score = max(0, current_score - 1)
            session['score'] = current_score
            message = "Mauvaise réponse ! -1 point"

    return render_template(
        'play.html',
        remaining_time=remaining_time,
        score=current_score,
        message=message,
        cocktail_image=session['cocktail_image']  # <--- pour afficher l'image
    )

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


