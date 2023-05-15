import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

data = pd.read_csv("data/board_games_atlas.csv")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/games')
def games():
    # Get query parameters
    sortby = request.args.get('sortby', default='name')
    order = request.args.get('order', default='asc')
    search = request.args.get('search', default='')
    category = request.args.get('categories', default='')
    mechanic = request.args.get('mechanic', default='')
    players = request.args.get('players', default='')

    # Filter the data based on search query
    if search:
        filtered_data = data[data['name'].str.contains(search, case=False)]
    else:
        filtered_data = data

    # Filter the data based on category, mechanic, and players
    if category:
        filtered_data = filtered_data[filtered_data['categories'] == category]
    if mechanic:
        filtered_data = filtered_data[filtered_data['mechanics'] == mechanic]
    if players:
        filtered_data = filtered_data[filtered_data['min_players'].astype(str) <= players]
        filtered_data = filtered_data[filtered_data['max_players'].astype(str) >= players]

    # Sort the data
    sorted_data = filtered_data.sort_values(by=sortby, ascending=(order == 'asc'))

    # Replace NaN values with None and convert the data to a list of dictionaries
    games_list = sorted_data.fillna(value='ffill').to_dict('records')

    # Return the games data as JSON if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(games_list)

    # Render the template with the games data
    return render_template('games.html', games=games_list, sortby=sortby, order=order, search=search)

if __name__ == '__main__':
    app.run(debug=True)
