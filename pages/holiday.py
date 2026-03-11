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
    html.H2("Summer Holidays"),

    html.Div([
        html.H4("Select Year:"),
        dcc.Dropdown(
            id="holiday_year-dropdown",
            options=[{"label": y, "value": y} for y in sorted(df_diff["year"].unique())],
            value=sorted(df_diff["year"].unique())[0],
            clearable=False,
            searchable = False
        ),
    ], style={"width": "200px", "display": "inline-block", "margin-right": "20px"}),

    dcc.Graph(id="holiday_heatmap-matrix")
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

    # Create matrix: rows = pollutant, columns = state
    matrix = df_year.set_index("state")[["PM10", "PM2.5"]].T
    # Round values for display
    matrix = matrix.round(2)

    # Prepare matrix
    matrix_values = df_year.set_index("state")[["PM10", "PM2.5"]].round(2)
   
    # Create text matrix: show numbers, "No data" for NaN
    text_matrix = matrix_values.astype(object)
    text_matrix = text_matrix.where(~matrix_values.isna(), "No data")
    
    # Build heatmap with go.Heatmap
    # Build heatmap with states on x, pollutants on y
    fig = go.Figure(data=go.Heatmap(
        z=matrix_values.T.values,
        x=matrix_values.index,      # states
        y=matrix_values.columns,    # pollutants
        text=text_matrix.T.values,
        texttemplate="%{text}",
        colorscale="RdBu_r",
        zmin=-5,
        zmax=5,
        hovertemplate="State: %{x}<br>Pollutant: %{y}<br>Difference: %{z}<extra></extra>",
        showscale=True,
        zmid=0,
        colorbar=dict(title="Difference")
    ))

    fig.update_layout(
        template="plotly_white",
        title=f"Difference in pollution during the summer holidays per state [{selected_year}]"
    )

    return fig