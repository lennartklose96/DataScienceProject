import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

###############
### Styling ###
###############

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Custom labels for pages
custom_labels = {
    "/corona" : "COVID-19",
    "/countries" : "Other Countries",
    "/germany" : "Trends in Germany",
    "/home" : "Home",
    "/location" : "Rural Areas",
    "/newyears" : "New Years",
    "/seasons" : "Seasons",
    "/holiday": "Summer Holidays",
    "/states" : "States",
    "/weather": "Weather"
}

#########################
### App initilization ###
#########################

# Initialize Dash app
app = dash.Dash(
    __name__,
    use_pages = True,
    external_stylesheets=external_stylesheets
)
# Start server for render
server = app.server

##################
### App layout ###
##################

app.layout = html.Div([
    html.H1(
        "Air Pollution in Germany"
    ),
    # Navigation links
    html.Div([
        html.Div(
            dcc.Link(
                custom_labels.get(page["path"], page["name"]),
                href=page["relative_path"],
                style={"margin-right": "20px"}  # optional spacing
            )
        ) for page in dash.page_registry.values()
    ], style={"margin-bottom": "30px"}),

    # Page container
    dash.page_container
])


###################
### Run the APP ###
###################

if __name__ == "__main__":
    app.run(debug=True)