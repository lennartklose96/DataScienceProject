import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, path = "/")

layout = html.Div([
    html.H1("What is the state of air pollution in German cities?", style={
        "font-size": "30px"
    } ),
    html.Div("In this project, we analyze trends in air quality in Germany from " \
    "January 1, 2016, to March 1, 2026, focusing on the pollutants PM₁₀, PM₂.₅, and NO₂. " \
    "The goal is to analyze trends and patterns in air pollution and to identify potential " \
    "influencing factors. To this end, we examine temporal changes, regional differences, "
    "and the influence of specific events, weather conditions, and seasonal factors. We " \
    "also compare different types of measurement station locations and, in some cases, " \
    "place the results in an international context."),
], style={
        "padding": "20px",
        "margin": "30px auto 30px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff",
        "font-size": "20px"
    })