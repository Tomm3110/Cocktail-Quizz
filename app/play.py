from flask import redirect, url_for, render_template, request, session
from app.timer import start_timer, get_remaining_time, is_time_over
from app.api_cocktails import get_random_cocktail

class Play :
	def play():
		# nouvelle partie 
		ingredients = [] # debug
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
			cocktail_image=session['cocktail_image'], 
			ingredients = ingredients # debug
		)