import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Order of the months in the year
MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅

###########################
### Loading data frames ###
###########################

### Load weather data
df_weather = pd.read_csv("Collected Data/Question 5_6/MonthlyWeighted.csv")
df_weather["date"] = pd.to_datetime(df_weather["date"])
df_weather["month"] = df_weather["date"].dt.month_name()
df_weather["year"] = df_weather["date"].dt.year
df_weather["month"] = pd.Categorical(df_weather["month"], categories=MONTH_ORDER, ordered=True)
weather_labels = {
    "peak_temperature": "Peak Temperature (°C)",
    "precipitation_mm": "Precipitation (mm)"
}

###########################
### Initialize Dash app ###
###########################

dash.register_page(__name__)

##################
### App layout ###
##################

layout = html.Div([

    # Title
    html.H2([
        "Air Quality and Weather in Major German Cities"
    ]),

    # Research question
    html.Div([
        html.H3("Research Question"),
        # The actual question
        html.H4([
            "How do temperature and precipitation influence ",
            html.Span(["PM", html.Sub("10")]),
            " and ",
            html.Span(["PM", html.Sub("2.5")]),
            " concentrations in major German cities between 2016 and 2025?"
        ]),
        # Description of why it is interesting and relevant
        html.P([
            "This question was mostly based on our own curiousity. We were unsure if the weather "
            "could influence the amount of air pollution. Perhaps high temperatures could destroy particles," 
            "or the rainfall might wash them away. Unsure what we would find, we wanted to examine if there is "
            "a correlation here at all, and if there were any, come up with theories as for why this might be."
        ]),
    ]),

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
            " before aggregating it into monthly segments."
            ". Weather data (temperature and precipitation) was obtained from the Open-Meteo API. "
            "As the amount of data we could request from Open-Meteo was imited, we chose to only look at the 100 largest german cities."
            "The Open-Meteo API requires geocoordinates to request weather related data, which were provided for the stations used by the Umweltbundesamt."
        ]),
    ]),

    # Visualization description
    html.Div([
        html.H6([
            "Visualization"
        ]),
        html.P([
            "This visualization shows monthly ",
            html.Span(["PM", html.Sub("10")]),
            " and ",
            html.Span(["PM", html.Sub("2.5")]),
            " concentrations alongside temperature or precipitation for a selected year."
        ]),
    ]),

    html.Hr(),

    # Controls in a horizontal layout
    html.Div([
        # Year dropdown
        html.Div([
            html.Label("Select Year:"),
            dcc.Dropdown(
                id="weather_year-dropdown",
                options=[
                    {"label": y, "value": y}
                    for y in sorted(df_weather["year"].unique())
                ],
                value=sorted(df_weather["year"].unique())[0],
                clearable=False,
                searchable=False
            ),
        ], style={"margin-right": "40px", "width": "200px"}),

        # Weather variable radio buttons
        html.Div([
            html.Label("Select Weather Variable:"),
            dcc.RadioItems(
                id="weather_dropdown",
                options=[
                    {"label": "Peak Temperature", "value": "peak_temperature"},
                    {"label": "Precipitation", "value": "precipitation_mm"}
                ],
                value="peak_temperature",
                labelStyle={"display": "inline-block", "margin-right": "20px"}
            )
        ])
    ],
    style={"display": "flex", "align-items": "center", "margin-bottom": "30px"}),

    # Visualization
    dcc.Graph(id="weather_graph"),

    html.Hr(),

    # Interpretation
    html.Div([
        html.H4("Interpretation"),
        html.P([
            "By looking at all the different years and observing the peak temperature "
            "and precipitation, we concluded there is no correlation between the temperature "
            "or the amount of rain and air pollution. There simply were not any visible "
            "trends that indicate those variables are in any way correlated."
        ])
    ], style={"margin-top": "30px"}),

])

#################
### Callbacks ###
#################

@callback(
    Output("weather_graph", "figure"),
    Input("weather_year-dropdown", "value"),
    Input("weather_dropdown", "value")
)
def update_combined_graph(selected_year, selected_weather):

    # Filter data
    df_filtered = df_weather[df_weather["year"] == selected_year].sort_values("month")

    fig_weather = go.Figure()

    # Add PM bars
    fig_weather.add_trace(go.Bar(
        x=df_filtered["month"],
        y=df_filtered["pm10"],
        name=PM10_LABEL,
        marker_color="#fcc653",
        yaxis="y1"
    ))
    fig_weather.add_trace(go.Bar(
        x=df_filtered["month"],
        y=df_filtered["pm25"],
        name=PM25_LABEL,
        marker_color="#53befc",
        yaxis="y1"
    ))

    # Add weather line trace
    fig_weather.add_trace(go.Scatter(
        x=df_filtered["month"],
        y=df_filtered[selected_weather],
        name=weather_labels[selected_weather],
        mode="lines+markers",
        line=dict(color="#f54033", width=3),
        yaxis="y2"
    ))

    # Define fixed ranges for second y-axis
    if selected_weather == "peak_temperature":
        y2_range = [0, 40]  # fixed temperature range
    else:  # precipitation_mm
        y2_range = [0, 10]  # fixed precipitation range

    # Update layout
    fig_weather.update_layout(
        title=f"Air Quality & {weather_labels[selected_weather]} [{selected_year}]",
        title_x=0.5,
        xaxis=dict(title="Month"),
        yaxis=dict(
            title="Concentration (µg/m³)",
            side="left",
            range=[0, 30]  # fixed PM range
        ),
        yaxis2=dict(
            title=weather_labels[selected_weather],
            overlaying="y",
            side="right",
            range=y2_range  # fixed range
        ),
        barmode="group",
        legend=dict(
            x=1,
            y=1,
            xanchor='right',
            yanchor='top',
            orientation="h"
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return fig_weather