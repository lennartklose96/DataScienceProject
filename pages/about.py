import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

layout = html.Div([
    html.Div(
    children=[
        # Linke Textbox
        html.Div("Who", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # Rechte Textbox
        html.Div("Our group consists of four members. Lennart, Lasse, Jonas, and Finn. " \
        "We are studying \"Business Information Technology\" (Wirtschaftsinformatik) and "
        "Computer Science at Kiel University (CAU) in northern Germany. For most of us, "
        "this data science project is part of our fifth semester and is a required component "
        "of our bachelor’s degree."
        , style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "center",
            "text-align": "left",
            "color": "black",
        })
    ],
    style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "50px auto 50px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    }),

    html.Div(
    children=[
        # Linke Textbox
        html.Div("What", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # Rechte Textbox
        html.Div("In this project, we analyze air quality data from Germany for the period " \
        "from 2016 to 2026. The project was completed over a four-week period. During this " \
        "time, we had to collect, process, and analyze the data, as well as create the final " \
        "visualizations. This was followed by a presentation of the results, a poster based " \
        "on the findings, and this website."
        , style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "center",
            "text-align": "left",
            "color": "black",
        })
    ],
    style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "50px auto 50px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    }),

    html.Div(
    children=[
        # Linke Textbox
        html.Div("Why", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # Rechte Textbox
        html.Div("Air quality is a key factor for the environment and public health. By " \
        "analyzing long-term measurement data, it is possible to identify trends, changes, "
        "and potential correlations with events, weather conditions, or human activity. " \
        "Such studies help us better understand the evolution of air pollution and provide " \
        "a basis for discussions on environmental measures and sustainable urban development."
        , style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "center",
            "text-align": "left",
            "color": "black",
        })
    ],
    style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "50px auto 50px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    })
])