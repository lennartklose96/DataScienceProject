import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#################
### Constants ###
#################

PM10_LABEL = "PM\u2081\u2080"
PM25_LABEL = "PM\u2082.\u2085"
NO2_LABEL = "NO\u2082"

# Dictionary for labels per pollutant
POLLUTANT_LABELS = {
    "PM10": PM10_LABEL,
    "PM2.5": PM25_LABEL,
    "NO2":  NO2_LABEL
}

###############
### Styling ###
###############

# For the main container divs
div_margin = {
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "40px auto 75px auto",
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

# Available years
years = sorted(data["PM10"]["date start"].dt.year.unique())

# Getting data from january first
jan1_data = {}

for name, df in data.items():
    jan1_data[name] = df[
        (df["date start"].dt.month == 1) &
        (df["date start"].dt.day == 1)
    ]

##################
### App layout ###
##################

layout = html.Div([

    html.Div([
        # Title
        #html.H2("Pollution during New Years"),

        # Research question
        html.Div([
            #html.H3("Research Question"),
            html.H4([
                "How does air pollution in Germany behave around New Years?"
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
    ], style=div_margin),

    html.Div([
        # Controls
        html.Div([

            html.Div([
                html.Label("Select Pollutants"),
                dcc.Dropdown(
                    id="newyears_pollutant-dropdown",
                    options=[
                        {"label": POLLUTANT_LABELS["PM10"], "value": "PM10"},
                        {"label": POLLUTANT_LABELS["PM2.5"], "value": "PM2.5"},
                        {"label": POLLUTANT_LABELS["NO2"], "value": "NO2"},
                    ],
                    value=["PM10"],
                    multi=True,
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

            html.Div([
                html.Label("Select Yearly Averages"),
                dcc.Dropdown(
                    id="newyears_avg-dropdown",
                    options=[
                        {"label": POLLUTANT_LABELS["PM10"] + " yearly average", "value": "PM10yearly"},
                        {"label": POLLUTANT_LABELS["PM2.5"] + " yearly average", "value": "PM2.5yearly"},
                        {"label": POLLUTANT_LABELS["NO2"]  + " yearly average", "value": "NO2yearly"}
                    ],
                    value=[],
                    multi=True,
                    clearable=True,
                    searchable=False,
                    style={"width": "200px"}
                ),
            ]),

        ], style={"display": "flex", "gap": "40px", "margin": "30px 30px 0px 30px"}),

        # Graphs
        html.Div([
            dcc.Graph(id="newyears_pollutant-graph", style={"width": "100%"}),
        ], style={
                "display": "flex",
                "gap": "20px",
                }),
    ], style=div_margin),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "TODO"
        ],style={"margin": "10px 30px 10px 30px"})
    ],style=div_margin),

    ####################
    ### Second graph ###
    ####################

    html.Div([
        # Controls
        html.Div([
            html.Div([
                html.Label("Select year"),
                dcc.Dropdown(
                    id="newyears_year-select",
                    options=[{"label": str(y), "value": y} for y in years],
                    value= years[0],
                    clearable=False,
                    searchable=False,
                    style={"width": "200px"}
                ),
            
            ]),
        ], style={"display": "flex", "gap": "40px", "margin": "30px 30px 0px 30px"}),

        # Graphs
        html.Div([
            dcc.Graph(id="newyears_comparison-graph", style={"width": "100%"}),
        ], style={
                "display": "flex",
                "gap": "20px",
                }),
    ], style=div_margin),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
            "TODO"
        ],style={"margin": "10px 30px 10px 30px"})
    ],style=div_margin)
])

#################
### Callbacks ###
#################

# -----------
# Scatterplot
# -----------

@callback(
    Output("newyears_pollutant-graph", "figure"),
    Input("newyears_pollutant-dropdown", "value"),
    Input("newyears_avg-dropdown", "value")
)
def update_graph(selected_pollutants, selected_averages):
    fig = go.Figure()

    # Plot daily/individual pollutants
    for name in selected_pollutants:
        df = data[name]
        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="markers",
                name=POLLUTANT_LABELS[name]
            )
        )
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
                    name=POLLUTANT_LABELS[name] + " trend"
                )
            )

    # Plot yearly averages with proper label
    for name in selected_averages:
        df = data[name]
        # Map "PM10yearly" -> "PM10", etc. for the label
        pollutant_key = name.replace("yearly", "")
        label = POLLUTANT_LABELS[pollutant_key] + " yearly average"
        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="lines+markers",
                name=label
            )
        )

    fig.update_layout(
        title="Pollution in Germany during New Years",
        xaxis_title="Year",
        yaxis_title="Concentration (µg/m³)",
        hovermode="closest"
    )

    return fig


# ---------
# Bar chart
# ---------

@callback(
    Output("newyears_comparison-graph", "figure"),
    Input("newyears_year-select", "value")
)

def update_graph_2(selected_year):

    # Pollutants
    pollutants = ["PM10", "PM2.5", "NO2"]

    jan_values = []
    yearly_values = []
    labels = []

    # Getting the relevant data
    for pollutant in pollutants:

        jan_df = jan1_data[pollutant]
        jan_val = jan_df[jan_df["date start"].dt.year == selected_year]["value"].mean()

        yearly_df = data[pollutant + "yearly"]
        yearly_val = yearly_df[yearly_df["date start"].dt.year == selected_year]["value"].mean()

        jan_values.append(jan_val)
        yearly_values.append(yearly_val)
        labels.append(POLLUTANT_LABELS[pollutant])

    # Creating figure
    fig = go.Figure()

    # Adding labels
    fig.add_trace(go.Bar(
        x=labels,
        y=jan_values,
        name="January 1st"
    ))

    fig.add_trace(go.Bar(
        x=labels,
        y=yearly_values,
        name="Yearly average"
    ))

    # Updating more labels and title
    fig.update_layout(
        title=f"January 1 vs Yearly Average Pollution [{selected_year}]",
        yaxis_title="Concentration (µg/m³)",
        barmode="group"
    )

    return fig