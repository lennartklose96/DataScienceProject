import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Order of the months in the year
MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
# ORder of the seasons in the year
SEASONS_ORDER = ["Spring", "Summer", "Fall", "Winter"]

###############
### Styling ###
###############

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

###########################
### Loading data frames ###
###########################

df_spring = pd.read_csv("../Collected Data/Question 4/daily_avg_spring_PM10.csv")
df_summer = pd.read_csv("../Collected Data/Question 4/daily_avg_summer_PM10.csv")
df_fall = pd.read_csv("../Collected Data/Question 4/daily_avg_fall_PM10.csv")
df_winter = pd.read_csv("../Collected Data/Question 4/daily_avg_winter_PM10.csv")

# Add season column to each dataframe
df_spring["season"] = "Spring"
df_summer["season"] = "Summer"
df_fall["season"] = "Fall"
df_winter["season"] = "Winter"

# Combine them
df_pollution = pd.concat([df_spring, df_summer, df_fall, df_winter])



# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

##################
### App layout ###
##################

app.layout = html.Div([
    
    ###############
    ### Seasons ###
    ###############
    
    html.H2("Seasons"),
    html.Div([
        html.Div([
            html.H4("Select Year:"),
            dcc.Dropdown(
                id="season-year-dropdown",
                options=[{"label": y, "value": y} for y in sorted(df_pollution["year"].unique())],
                value=df_pollution["year"].unique()[0],
                clearable=False
            ),
        ], style={"width": "200px", "display": "inline-block", "margin-right": "20px"}),
    ]),
    html.Div(dcc.Graph(id="season-pie"))
])

#################
### Callbacks ###
#################

###############
### Seasons ###
###############

@callback(
    Output("season-pie", "figure"),
    Input("season-year-dropdown", "value")
)
def update_pie(selected_year):

    df_year = df_pollution[df_pollution["year"] == selected_year]

    # Sum pollution per season
    df_grouped = df_year.groupby("season")[["pm10","pm25"]].mean().reset_index()

    # Combine pm10 + pm25 if you want total pollution
    df_grouped["pollution_total"] = df_grouped["pm10"] + df_grouped["pm25"]

    fig = px.pie(
        df_grouped,
        values="pollution_total",
        names="season",
        title=f"Pollution Distribution by Season ({selected_year})",
        category_orders={"season": SEASONS_ORDER}
    )

    fig.update_layout(title_x=0.5)

    return fig

if __name__ == "__main__":
    app.run(debug=True)