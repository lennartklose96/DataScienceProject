import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

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

# The yearly average in germany
yearly_data = {
    "PM10": pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM10.csv"),
    "PM25": pd.read_csv("Collected Data/Question 1/yearly_avg_deutschland_PM2,5.csv"),
}
df_yearly = pd.merge(yearly_data["PM10"], yearly_data["PM25"], on="date start")
df_yearly = df_yearly.rename(columns={"date start": "date"})



##################
### App layout ###
##################

layout = html.Div([
    # Page title
    html.H2("PM10 Seasonal Analysis"),
    # Year dropdown
    html.Div([
        html.H4("Select Year:"),
        dcc.Dropdown(
            id="seasons_year-dropdown",
            options=[{"label": y, "value": y} for y in sorted(df_grouped_year["year"].unique())],
            value=df_grouped_year["year"].unique()[0],
            clearable=False,
            searchable=False
        )
    ], style={"width": "200px", "margin-bottom": "20px"}),
    # Two charts side by side
    html.Div([
        dcc.Graph(id="seasons_bar", style={"width": "48%"}),
        dcc.Graph(id="seasons_pie", style={"width": "48%"})
    ], style={"display": "flex", "justify-content": "space-between"})
])

#################
### Callbacks ###
#################

