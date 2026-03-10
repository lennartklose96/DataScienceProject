import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Order of the months in the year
MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
# Order of the seasons in the year
SEASONS_ORDER = ["Spring", "Summer", "Fall", "Winter"]

###############
### Styling ###
###############

# Define colors for each season
season_colors = {
    "Spring": "#98E221",  # DeepSkyBlue
    "Summer": "#FFEB3C",  # Gold
    "Fall":   "#F3A32B",  # DarkOrange
    "Winter": "#65B2FA"   # DodgerBlue
}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

###########################
### Initialize Dash app ###
###########################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

###########################
### Loading data frames ###
###########################

# Loading .csv
df_spring = pd.read_csv("Collected Data/Question 4/daily_avg_spring_PM10.csv")
df_summer = pd.read_csv("Collected Data/Question 4/daily_avg_summer_PM10.csv")
df_fall = pd.read_csv("Collected Data/Question 4/daily_avg_fall_PM10.csv")
df_winter = pd.read_csv("Collected Data/Question 4/daily_avg_winter_PM10.csv")

# Adding seasons
df_spring["season"] = "Spring"
df_summer["season"] = "Summer"
df_fall["season"] = "Fall"
df_winter["season"] = "Winter"

# Combining to singular df
df_seasons = pd.concat([df_spring, df_summer, df_fall, df_winter])
df_seasons["date"] = pd.to_datetime(df_seasons["date"])
df_seasons["year"] = df_seasons["date"].dt.year
df_seasons = df_seasons[df_seasons["year"] != 2026]

# Final new seasons df
df_grouped_year = df_seasons.groupby(["year", "season"])["value"].mean().reset_index()

##################
### App layout ###
##################

app.layout = html.Div([
    html.H2("PM10 Seasonal Analysis"),
    html.Div([
        html.H4("Select Year:"),
        dcc.Dropdown(
            id="season-year-dropdown",
            options=[{"label": y, "value": y} for y in sorted(df_grouped_year["year"].unique())],
            value=df_grouped_year["year"].unique()[0],
            clearable=False,
            searchable=False
        )
    ], style={"width": "200px", "margin-bottom": "20px"}),
    # Two charts side by side
    html.Div([
        dcc.Graph(id="season-bar", style={"width": "48%"}),
        dcc.Graph(id="season-pie", style={"width": "48%"})
    ], style={"display": "flex", "justify-content": "space-between"})
])

#################
### Callbacks ###
#################


###########################
### Yearly Distribution ###
###########################

@callback(
    Output("season-bar", "figure"),
    Output("season-pie", "figure"),
    Input("season-year-dropdown", "value")
)
def update_pie(selected_year):
    # Filter data for the selected year
    df_year = df_grouped_year[df_grouped_year["year"] == selected_year]

    # ---------
    # Bar chart
    # ---------

    fig_bar = px.bar(
        df_year,
        x="season",
        y="value",
        title=f"PM10 Concentration per season [{selected_year}]",
        color="season",
        color_discrete_map=season_colors,
        category_orders={"season": SEASONS_ORDER},
        text="value"

    )
    # Adding axis titles
    fig_bar.update_layout(
        title_x=0.5,
        xaxis_title = "Season",
        yaxis_title="PM10 (µg/m³)",
        legend_title_text = "Season"
    )

    fig_bar.update_yaxes(range=[0, 25])
    
    # Adding grid lines
    fig_bar.update_yaxes(
        showgrid=True,            # turn on horizontal grid
        gridcolor="#d3d3d3",      # light gray lines
        gridwidth=1,
        zeroline=False,
        showline=True,            # optional: show the axis line
        linecolor="#000000"       # color of the axis line
    )
    
    # ---------
    # Pie chart
    # ---------
    fig_pie = px.pie(
        df_year,
        names="season",
        values="value",
        title=f"Relative PM10 distribution per season [{selected_year}]",
        color="season",
        color_discrete_map = season_colors,
        category_orders={"season": SEASONS_ORDER}
    )
    fig_pie.update_layout(title_x=0.5)

    # Return the callback
    return fig_bar, fig_pie

if __name__ == "__main__":
    app.run(debug=True)