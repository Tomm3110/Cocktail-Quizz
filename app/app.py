from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
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
