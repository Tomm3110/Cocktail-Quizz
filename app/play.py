from flask import redirect, url_for, render_template, request, session
from game_timer import start_timer, get_remaining_time, is_time_over
from api_cocktails import get_random_cocktail

class Play :
	def play():
		# nouvelle partie 
		ingredients = [] # debug
		if 'start_time' not in session:
			start_timer()
			session['score'] = 100

		# Temps restant
		remaining_time = get_remaining_time()
		if remaining_time <= 0:
			return redirect(url_for('game_over'))
		
		# Charger un cocktail aléatoire depuis l'API
		if 'cocktail_name' not in session:
			cocktail = get_random_cocktail()
			session['cocktail_name'] = cocktail["name"]
			session['cocktail_image'] = cocktail["image"]
			session['ingredients'] = cocktail["ingredients"]
			session['cocktail_category'] = cocktail.get('category', 'Inconnue')

			session['hints_revealed'] = 0

		message = None
		current_score = session.get('score', 100)
		hints_count = session.get('hints_revealed', 0)

		# Données du cocktail
		cocktail_name = session['cocktail_name'].lower()
		ingredients = [i.lower() for i in session['ingredients']]

		# Gestion du formulaire
		if request.method == 'POST':
			guess = request.form.get('guess', '').strip().lower()

			if (len(guess) >= 3) and (guess in cocktail_name):
				session['score'] = current_score + 10 

				session.pop('cocktail_name', None)
				session.pop('ingredients', None)
				session.pop('cocktail_image', None)
				session.pop('cocktail_category', None)
                
				return redirect(url_for('play'))
			
			elif guess in ingredients:
				message = "C'est un ingrédient, il faut le nom du cocktail !"
            
			else:
				current_score = max(0, current_score - 1)
				session['score'] = current_score
				message = "Mauvaise réponse ! -1 point"
				session['hints_revealed'] = hints_count + 1
		
		original_ingredients = session['ingredients']
		current_hints_count = session.get('hints_revealed', 0)
		difficulty = session.get('difficulty', 'easy')

		if difficulty == 'hard':
			visible_ingredients = original_ingredients
		else:
			visible_ingredients = original_ingredients[:current_hints_count]

		return render_template('play.html',
			remaining_time=remaining_time,
			score=current_score,
			message=message,
			cocktail_image=session['cocktail_image'], 
			ingredients=visible_ingredients,
			category=session.get('cocktail_category', 'Inconnue')
		)