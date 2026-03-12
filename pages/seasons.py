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
SEASONS_ORDER = ["Spring", "Summer", "Autumn", "Winter"]
# Labels for pollutants
PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅
NO2_LABEL = "NO\u2082"          # NO₂

# Dictionary for labels per pollutant
POLLUTANT_LABELS = {
    "pm10": "PM\u2081\u2080",   # PM₁₀
    "pm25": "PM\u2082.\u2085",  # PM₂.₅
    "no2":  "NO\u2082"          # NO₂
}

###############
### Styling ###
###############

# Define colors for each season
season_colors = {
    "Spring": "#98E221",  
    "Summer": "#FFEB3C",
    "Autumn": "#F3A32B",
    "Winter": "#65B2FA"
}


###########################
### Initialize Dash app ###
###########################

# Initialize Dash page
dash.register_page(__name__)

###########################
### Loading data frames ###
###########################

# Loading .csv
df_spring = pd.read_csv("Collected Data/Question 4/spring_daily_avg_data.csv")
df_summer = pd.read_csv("Collected Data/Question 4/summer_daily_avg_data.csv")
df_autumn = pd.read_csv("Collected Data/Question 4/autumn_daily_avg_data.csv")
df_winter = pd.read_csv("Collected Data/Question 4/winter_daily_avg_data.csv")

# Adding seasons
df_spring["season"] = "Spring"
df_summer["season"] = "Summer"
df_autumn["season"] = "Autumn"
df_winter["season"] = "Winter"

# Combining to singular df
df_seasons = pd.concat([df_spring, df_summer, df_autumn, df_winter])
df_seasons["date"] = pd.to_datetime(df_seasons["date"])
df_seasons["year"] = df_seasons["date"].dt.year
df_seasons = df_seasons[df_seasons["year"] != 2026]

# Final new seasons df
df_grouped_year = df_seasons.groupby(["year", "season"])[["pm10","pm25","no2"]].mean().reset_index()

##################
### App layout ###
##################

layout = html.Div([

    # Page title
    html.H2("Seasonal Pollutant Analysis"),

    # Research question
    html.Div([
        html.H3("Research Question"),
        html.H4([
            "How do seasonal changes influence the pollution concentrations in Germany between 2016 and 2025?"
        ]),
        html.P([
            "We wanted to explore how air pollution varies across seasons. "
            "Perhaps there is a correlation between the season or how polluted it is, "
            "or maybe certain months favor certain pollutants."
        ]),
    ]),
    # Data description
    html.Div([
        html.H6("Used Data"),
        html.P([
            "Daily air quality data for the pollutants were obtained "
            "obtained from the Umweltbundesamt API. "
            "The data was aggregated into seasonal averages to facilitate comparisons."
        ])
    ]), 

    # Visualization description
    html.Div([
        html.H6("Visualization"),
        html.P([
            "The bar chart shows the mean concentration of the selected pollutant per season. "
            "The pie chart shows the relative distribution of the pollutant across seasons."
        ])
    ]),

    html.Hr(),

    # Controls in horizontal layout
    html.Div([
        # Year dropdown
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="seasons_year-dropdown",
                options=[{"label": y, "value": y} for y in sorted(df_grouped_year["year"].unique())],
                value=df_grouped_year["year"].unique()[0],
                clearable=False,
                searchable=False
            )
        ], style={"margin-right": "40px", "width": "200px"}),

        # Pollutant dropdown
        html.Div([
            html.Label("Select Pollutant:"),
            dcc.Dropdown(
                id="seasons_pollutant-dropdown",
                options=[
                    {"label": PM10_LABEL, "value": "pm10"},
                    {"label": PM25_LABEL, "value": "pm25"},
                    {"label": NO2_LABEL, "value": "no2"}
                ],
                value="pm10",
                clearable=False,
                searchable=False
            )
        ], style={"width": "200px"})
    ], style={"display": "flex", "align-items": "center", "margin-bottom": "30px"}),

    # Visualization charts side by side
    html.Div([
        dcc.Graph(id="seasons_bar", style={"width": "48%"}),
        dcc.Graph(id="seasons_pie", style={"width": "48%"})
    ], style={"display": "flex", "justify-content": "space-between"}),

    html.Hr(),

    # Interpretation
    html.Div([
        html.H4("Interpretation"),
        html.P([
            "By comparing pollutant levels across seasons for several different years, "
            "winter and spring are consistently more polluted, particularly when it comes to ",
            html.Span(["NO", html.Sub("2")]), 
            ". Summer however tends to be relatively clean. This effect is a bit less pronounced for the "
            "fine dust particles, but still observable."
        ])
    ])
])

#################
### Callbacks ###
#################

@callback(
    Output("seasons_bar", "figure"),
    Output("seasons_pie", "figure"),
    Input("seasons_year-dropdown", "value"),
    Input("seasons_pollutant-dropdown", "value")
)
def update_pie(selected_year, selected_pollutant):
    # Filter data for the selected year
    df_year = df_grouped_year[df_grouped_year["year"] == selected_year]

    # Get proper label for selected pollutant
    pollutant_label = POLLUTANT_LABELS[selected_pollutant]

    # ---------
    # Bar chart
    # ---------
    fig_bar = px.bar(
        df_year,
        x="season",
        y=selected_pollutant,
        title=f"{pollutant_label} Concentration per Season [{selected_year}]",
        color="season",
        color_discrete_map=season_colors,
        category_orders={"season": SEASONS_ORDER},
        text=selected_pollutant
    )

    # Update layout with proper units
    fig_bar.update_layout(
        title_x=0.5,
        xaxis_title="Season",
        yaxis_title=f"{pollutant_label} (µg/m³)" if selected_pollutant != "no2" else f"{pollutant_label} (µg/m³)",
        legend_title_text="Season"
    )

    # Fixed range for easier comparison
    fig_bar.update_yaxes(range=[0, 35])

    # Round the numbers displayed on top of bars
    fig_bar.update_traces(texttemplate='%{text:.2f}')

    # Adding grid lines
    fig_bar.update_yaxes(
        showgrid=True,
        gridcolor="#d3d3d3",
        gridwidth=1,
        zeroline=False,
        showline=True,
        linecolor="#000000"
    )

    # ---------
    # Pie chart
    # ---------
    fig_pie = px.pie(
        df_year,
        names="season",
        values=selected_pollutant,
        title=f"Relative {pollutant_label} Distribution per Season [{selected_year}]",
        color="season",
        color_discrete_map=season_colors,
        category_orders={"season": SEASONS_ORDER}
    )
    fig_pie.update_layout(title_x=0.5)

    # Return figures for the callback
    return fig_bar, fig_pie