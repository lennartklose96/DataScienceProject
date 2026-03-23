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

    html.Div([
        # Title
        #html.H2("COVID-19 and Air Pollution", style={
            #    "font-size": "30px"
            #}),

        # Research question
        html.Div([
            #html.H3("Research Question"),
            # The actual question
            html.H4([
                "How did COVID-19 lockdowns and restrictions affect air pollution in Germany "
                "compared to the previous and following years? "
            ], style={
                "font-size": "30px"
            }),
            # Description of why it is interesting and relevant
            html.P([
            "The COVID-19 pandemic led to major changes in daily life, including lockdowns, "
            "reduced traffic, and decreased industrial activity. These changes created a "
            "unique opportunity to analyze how human activity influences air pollution "
            "levels. Investigating the relationship between COVID-19 restrictions and "
            "air quality can help better understand the impact of human behavior on "
            "environmental conditions.",
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H4("Used Data"),
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
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H4("Visualization"),
            html.P([
            "The graph shows the daily and annual PM\u2081\u2080, PM\u2082.\u2085, and NO₂ values from 2019 to "
            "the end of 2021 and their corresponding regression lines. "
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

    html.Div([
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
                "margin": "30px 30px 0px 30px"

            }),

            # Visualizations side by side
            html.Div([
                dcc.Graph(id="corona_pollution-graph", style={"width": "49%"}),
                dcc.Graph(id="corona_boxplot-graph", style={"width": "49%"})
            ], style={
                "display": "flex",
                "gap": "20px"
            }),
        ]),
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
            "The graph suggests a slight decrease in PM\u2081\u2080, PM\u2082.\u2085, and NO₂ concentrations around"
            " the beginning of the COVID-19 pandemic in 2020. This may be related to lockdown "
            "measures that reduced traffic and economic activity. However, the effect "
            "appears moderate, and pollution levels show strong daily fluctuations, "
            "indicating that additional factors such as weather conditions also influence "
            "air quality."
        ],style={"margin": "10px 30px 10px 30px", "font-size": "18px"})
    ], style={
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

            # plot
            fig.add_trace(
                go.Scatter(
                    x=df["date start"],
                    y=y_pred,
                    mode="lines",
                    name=f"{LABEL_MAP[p]} trend<br>"
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
                    name=f"{LABEL_MAP[p]} CI <br>"
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