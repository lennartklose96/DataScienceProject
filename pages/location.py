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


data = {
    "daily": {
        "rural": pd.read_csv("Collected Data/Question 3/daily_avg_ländlich_PM10.csv"),
        "urban": pd.read_csv("Collected Data/Question 3/daily_avg_städtisch_PM10.csv"),
        "suburban": pd.read_csv("Collected Data/Question 3/daily_avg_vorstädtisch_PM10.csv"),
    },
    "monthly": {
        "rural": pd.read_csv("Collected Data/Question 3/monthly_avg_ländlich_PM10.csv"),
        "urban": pd.read_csv("Collected Data/Question 3/monthly_avg_städtisch_PM10.csv"),
        "suburban": pd.read_csv("Collected Data/Question 3/monthly_avg_vorstädtisch_PM10.csv"),
    }
}

data2 = {
    "rural": {
        "background": pd.read_csv("Collected Data/Question 3.1/monthly_avg_ländlich_hintergrund_PM10.csv"),
        "traffic": pd.read_csv("Collected Data/Question 3.1/monthly_avg_ländlich_verkehr_PM10.csv"),
        "industrie": pd.read_csv("Collected Data/Question 3.1/monthly_avg_ländlich_industrie_PM10.csv"),
    },
    "urban": {
        "background": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_hintergrund_PM10.csv"),
        "traffic": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_verkehr_PM10.csv"),
        "industrie": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_industrie_PM10.csv"),
    },
    "suburban": {
        "background": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_hintergrund_PM10.csv"),
        "traffic": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_verkehr_PM10.csv"),
        "industrie": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_industrie_PM10.csv"),
    }
}


for period in data2.values():
    for df in period.values():

        if df["date start"].astype(str).str.len().iloc[0] == 7:
            df["date start"] = pd.to_datetime(df["date start"], format="%Y-%m")
        else:
            df["date start"] = pd.to_datetime(df["date start"])

for period in data.values():
    for df in period.values():

        if df["date start"].astype(str).str.len().iloc[0] == 7:
            df["date start"] = pd.to_datetime(df["date start"], format="%Y-%m")
        else:
            df["date start"] = pd.to_datetime(df["date start"])

pollutants={"PM10","PM2.5","NO2"}

##################
### App layout ###
##################

layout = html.Div([

    html.Div([
        ######################
        ### First question ###
        ######################

        # Title
        #html.H2("Air Pollution Levels by Area Type"),

        # Research question
        html.Div([
            #html.H3("Research Question"),
            html.H4([
                "How does air pollution vary across urban, suburban and rural areas?"
            ], style={
                "font-size": "30px"
            }),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H6("Used Data"),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H6("Visualization"),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 10px 30px"}),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "40px auto 75px auto",
                }),

    html.Div([
        # Controls (time period + area type)
        html.Div([

            html.Div([
                html.Label("Select Time Period"),
                dcc.Dropdown(
                    id="location_time-dropdown",
                    options=[
                        {"label": "Daily", "value": "daily"},
                        {"label": "Monthly", "value": "monthly"}
                    ],
                    value="daily",
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

            html.Div([
                html.Label("Select Area Type"),
                dcc.Dropdown(
                    id="location_area-dropdown",
                    options=[
                        {"label": "Rural", "value": "rural"},
                        {"label": "Urban", "value": "urban"},
                        {"label": "Suburban", "value": "suburban"}
                    ],
                    value=["rural"],
                    multi=True,
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

        ], style={
            "display": "flex",
            "gap": "40px",
            "margin": "30px 30px 0px 30px"
        }),

        html.Div([
            # Graph
            dcc.Graph(id="location_pollution-graph" , style={"width": "100%"}),
        ], style={
                "display": "flex",
                "gap": "20px",
                }),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "75px auto 75px auto",
                }),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "TODO"
        ],style={"margin": "10px 30px 10px 30px"})
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "75px auto 75px auto",
                }),

    #######################
    ### Second question ###
    #######################

    # Title for second section
    #html.H2("Air Pollution Levels by Area Type and Source"),

    html.Div([
        # Research question
        html.Div([
            #html.H3("Research Question"),
            html.H4([
                "How does air pollution vary between background, traffic and industrial monitoring stations?"
            ], style={
                "font-size": "30px"
            }),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H6("Used Data"),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H6("Visualization"),
            html.P([
                "TODO"
            ]),
        ],style={"margin": "10px 30px 10px 30px"}),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "75px auto 75px auto",
                }),

    html.Div([
        # Controls (area type + source)
        html.Div([

            html.Div([
                html.Label("Select Area Type"),
                dcc.Dropdown(
                    id="location_area-dropdown-2",
                    options=[
                        {"label": "Rural", "value": "rural"},
                        {"label": "Urban", "value": "urban"},
                        {"label": "Suburban", "value": "suburban"}
                    ],
                    value="rural",
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

            html.Div([
                html.Label("Select Pollutants"),
                dcc.Dropdown(
                    id="location_source-dropdown-2",
                    options=[
                        {"label": "Background", "value": "background"},
                        {"label": "Traffic", "value": "traffic"},
                        {"label": "Industry", "value": "industrie"}
                    ],
                    value=["background"],
                    multi=True,
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

        ], style={
            "display": "flex",
            "gap": "40px",
            "margin": "30px 30px 0px 30px"
        }),

        html.Div([
            # Graph
            dcc.Graph(id="location_pollution-graph-2" , style={"width": "100%"}),
        ], style={
                "display": "flex",
                "gap": "20px",
                }),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "75px auto 75px auto",
                }),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "TODO"
        ],style={"margin": "10px 30px 10px 30px"})
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "75px auto 75px auto",
                }),

])

#################
### Callbacks ###
#################

@callback(
    Output("location_pollution-graph", "figure"),
    Input("location_time-dropdown", "value"),
    Input("location_area-dropdown", "value")
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
        title="Air quality over the last 10 years for PM\u2081\u2080",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig

@callback(
    Output("location_pollution-graph-2", "figure"),
    Input("location_area-dropdown-2", "value"),
    Input("location_source-dropdown-2", "value")
)
def update_graph_2(time_period, pollutants):

    fig = go.Figure()

    for p in pollutants:
        df = data2[time_period][p]

        fig.add_trace(
            go.Bar(
                x=df["date start"],
                y=df["value"],
                name=p
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
                    name=p + " trend",
                )
            )

    fig.update_layout(
        title="Air quality over the last 10 years for PM\u2081\u2080",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig