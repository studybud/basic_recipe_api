from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/hello')
def hello():
    return "Hello Flask World!"
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/')
def index():
    return "Welcome to Nazzy's Kitchen"
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify({"data": recipes})
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):

    print(f"recipe id requested: {recipe_id}")
    # iterate through recipes & retrieve ID requested or None if nor
    recipe = next((recipe for recipe in recipes if recipe["id"] == recipe_id), None)
    print(f"recipe found: {recipe}")

    if recipe:
        return jsonify(recipe)

    print(f"retuning: recipe id requested: {recipe_id} \nrecipe found: {recipe}")
    return jsonify({"message": "recipe not found"}), HTTPStatus.NOT_FOUND
# ///////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    app.run()
