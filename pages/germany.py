import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

##################
### Constants ####
##################

PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅
NO2_LABEL = "NO\u2082"          # NO₂

# Dictionary for labels per pollutant
POLLUTANT_LABELS = {
    "PM10": PM10_LABEL,   # PM₁₀
    "PM2.5": PM25_LABEL,  # PM₂.₅
    "NO2":  NO2_LABEL     # NO₂
}

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
        "PM10": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_NO2.csv"),
    },
    "monthly": {
        "PM10": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_NO2.csv"),
    },
    "yearly": {
        "PM10": pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_NO2.csv"),
    }
}


for period_name, period in data.items():
    for df in period.values():

        if period_name == "yearly":
            df["date start"] = pd.to_datetime(df["date start"], format="%Y")

        else:
            df["date start"] = pd.to_datetime(df["date start"], errors="coerce")

pollutants={"PM10","PM2.5","NO2"}

##################
### App layout ###
##################

layout = html.Div([

    # Title
    #html.H2("Air Pollution Germany"),

    # Research question
    html.Div([
        #html.H3("Research Question"),
        html.H4([
            "How did the average values of PM₁₀, PM₂.₅ and NO₂ change in Germany?"
        ], style={
            "font-size": "30px"
        }),
        html.P([
           "TODO"
        ]),
    ]),

    # Data description
    html.Div([
        html.H6("Used Data"),
        html.P([
            "TODO"
        ]),
    ]),

    # Visualization description
    html.Div([
        html.H6("Visualization"),
        html.P([
           "TODO"
        ]),
    ]),

    html.Hr(),

    # Controls
    html.Div([

        html.Div([
            html.Label("Select Time Period"),
            dcc.Dropdown(
                id="Q10_time-dropdown",
                options=[
                    {"label": "Daily", "value": "daily"},
                    {"label": "Monthly", "value": "monthly"},
                    {"label": "Yearly", "value": "yearly"}
                ],
                value="monthly",
                clearable=False,
                searchable=False,
                style={"width": "200px"}
            ),
        ]),

        html.Div([
            html.Label("Select Pollutants"),
            dcc.Dropdown(
                id="Q10_pollutant-dropdown",
                options=[
                    {"label": POLLUTANT_LABELS["PM10"], "value": "PM10"},
                    {"label": POLLUTANT_LABELS["PM2.5"], "value": "PM2.5"},
                    {"label": POLLUTANT_LABELS["NO2"], "value": "NO2"}
                ],
                value=["PM10"],
                multi=True,
                clearable=False,
                searchable=False,
                style={"width": "200px"}
            ),
        ]),
    ], style={"display": "flex", "align-items": "center", "margin-bottom": "30px", "gap" : "40px"}),

    html.Div([
        # Graph
        dcc.Graph(id="Q10_pollution-graph", style={"width": "100%"}),
    ], style={
            "display": "flex",
            "gap": "20px",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)"
            }),

    html.Hr(),

    # Interpretation
    html.Div([
        html.H4("Interpretation"),
        html.P([
            "TODO"
        ])
    ]),

])

@callback(
    Output("Q10_pollution-graph", "figure"),
    Input("Q10_time-dropdown", "value"),
    Input("Q10_pollutant-dropdown", "value")
)
def update_graph(time_period, pollutants):

    fig = go.Figure()

    for p in pollutants:
        df = data[time_period][p]

        fig.add_trace(
            go.Bar(
                x=df["date start"],
                y=df["value"],
                name=POLLUTANT_LABELS[p]
            )
        )

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
                    name=POLLUTANT_LABELS[p] + " trend",
                )
            )

    fig.update_layout(
        title="Air quality in Germany over the last 10 years",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig

options=[
                    {"label": POLLUTANT_LABELS["PM10"], "value": "PM10"},
                    {"label": POLLUTANT_LABELS["PM2.5"], "value": "PM2.5"},
                    {"label": POLLUTANT_LABELS["NO2"], "value": "NO2"}
                ],