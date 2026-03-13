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
            "How did COVID-19 lockdowns and restrictions affect air pollution in Germany "
            "compared to the previous and following years? "
        ]),
        # Description of why it is interesting and relevant
        html.P([
           "The COVID-19 pandemic led to major changes in daily life, including lockdowns, "
           "reduced traffic, and decreased industrial activity. These changes created a "
           "unique opportunity to analyze how human activity influences air pollution "
           "levels. Investigating the relationship between COVID-19 restrictions and "
           "air quality can help better understand the impact of human behavior on "
           "environmental conditions."
        ]),
    ]),

    # Data description
    html.Div([
        html.H6("Used Data"),
        html.P([
            "This study uses publicly available air quality data provided by the German "
            "Environment Agency (Umweltbundesamt). The dataset includes measurements of "
            "key air pollutants such as PM\u2081\u2080, PM\u2082.\u2085, and NO₂ collected from monitoring "
            "stations across Germany. To analyze trends over time, the data was aggregated "
            "into daily, monthly, and yearly averages. Each dataset contains a timestamp "
            "(date start) and the corresponding pollutant concentration value in µg/m³. "
            "These datasets enable the analysis of temporal changes in air pollution levels "
            "and allow comparisons between different time periods, including the COVID-19 "
            "pandemic."
        ]),
    ]),

    # Visualization description
    html.Div([
        html.H6("Visualization"),
        html.P([
           "The graph shows the daily and annual PM\u2081\u2080, PM\u2082.\u2085, and NO₂ values from 2019 to "
           "the end of 2021 and their corresponding regression lines. "
        ]),
    ]),

    html.Hr(),
    html.Div([
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
            "margin-bottom": "20px",

        }),

        # Visualizations side by side
        html.Div([
            dcc.Graph(id="corona_pollution-graph", style={"width": "50%"}),
            dcc.Graph(id="corona_boxplot-graph", style={"width": "50%"})
        ], style={
            "display": "flex",
            "gap": "20px",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)"
        }),
    ]),

    html.Hr(),

    # Interpretation
    html.Div([
        html.H4("Interpretation"),
        html.P([
            "The graph suggests a slight decrease in PM\u2081\u2080, PM\u2082.\u2085, and NO₂ concentrations around"
            " the beginning of the COVID-19 pandemic in 2020. This may be related to lockdown "
            "measures that reduced traffic and economic activity. However, the effect "
            "appears moderate, and pollution levels show strong daily fluctuations, "
            "indicating that additional factors such as weather conditions also influence "
            "air quality."
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