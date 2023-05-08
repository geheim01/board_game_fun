import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')

data = pd.read_csv("board_games_atlas.csv")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/games')
def games():
    # Get query parameters
    sortby = request.args.get('sortby', default='name')
    order = request.args.get('order', default='asc')
    search = request.args.get('search', default='')

    # Filter the data based on search query
    if search:
        print("search triggered with: ", search)
        filtered_data = data[data['name'].str.contains(search, case=False)]
    else:
        filtered_data = data

    # Sort the data
    sorted_data = filtered_data.sort_values(by=sortby, ascending=(order == 'asc'))

    # Convert the data to a list of dictionaries
    games_list = sorted_data.to_dict('records')

    for i in games_list:
        print(i['name'])
    # Return the games data as JSON if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(games_list)

    # Render the template with the games data
    return render_template('games.html', games=games_list, sortby=sortby, order=order, search=search)



if __name__ == '__main__':
    app.run(debug=True)
