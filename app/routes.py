from flask import Blueprint, render_template, redirect, url_for, request, session
from app.timer import start_timer, get_remaining_time, is_time_over

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/play', methods=['GET', 'POST'])
def play():
    if 'start_time' not in session:
        start_timer()

    if is_time_over():
        return redirect(url_for('main.game_over'))

    if request.method == 'POST':
        if is_time_over():
            return redirect(url_for('main.game_over'))

    remaining_time = get_remaining_time()
    return render_template('play.html', remaining_time=remaining_time)

@main.route('/game_over')
def game_over():
    score = session.get('score')
    session.pop('start_time',None)
    return render_template('game_over.html',score=score)


