from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import numpy as np


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

data2 = {
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


for period in data2.values():           # daily, monthly, yearly
    for df in period.values():        # PM10, PM2.5, NO2
        df["date start"] = pd.to_datetime(df["date start"])

pollutants={"PM10","PM2.5","NO2"}

app = Dash(__name__)

app.layout = html.Div([

    html.H1("Air Pollution Germany"),

    html.Label("Select Time Period"),
    dcc.Dropdown(
        id="time-dropdown",
        options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Monthly", "value": "monthly"},
            {"label": "Yearly", "value": "yearly"}
        ],
        value="daily",
        clearable=False,
    ),

    html.Br(),

    html.Label("Select Pollutants"),
    dcc.Dropdown(
        id="pollutant-dropdown",
        options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2.5"},
            {"label": "NO\u2082", "value": "NO2"}
        ],
        value=["PM10"],
        multi=True,
        clearable=False
    ),

    dcc.Graph(id="pollution-graph"),

    html.Hr(),

    html.H1("Air Pollution Germany"),

    html.Label("Select Time Period"),
    dcc.Dropdown(
        id="time-dropdown-2",
        options=[
            {"label": "Daily", "value": "daily"},
            {"label": "Monthly", "value": "monthly"},
            {"label": "Yearly", "value": "yearly"}
        ],
        value="monthly",
        clearable=False,
    ),

    html.Br(),

    html.Label("Select Pollutants"),
    dcc.Dropdown(
        id="pollutant-dropdown-2",
        options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2.5"},
            {"label": "NO\u2082", "value": "NO2"}
        ],
        value=["PM10"],
        multi=True,
        clearable=False
    ),

    dcc.Graph(id="pollution-graph-2")

])


@callback(
    Output("pollution-graph", "figure"),
    Input("time-dropdown", "value"),
    Input("pollutant-dropdown", "value")
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

    fig.update_layout(
        title="Air quality over the last 10 years",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)",
        showlegend=False
    )

    return fig

@callback(
    Output("pollution-graph-2", "figure"),
    Input("time-dropdown-2", "value"),
    Input("pollutant-dropdown-2", "value")
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
        title="Air quality over the last 10 years",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)",
        showlegend=False
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)