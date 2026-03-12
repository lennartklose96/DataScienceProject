import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

###########################
### Initialize Dash app ###
###########################

# Initialize Dash page
dash.register_page(__name__)

###########################
### Loading data frames ###
###########################

data = {
    "PM10":  pd.read_csv("Collected Data/Question 1.2/neujahr_PM10.csv"),
    "PM2.5":  pd.read_csv("Collected Data/Question 1.2/neujahr_PM2,5.csv"),
    "NO2":  pd.read_csv("Collected Data/Question 1.2/neujahr_NO2.csv"),

    "PM10yearly":  pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM10.csv"),
    "PM2.5yearly":  pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM2,5.csv"),
    "NO2yearly":  pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_NO2.csv")
}

for name, df in data.items():

    if "yearly" in name:
        df["date start"] = pd.to_datetime(df["date start"], format="%Y")
    else:
        df["date start"] = pd.to_datetime(df["date start"])


##################
### App layout ###
##################

layout = html.Div([
    html.H2("New Years"),

    html.Label("Select Pollutants"),
    dcc.Dropdown(
        id="newyears_pollutant-dropdown",
        options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2.5"},
            {"label": "NO\u2082", "value": "NO2"},
            {"label": "PM\u2081\u2080 avg for each year", "value": "PM10yearly"},
            {"label": "PM\u2082.\u2085 avg for each year", "value": "PM2.5yearly"},
            {"label": "NO\u2082 avg for each year", "value": "NO2yearly"}
        ],
        value=["PM10"],
        clearable=False,
        searchable = False,
        multi=True,
        style={"margin-right": "40px", "width": "200px"}
    ),

    dcc.Graph(id="newyears_pollutant-graph")
])

#################
### Callbacks ###
#################

@callback(
    Output("newyears_pollutant-graph", "figure"),
    Input("newyears_pollutant-dropdown", "value")
)
def update_graph(selected_pollutants):
    fig = go.Figure()

    for name in selected_pollutants:
        df = data[name]

        # Scatter points
        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="markers",
                name=name,
            )
        )

        # Regression
        if len(df) > 3:
            x_num = df["date start"].map(pd.Timestamp.toordinal)
            y = df["value"]
            coeff = np.polyfit(x_num, y, 3)
            poly = np.poly1d(coeff)
            y_reg = poly(x_num)

            fig.add_trace(
                go.Scatter(
                    x=df["date start"],
                    y=y_reg,
                    mode="lines",
                    name=name + " trend",
                )
            )

    fig.update_layout(
        title="Germany around New Year",
        xaxis_title="Date",
        yaxis_title="Concentration in µg/m³",
        hovermode="closest",
        showlegend=False
    )

    return fig