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

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

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

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

##################
### App layout ###
##################

app.layout = html.Div([
    html.H2("Air Quality & Weather"),

    html.Div([
        html.Div([
            html.H4("Select Year:"),
            dcc.Dropdown(
                id="weather-year-dropdown",
                options=[{"label": y, "value": y} for y in sorted(df_weather["year"].unique())],
                value=df_weather["year"].unique()[0],
                clearable=False
            ),
        ], style={"width": "200px", "display": "inline-block", "margin-right": "20px"}),

        html.Div([
            html.H4("Select Weather Variable:"),
            dcc.Dropdown(
                id="weather-dropdown",
                options=[
                    {"label": "Peak Temperature", "value": "peak_temperature"},
                    {"label": "Precipitation", "value": "precipitation_mm"}
                ],
                value="peak_temperature",
                style={"width": "300px"},
                clearable=False
            )
        ], style={"width": "350px", "display": "inline-block"})
    ]),

    html.Div(
        dcc.Graph(id="weather-graph"),
        style={"width": "900px", "margin": "0 auto"}
    )
])

#################
### Callbacks ###
#################

@callback(
    Output("weather-graph", "figure"),
    Input("weather-year-dropdown", "value"),
    Input("weather-dropdown", "value")
)
def update_combined_graph(selected_year, selected_weather):

    ###############
    ### Weather ###
    ###############

    # Weather DF filtered
    df_filtered = df_weather[df_weather["year"] == selected_year].sort_values("month")

    fig_weather = go.Figure()

    # Add PM bars
    fig_weather.add_trace(go.Bar(
        x=df_filtered["month"],
        y=df_filtered["pm10"],
        name="PM10",
        marker_color="#fcc653",
        yaxis="y1"
    ))
    fig_weather.add_trace(go.Bar(
        x=df_filtered["month"],
        y=df_filtered["pm25"],
        name="PM2.5",
        marker_color="#53befc",
        yaxis="y1"
    ))

    # Add line for selected weather variable
    fig_weather.add_trace(go.Scatter(
        x=df_filtered["month"],
        y=df_filtered[selected_weather],
        name=weather_labels[selected_weather],
        mode="lines+markers",
        line=dict(color="#f34033", width=3),
        yaxis="y2"
    ))

    # Layout
    fig_weather.update_layout(
        title=f"Air Quality & {weather_labels[selected_weather]} in {selected_year}",
        title_x=0.5,  # Center title
        xaxis=dict(title="Month"),
        yaxis=dict(title="Concentration (µg/m³)", side="left"),
        yaxis2=dict(
            title=selected_weather.replace("_"," ").title(),
            overlaying="y",
            side="right"
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

if __name__ == "__main__":
    app.run(debug=True)