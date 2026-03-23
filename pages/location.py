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
PM10_LABEL = "PM\u2081\u2080"
PM25_LABEL = "PM\u2082.\u2085"
NO2_LABEL = "NO\u2082"

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
        "industry": pd.read_csv("Collected Data/Question 3.1/monthly_avg_ländlich_industrie_PM10.csv"),
    },
    "urban": {
        "background": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_hintergrund_PM10.csv"),
        "traffic": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_verkehr_PM10.csv"),
        "industry": pd.read_csv("Collected Data/Question 3.1/monthly_avg_städtisch_industrie_PM10.csv"),
    },
    "suburban": {
        "background": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_hintergrund_PM10.csv"),
        "traffic": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_verkehr_PM10.csv"),
        "industry": pd.read_csv("Collected Data/Question 3.1/monthly_avg_vorstädtisch_industrie_PM10.csv"),
    }
}

AREA_MAP = {"rural": "Rural", "urban": "Urban", "suburban": "Suburban"}

# Convert to a valid time format

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
    
    ######################
    ### First question ###
    ######################

    # Research question
    html.Div([
        html.Div([
            html.H4([
                "How does air pollution for " + PM10_LABEL +  " vary across urban, suburban and rural areas?"
            ], style={
                "font-size": "30px"
            }),
            html.P([
                "Urban areas are naturally more populated than suburban and rural areas. On the other hand, "
                "rural areas typically have agricultural emissions that might affect the air quality. To find out "
                "the differences in pollution we compared data based on the monitoring station's location."
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H4("Used Data"),
            html.P([
                "Daily air quality data for " + PM10_LABEL +  " was obtained from the Umweltbundesamt "
                "API. For this process, each station had an attribute, that specified "
                "in what kind of location the station is in - urban, suburban or rural. The data "
                "was then aggregated into daily and monthly means for each of the different locations."
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H4("Visualization"),
            html.P([
                "This visualization shows daily or monthly values for the past ten years for " + PM10_LABEL +
                " based on the chosen location type. Additionally it also displays the trend line."
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

    # Visualization
    html.Div([
        # Controls (time period + area type)
        html.Div([

            # Time period
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

            # Location type
            html.Div([
                html.Label("Select Location Type"),
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

        # Graph
        html.Div([
            dcc.Graph(id="location_pollution-graph" , style={"width": "100%"}),
        ], style={"display": "flex","gap": "20px",}),
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
            "The different station types vary in intensity exactly like we expected them to. The more populated "
            "areas have a higher amount of concentration, meaning that the population amount does contribute to "
            "the amount of air pollution. The lines all follow the same pattern, indicating that pollution patterns "
            "are consistent between different location types."
        ],style={"margin": "10px 30px 10px 30px","font-size": "18px"})
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

    #######################
    ### Second question ###
    #######################

    # Research question
    html.Div([
        html.Div([
            html.H4([
                "How does air pollution for " + PM10_LABEL + " vary between background, "\
                "traffic and industrial monitoring stations?"
            ], style={
                "font-size": "30px"
            }),
            html.P([
                "Different areas in the country contribute differently to air pollution. "\
                "To find out just how intense those differences "
                "are, we checked different station locations. For this we examined stations "\
                "located near roads, near the industrial areas "
                "and in background environmental areas with low population and traffic. "
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H4("Used Data"),
            html.P([
                "Daily air quality data for " + PM10_LABEL +  " was obtained from the Umweltbundesamt "
                "API. For this process, each station had an attribute, that specified "
                "what kind of station type collected the data. Those types included industry, traffic and "
                "background monitoring stations. Additionally, we also filtered for the location once again. The data "
                "was then aggregated monthly means for each of the different station types and locations."
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H4("Visualization"),
            html.P([
                "This visualization shows monthly values for the past ten years for " + PM10_LABEL +
                " based on the chosen station types and the location. Additionally it also displays the trend line."
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

    # Visualization
    html.Div([
        # Controls
        html.Div([

            # Location type
            html.Div([
                html.Label("Select Location Type"),
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

            # Station type 
            html.Div([
                html.Label("Select Station Type"),
                dcc.Dropdown(
                    id="location_source-dropdown-2",
                    options=[
                        {"label": "Background", "value": "background"},
                        {"label": "Traffic", "value": "traffic"},
                        {"label": "Industry", "value": "industry"}
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
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 25px auto",
                }),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "Overall, across all different location types, the industry and traffic monitoring stations "
            "shows a significantly higher amount of " + PM10_LABEL + " concentration. This aligns with out intiial "
            "expectations, although traffic and industry are somewhat close when it comes to pollution. This shows "
            "just how much of an impact big production factories and car traffic have an effect on our air quality."
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

######################
### First question ###
######################

@callback(
    Output("location_pollution-graph", "figure"),
    Input("location_time-dropdown", "value"),
    Input("location_area-dropdown", "value")
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
                name=AREA_MAP[p]
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

            # Confidence Interval
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
                    name=f"{AREA_MAP[p]} trend<br>"
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
                    name=f"{AREA_MAP[p]} CI <br>"
                )
            )


    fig.update_layout(
        title="Air quality over the last 10 years for PM\u2081\u2080",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig


#######################
### Second question ###
#######################

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
                name=p,
                showlegend=True,
            )
        )

    fig.update_layout(
        title="Air quality over the last 10 years for PM\u2081\u2080",
        xaxis_title="Date",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig