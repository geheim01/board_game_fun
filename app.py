"""
This module is a Flask application that provides a web interface for displaying and filtering board game data.

It uses the Flask framework and the pandas library for data manipulation and rendering templates.

The main routes of the application are:
- "/" - Renders the home.html template.
- "/games" - Renders the games.html template and provides game data based on query parameters.

The module also reads board game data from a CSV file and performs data preprocessing before serving the data.
"""

import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="templates")

data = pd.read_csv("data/board_games_atlas.csv")

data.drop(columns=["Unnamed: 0"])
data["min_players"] = data["min_players"].astype("Int64")
data["max_players"] = data["min_players"].astype("Int64")
data["min_playtime"] = data["min_playtime"].astype("Int64")


@app.route("/")
def index():
    """
    Renders the home.html template.

    Returns:
        The rendered home.html template.
    """
    return render_template("home.html")


@app.route("/games")
def games():
    """
    Renders the games.html template and provides game data.

    Returns:
        If the request is AJAX, returns the game data as JSON.
        Otherwise, returns the rendered games.html template.
    """
    # Get query parameters
    sortby = request.args.get("sortby", default="name")
    order = request.args.get("order", default="asc")
    search = request.args.get("search", default="")

    # Filter the data based on search query
    if search:
        filtered_data = data[data["name"].str.contains(search, case=False)]
    else:
        filtered_data = data

    # Sort the data
    sorted_data = filtered_data.sort_values(by=sortby, ascending=order == "asc")

    # Convert the data to a list of dictionaries
    games_list = sorted_data.to_dict("records")

    # Return the games data as JSON if the request is AJAX
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(games_list)

    # Render the template with the games data
    return render_template(
        "games.html", games=games_list, sortby=sortby, order=order, search=search
    )


if __name__ == "__main__":
    app.run(debug=True)
