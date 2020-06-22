from flask import Flask, jsonify, request, render_template
from http import HTTPStatus
import logging

# create logger
logger = logging.getLogger(
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s'))
# logging.basicConfig(level=logging.DEBUG, format=f'{asctime} [{levelname}]: {message}')

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.',
        'ingredients': [{'eggs': '2'}, {'mayonnaise': '500 ml'}, {'parsley': '3-4 leaves'}, {'salt': 'to taste'},
                        {'pepper': 'to taste'}],
        'method': 'mix everything nicely!'
    },
    {
        'id': 2,
        'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.',
        'ingredients': ['tomato', 'noodles', 'garlic', 'salt', 'pepper'],
        'method': 'mix everything nicely!'
    },
    {
        'id': 3,
        'name': 'Potato Salad',
        'description': 'This is an awesome potato salad recipe.',
        'ingredients': ['potato', 'mayonnaise', 'chives', 'salt', 'pepper'],
        'method': 'mix everything nicely!'
    },
    {
        'id': 4,
        'name': 'Toasted Cheese',
        'description': 'This is crunchy sticky toasted cheese recipe.',
        'ingredients': ['bread', 'mayonnaise', 'butter', 'salt', 'pepper', 'tomato - optional'],
        'method': 'mix everything nicely!'
    },
    {
        "id": 5,
        "name": "Cheese Pizza",
        "description": "This is a lovely cheese pizza"
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
    """have to say something here"""
    logger.info(f"recipe id requested: {recipe_id}")
    # iterate through recipes & retrieve ID requested or None if nor
    recipe = next((recipe for recipe in recipes if recipe["id"] == recipe_id), None)
    logger.info(f"type: {type(recipe)} >> recipe found: {recipe}")

    if recipe:
        logger.info(f"type: {type(recipe)} >> recipe found: {recipe}")
        # return jsonify(recipe)
        return render_template('recipe.html', recipe=recipe)

    return jsonify({"message": "recipe not found"}), HTTPStatus.NOT_FOUND
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes/name/<string:search_keyword>', methods=['GET'])
def get_recipe_by_search_keyword(search_keyword):
    """have to say something here"""
    logger.info(f"searching for recipes by name: {search_keyword}")
    # iterate through recipes & retrieve ID requested or None if not found
    # recipes_found = next((recipe for recipe in recipes if search_keyword.lower() in recipe["name"].lower()), None)
    recipes_found = [recipe for recipe in recipes if search_keyword.lower() in recipe["name"].lower()]
    logger.info(f"recipes found: {recipes_found}")

    if recipes_found:
        logger.info(f"retuning: recipes requested: {search_keyword} \nrecipe found: {recipes_found}")
        return jsonify(recipes_found)

    return jsonify({"message": "recipe\\s not found"}), HTTPStatus.NOT_FOUND
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes', methods=['POST'])
def create_recipe():
    """have to say something here"""
    data_submitted = request.get_json()
    logger.info(f"data request type: {type(data_submitted)} - data request:: {data_submitted}")
    name = data_submitted.get('name')
    description = data_submitted.get('description')

    new_recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(new_recipe)

    return jsonify(new_recipe), HTTPStatus.CREATED
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    """have to say something here"""
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message': f'recipe {recipe_id} not found'}), HTTPStatus.NOT_FOUND

    data_submitted = request.get_json()

    recipe.update(
        {
            'name': data_submitted.get('name'),
            'description': data_submitted.get('description')
        }
    )

    return jsonify(recipe)
# ///////////////////////////////////////////////////////////////////////////////////////


# ///////////////////////////////////////////////////////////////////////////////////////
@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    """have to say something here"""
    logger.info(f"recipe id to delete: {recipe_id}")
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    logger.info(f"recipe to delete type: {type(recipe)}")
    if not recipe:
        return jsonify({'message': f'recipe {recipe_id} not found'}), HTTPStatus.NOT_FOUND

    logger.info(f"recipe len: {len(recipes)}, index: {recipes.index(recipe)}")
    recipe_deleted = recipes.pop(recipes.index(recipe))
    # recipe_deleted = recipes.remove(recipe)

    # return jsonify(recipe)
    # return jsonify({"deleted": recipe_deleted}), HTTPStatus.NO_CONTENT
    return jsonify({"deleted": recipe_deleted})
# ///////////////////////////////////////////////////////////////////////////////////////


if __name__ == "__main__":
    # print helper urls to test with
    import helper_urls
    for url in helper_urls.urls:
        print(url)

    app.run(debug=True, host='0.0.0.0', port='5000')
