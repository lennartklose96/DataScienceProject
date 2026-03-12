import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Labels for pollutants
PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅
NO2_LABEL = "NO\u2082"          # NO₂

LABEL_MAP = {
    "PM10": PM10_LABEL,
    "PM2.5": PM25_LABEL,
    "NO2": NO2_LABEL
}


###########################
### Initialize Dash app ###
###########################

# Initialize Dash page
dash.register_page(__name__)

###########################
### Loading data frames ###
###########################

data_corona = {
    "daily": {
        "PM10": pd.read_csv("Collected Data/Question 1.1/corona_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1.1/corona_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1.1/corona_NO2.csv")
    },
    "monthly": {
        "PM10": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1.1/monthly_avg_corona_NO2.csv")
    }
}

data_germany = {
    "daily": {
        "PM10": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1/daily_avg_deutschland_NO2.csv")
    },
    "monthly": {
        "PM10": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_PM10.csv"),
        "PM2.5": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_PM2,5.csv"),
        "NO2": pd.read_csv("Collected Data/Question 1/monthly_avg_deutschland_NO2.csv")
    }
}

# Converting to datetime
for dataset in [data_corona, data_germany]:
    for period in dataset.values():
        for df in period.values():
            df["date start"] = pd.to_datetime(df["date start"])

# Building no corona df
data_no_corona = {
    "daily": {},
    "monthly": {}
}

for period in ["daily", "monthly"]:
    for p in ["PM10", "PM2.5", "NO2"]:

        germany_df = data_germany[period][p]
        covid_df = data_corona[period][p]

        non_covid_df = germany_df[
            ~germany_df["date start"].isin(covid_df["date start"])
        ].copy()

        data_no_corona[period][p] = non_covid_df


pollutants={"PM10","PM2.5","NO2"}

##################
### App layout ###
##################

layout = html.Div([

    # Title
    html.H2("COVID-19 and Air Pollution"),

    # Research question
    html.Div([
        html.H3("Research Question"),
        # The actual question
        html.H4([
            "How did COVID-19 lockdowns and restrictions affect air pollution in Germany? "
        ]),
        # Description of why it is interesting and relevant
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

    # Controls (time period + pollutants)
    html.Div([

        html.Div([
            html.Label("Select Time Period"),
            dcc.Dropdown(
                id="corona_time-dropdown",
                options=[
                    {"label": "Daily", "value": "daily"},
                    {"label": "Monthly", "value": "monthly"},
                ],
                value="daily",
                clearable=False,
                searchable=False,
                style={"width": "200px"}
            ),
        ]),

        html.Div([
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
                searchable=False,
                style={"width": "200px"}
            ),
        ]),

    ], style={
        "display": "flex",
        "gap": "40px",
        "margin-bottom": "20px"
    }),

    # Visualizations side by side
    html.Div([
        dcc.Graph(id="corona_pollution-graph", style={"width": "50%"}),
        dcc.Graph(id="corona_boxplot-graph", style={"width": "50%"})
    ], style={
        "display": "flex",
        "gap": "20px"
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

#################
### Callbacks ###
#################

@callback(
    Output("corona_pollution-graph", "figure"),
    Output("corona_boxplot-graph", "figure"),
    Input("corona_time-dropdown", "value"),
    Input("corona_pollutant-dropdown", "value")
)
def update_graph(time_period, pollutants):

    # Line plot
    fig = go.Figure()

    for p in pollutants:
        df = data_corona[time_period][p]

        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="lines",
                name=LABEL_MAP[p]
            )
        )

    for p in pollutants:
        df = data_corona[time_period][p]
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
                    name=LABEL_MAP[p] + " trend",
                )
            )

    fig.update_layout(
        title="Air quality during the coronavirus pandemic",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    # Build dataset for boxplot
    box_data = []

    for p in pollutants:

        covid_df = data_corona[time_period][p].copy()
        non_covid_df = data_no_corona[time_period][p].copy()

        covid_df["period"] = "COVID"
        non_covid_df["period"] = "Non-COVID"

        covid_df["pollutant"] = p
        non_covid_df["pollutant"] = p

        box_data.append(covid_df)
        box_data.append(non_covid_df)

    box_df = pd.concat(box_data)
    # Add labels
    box_df["pollutant"] = box_df["pollutant"].map(LABEL_MAP)

    box_fig = px.box(
        box_df,
        x="pollutant",
        y="value",
        color="period",
        boxmode="group",
        points="outliers"
    )

    box_fig.update_layout(
        title="Comparing the pollution during COVID-19 to the prior and following years",
        xaxis_title="Pollutant",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig, box_fig