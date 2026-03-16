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
        # first row
        # left side
        html.Div("Who?", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # right side
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
            "font-size": "18px",
        })
    ], style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "25px auto 25px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    }),

    html.Div(
    children=[
        # second row
        # left side
        html.Div("What?", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # right side
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
    ], style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "25px auto 25px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    }),

    html.Div(
    children=[
        # third row
        # left side
        html.Div("Why?", style={
            "padding": "20px",
            "border-radius": "5px",
            "color": "white",
            "text-align": "left",
            "color": "black",
            "font-size": "30px"
        }),
        # right side
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
    ], style={
        "display": "grid",
        "grid-template-columns": "30% 70%",
        "grid-gap": "20px",
        "padding": "20px",
        "margin": "25px auto 0px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    })
])