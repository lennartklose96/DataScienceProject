import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Order of the months in the year
MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅

###############
### Styling ###
###############

###########################
### Initialize Dash app ###
###########################

# Initialize Dash page
dash.register_page(__name__)

###########################
### Loading data frames ###
###########################

# Average of german states
df_country = {
    "daily" : pd.read_csv("Collected Data/Question 2/States_Daily_Data.csv"),
    "monthly" : pd.read_csv("Collected Data/Question 2/States_Monthly_Data.csv"),
    "yearly" : pd.read_csv("Collected Data/Question 2/States_Yearly_Data.csv"),
}
# Average of holidays per state
df_holidays = {
    "daily" : pd.read_csv("Collected Data/Question 7/SummerHolidaysState_Daily_Data.csv"),
    "yearly" : pd.read_csv("Collected Data/Question 7/SummerHolidaysState_Yearly_Data.csv")
}

# Merge holiday and overall yearly data on state and year
df_diff = df_holidays["yearly"].merge(
    df_country["yearly"],
    on=["state", "year"],
    suffixes=("_holiday", "_all")
)

# Drop irrelevant column
df_diff = df_diff.drop(columns="no2")

# Compute differences with nice labels
df_diff["PM10"] = df_diff["pm10_holiday"] - df_diff["pm10_all"]
df_diff["PM2.5"] = df_diff["pm25_holiday"] - df_diff["pm25_all"]


##################
### App layout ###
##################

layout = html.Div([

    
    html.Div([
    # Title
    #html.H2([
    #    "Summer Holidays and Air Pollution"
    #]),

    # Research question
    html.Div([
            #html.H3("Research Question"),
            # The actual question
            html.H4([
                "How did summer school holidays in German federal states affect ",
                html.Span(["PM", html.Sub("10")]),
                " and ",
                html.Span(["PM", html.Sub("2.5")]),
                " concentrations over the past ten years?"
            ], style={
                "font-size": "30px"
            }),
            # Description of why it is interesting and relevant
            html.P([
                "Traffic is one of the main sources of particulate matter in urban areas. "
                "During summer school holidays, many families tend to go on vacation "
                "and traffic patterns change. To determine how this affects the ",
                html.Span(["PM", html.Sub("10")]),
                " and ",
                html.Span(["PM", html.Sub("2.5")]),
                " concentrations, we compared the mean of each state during the summer holidays "
                "to their yearly mean."
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Data description
        html.Div([
            html.H6([
                "Used Data"
            ]),
            html.P([
                "We used daily pollution data provided by the Umweltbundesamt API for ",
                html.Span(["PM", html.Sub("10")]),
                " and ",
                html.Span(["PM", html.Sub("2.5")]),
                "and additionally found out when the summer school holidays are via ",
                html.A("https://www.schulferien.org/"),
                " to make comparisons."
            ]),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H6([
                "Visualization"
            ]),
            html.P([
                "This visualization shows how particulate matter concentrations in each state "
                "differ during summer holidays compared to the yearly average."
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
        # Controls
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="holiday_year-dropdown",
                options=[
                    {"label": y, "value": y}
                    for y in sorted(df_diff["year"].unique())
                ],
                value=sorted(df_diff["year"].unique())[0],
                clearable=False,
                searchable=False
            ),
        ], style={
            "width": "250px",
            "margin-bottom": "20px",
            "margin": "30px 30px 0px 30px"
        }),

        html.Div([
            # Visualization
            dcc.Graph(id="holiday_heatmap-matrix" , style={"width": "100%"}),
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

    # Explanation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([
          "In the vast majority of years in most states, we can see the difference is negative. "
          "This heavily implies the summer holidays have a positive impact on air pollution in Germany. "
          "A likely cause for this is that a lot of families going on vacation end up having fewer daily "
          "commutes (for example, to bring their children to school), or leave the country entirely."
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
    Output("holiday_heatmap-matrix", "figure"),
    Input("holiday_year-dropdown", "value")
)

def update_heatmap(selected_year):
    # Filter by year
    df_year = df_diff[df_diff["year"] == selected_year]

    # Prepare matrix: rows = pollutant, columns = state
    matrix_values = df_year.set_index("state")[["PM10", "PM2.5"]].round(2)

    # Text matrix: show numbers, "No data" for NaN
    text_matrix = matrix_values.astype(object).where(~matrix_values.isna(), "No data")

    # Replace y-axis labels with proper notation + units
    pollutant_labels = [
        "PM\u2081\u2080",  # PM10
        "PM\u2082.\u2085"  # PM2.5
    ]

    # Build heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix_values.T.values,
        x=matrix_values.index,      # states
        y=pollutant_labels,         # use proper notation
        text=text_matrix.T.values,
        texttemplate="%{text}",
        colorscale="RdBu_r",
        zmin=-5,
        zmax=5,
        zmid=0,
        hovertemplate="State: %{x}<br>Pollutant: %{y}<br>Difference: %{z} µg/m³<extra></extra>",
        showscale=True,
        colorbar=dict(title="Difference (µg/m³)")
    ))

    # Layout
    fig.update_layout(
        template="plotly_white",
        title=f"Difference in pollution during the summer holidays per state compared to their yearly mean [{selected_year}]",
        yaxis_title="Pollutant"
    )

    return fig