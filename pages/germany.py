import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression

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

# Creating yearly columns for the pollutants
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
    # Research question
    html.Div([
        html.Div([
            html.H4([
                "How did the average values of PM₁₀, PM₂.₅ and NO₂ change in Germany?"
            ], style={
                "font-size": "30px"
            }),
            html.P([
            "Our world is ever-changing. As such it would also make sense that the concentration of air pollution "
            "has been changing over the past ten years. In this question, we want to see how the concentration "
            "has changed and developed, and what could be attributed to this change."
              
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H4("Used Data"),
            html.P([
                "Daily air quality data for the pollutants were obtained "
                "from the Umweltbundesamt API. The data was aggregated "
                "into daily, monthly and yearly means to facilitate comparisons."
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H4("Visualization"),
            html.P([
            "The visualization shows the mean pollution across all monitoring stations in Germany "
            "for the past ten years. Daily, monthly and yearly intervals can be chosen. "
            "A trend line also shows how the concenctration of pollution has developed."
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 10px 30px"}),

    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 25px auto",
                }),
                
    # Layout for the visualization
    html.Div([
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
        ], style={"display": "flex", "align-items": "left", "margin": "30px 30px 0px 30px", "gap" : "40px"}),

        html.Div([
            # Graph
            dcc.Graph(id="Q10_pollution-graph", style={"width": "100%"}),
        ], style={
                "display": "flex",
                "gap": "20px"
                }),
    # Style for the visualization section
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 25px auto",
                }),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "We can see that while the pollution for fine dust particles remains fairly "
            "constant, there is a small declining trend visible. For " + NO2_LABEL +
            " specifically however, there is a strong downwards trend, indicating "
            "that the overall air quality has been increasing over the past 10 years." 
            "One cause for this could be a general push for environmental awareness and "
            "concious decisionmaking that improves our overall air quality."
        ],style={"margin": "10px 30px 10px 30px", "font-size": "18px"})
    ],style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 0px auto",
                }),

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

        # Bars
        fig.add_trace(
            go.Bar(
                x=df["date start"],
                y=df["value"],
                name=POLLUTANT_LABELS[p]
            )
        )

        # Regression
        if len(df) > 1:

            # prepare X
            X_raw = df["date start"].map(pd.Timestamp.toordinal).values
            X = (X_raw - X_raw.min()).reshape(-1, 1)
            y = df["value"].values

            # modell
            model = LinearRegression()
            model.fit(X, y)

            # prediction
            y_pred = model.predict(X)

            # coefficients
            slope = model.coef_[0]
            intercept = model.intercept_

            if time_period == "daily":
                factor = 1
                unit = "day"

            elif time_period == "monthly":
                factor = 30
                unit = "month"

            elif time_period == "yearly":
                factor = 365
                unit = "year"

            slope_adjusted = slope * factor

            # confidence interval
            n = len(y)
            y_mean = np.mean(y)
            residuals = y - y_pred

            # standard error
            s_err = np.sqrt(np.sum(residuals**2) / (n - 2))

            # t-Value (95% CI)
            t_val = stats.t.ppf(0.975, df=n-2)

            # Calculate the confidence interval
            x_mean = np.mean(X)
            conf = t_val * s_err * np.sqrt(
                1/n + (X - x_mean)**2 / np.sum((X - x_mean)**2)
            )

            upper = y_pred + conf.flatten()
            lower = y_pred - conf.flatten()

            # Plot
            fig.add_trace(
                go.Scatter(
                    x=df["date start"],
                    y=y_pred,
                    mode="lines",
                    name=f"{POLLUTANT_LABELS[p]} trend<br>"
                    f"(slope={slope_adjusted:.4f}, CI≈[{lower.mean():.2f},{upper.mean():.2f}])",
                    line=dict(width=3)
                )
            )

            # Confidence Band
            fig.add_trace(
                go.Scatter(
                    x=list(df["date start"]) + list(df["date start"][::-1]),
                    y=list(upper) + list(lower[::-1]),
                    fill="toself",
                    fillcolor="rgba(0,0,0,0.1)",
                    line=dict(color="rgba(255,255,255,0)"),
                    hoverinfo="skip",
                    showlegend=True,
                    name=f"{POLLUTANT_LABELS[p]} CI <br>"
                )
            )

    fig.update_layout(
        title="Air quality in Germany over the last 10 years",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig