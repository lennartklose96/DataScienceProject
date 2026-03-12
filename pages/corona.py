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
    "daily": {
        "PM10": pd.read_csv("Collected Data/Question 1.1/corona_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1.1/corona_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1.1/corona_NO2.csv"),
    },
    "monthly": {
        "PM10": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_NO2.csv"),
    }
}

for period in data.values():          # daily, monthly, monthly-10-year-span
    for df in period.values():        # PM10, PM2.5, NO2
        df["date start"] = pd.to_datetime(df["date start"])

pollutants={"PM10","PM2.5","NO2"}

##################
### App layout ###
##################

layout = html.Div([

    html.H2("COVID-19"),

    html.Label("Select Time Period"),
    dcc.Dropdown(
        id="corona_time-dropdown",
        options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Monthly", "value": "monthly"},
        ],
        value="daily",
        clearable=False,
        style={"margin-right": "40px", "width": "200px"}
    ),

    html.Br(),

    html.Label("Select Pollutants"),
    dcc.Dropdown(
        id="corona_pollutant-dropdown",
        options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2.5"},
            {"label": "NO\u2082", "value": "NO2"}
        ],
        value=["PM10"],
        multi=True,
        clearable=False,
        style={"margin-right": "40px", "width": "200px"}
    ),

    dcc.Graph(id="corona_pollution-graph"),
])

#################
### Callbacks ###
#################

@callback(
    Output("corona_pollution-graph", "figure"),
    Input("corona_time-dropdown", "value"),
    Input("corona_pollutant-dropdown", "value")
)
def update_graph(time_period, pollutants):

    fig = go.Figure()

    for p in pollutants:
        df = data[time_period][p]

        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="lines",
                name=p
            )
        )


    for p in pollutants:
        df = data[time_period][p]
        # Regression
        if len(df) > 1:  # mindestens 2 Punkte
            x_num = df["date start"].map(pd.Timestamp.toordinal)
            y = df["value"]

            n_points = len(df)
            if n_points <= 20:
                deg = min(2, n_points - 1)
            else:
                deg = 3

            coeff = np.polyfit(x_num, y, deg)
            poly = np.poly1d(coeff)
            y_reg = poly(x_num)

            fig.add_trace(
                go.Scatter(
                    x=df["date start"],
                    y=y_reg,
                    mode="lines",
                    name=p + " trend",
                )
            )

    fig.update_layout(
        title="Air quality during the coronavirus pandemic",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)",
        showlegend=False
    )

    return fig