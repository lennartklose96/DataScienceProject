import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__, "/data")

layout = html.Div([
    html.H2("This is our homepage for the Data Science Project"),
    html.Div("We will put content here."),
])