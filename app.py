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

# Global button style
button_style = {
    #"border": "1px solid black",
    "padding": "8px 15px",
    "border-radius": "5px",
    "text-decoration": "none",
    "background-color": "#ffffff",
    "color": "black",
    "height": "22px"
}

# Custom labels for pages
custom_labels = {
    "/about" : "About",
    "/corona" : "COVID-19",
    "/countries" : "Other Countries",
    "/data" : "Data",
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

    html.Div([

        dcc.Link("Home", href="/", 
            style={#"border": "1px solid black",
                    "padding": "8px 15px",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "background-color": "#ffffff",
                    "color": "black",
                    "height":"22px"}
        ),

        dcc.Link("Data", href="/data", style=button_style),

        dcc.Dropdown(
            options=[
                {"label": "Trends in Germany", "value": "/germany"},
                {"label": "New Years", "value": "/newyears"},
                {"label": "COVID-19", "value": "/corona"},
                {"label": "States", "value": "/states"},
                {"label": "Location", "value": "/location"},
                {"label": "Season", "value": "/seasons"}
            ],
            placeholder="UBA",
            id="germany-dropdown1",
            style={"width": "100px",
                    #"border": "1px solid black",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "color": "black",
                    "height":"38px"},
                    maxHeight=400,
                    searchable=False
        ),

        dcc.Dropdown(
            options=[
                {"label": "Weather", "value": "/weather"}
            ],
            placeholder="Weather",
            id="events-dropdown2",
            style={"width": "140px",
                   #"border": "1px solid black",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "color": "black",
                    "height":"38px"},
                    maxHeight=400,
                    searchable=False
        ),

        dcc.Dropdown(
            options=[
                {"label": "Summer Holidays", "value": "/holiday"}
            ],
            placeholder="Holidays",
            id="events-dropdown3",
            style={"width": "140px",
                   #"border": "1px solid black",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "color": "black",
                    "height":"38px"},
                    maxHeight=400,
                    searchable=False
        ),

        dcc.Dropdown(
            options=[
                {"label": "Other Countries", "value": "/countries"}
            ],
            placeholder="International",
            id="events-dropdown4",
            style={"width": "190px", 
                   #"border": "1px solid black",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "color": "black",
                    "height":"38px"},
                    maxHeight=400,
                    searchable=False
        ),

        dcc.Link("About", href="/about", style=button_style),

    ], style={"display": "flex", 
                    "gap": "20px", 
                    "margin": "0px",
                    "border": "1px solid black",
                    "padding": "8px 15px",
                    "border-radius": "5px",
                    "text-decoration": "none",
                    "background-color":  "rgb(53, 167, 187)",
                    "color": "black",
                    "align-items":"center",
                    "justify-content": "center",
                    "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                    "position": "sticky",
                    "top":"0",
                    "z-index": "1000"}),

    dcc.Location(id="url"),

    dash.page_container
]),

@callback(
    Output("url", "pathname"),
    Input("germany-dropdown1", "value"),
    Input("events-dropdown2", "value"),
    Input("events-dropdown3", "value"),
    Input("events-dropdown4", "value"),
    prevent_initial_call=True
)
def navigate_page(v1, v2, v3, v4):

    for v in [v1, v2, v3, v4]:
        if v:
            return v
###################
### Run the APP ###
###################

if __name__ == "__main__":
    app.run(debug=True)