import requests

def get_random_cocktail():
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    data = response.json()

    drink = data["drinks"][0]

    name = drink["strDrink"]
    image = drink["strDrinkThumb"]
    category = drink['strCategory']

    # Récupérer les ingrédients (max 15)
    ingredients = []
    for i in range(1, 16):
        ing = drink.get(f"strIngredient{i}")
        if ing:
            ingredients.append(ing)

    return {
        "name": name,
        "image": image,
        "ingredients": ingredients,
        "category":category
    }
