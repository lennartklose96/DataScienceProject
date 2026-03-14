import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

###########################
### Initialize Dash app ###
###########################

dash.register_page(__name__)

#################
### Constants ###
#################

MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
YEARS = [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]
POLLUTANTS = ["PM10","PM2,5","NO2"]

###########################
### Loading data frames ###
###########################

daily_data = {
    "PM10": {},
    "PM2,5": {},
    "NO2": {}
}
monthly_data = {
    "PM10": {},
    "PM2,5": {},
    "NO2": {}
}

countries = [
    "baden-württemberg",
    "bayern",
    "berlin",
    "brandenburg",
    "bremen",
    "hamburg",
    "hessen",
    "mecklenburg-vorpommern",
    "niedersachsen",
    "nordrhein-westfalen",
    "rheinland-pfalz",
    "saarland",
    "sachsen",
    "sachsen-anhalt",
    "schleswig-holstein",
    "thüringen"
]

country_labels = {
    "baden-württemberg": "Baden-Württemberg",
    "bayern": "Bayern",
    "berlin": "Berlin",
    "brandenburg": "Brandenburg",
    "bremen": "Bremen",
    "hamburg": "Hamburg",
    "hessen": "Hessen",
    "mecklenburg-vorpommern": "Mecklenburg-Vorpommern",
    "niedersachsen": "Niedersachsen",
    "nordrhein-westfalen": "Nordrhein-Westfalen",
    "rheinland-pfalz": "Rheinland-Pfalz",
    "saarland": "Saarland",
    "sachsen": "Sachsen",
    "sachsen-anhalt": "Sachsen-Anhalt",
    "schleswig-holstein": "Schleswig-Holstein",
    "thüringen": "Thüringen"
}

def add_data(country):

    for p in POLLUTANTS:

        try:
            daily_data[p][country] = pd.read_csv(f"Collected Data/Question 2/{p}/daily_avg_{country}_{p}.csv")
            monthly_data[p][country] = pd.read_csv(f"Collected Data/Question 2/{p}/monthly_avg_{country}_{p}.csv")
        
        except Exception:
            pass

for c in countries:
    add_data(c)


##################
### Page layout ###
##################

layout = html.Div([

    # Title
    #html.H2("Air Quality in different German States"),

    # Research question
    html.Div([
        #html.H3("Research Question"),
        html.H4([
            "How does the air quality vary between the different german federal states?"
        ], style={
            "font-size": "30px"
        }),
        html.P([
            "TODO"
        ]),
    ]),

    # Data description
    html.Div([
        html.H6("Used Data"),
        html.P([
            "TODO"
        ]),
    ]),

    # Visualization description
    html.Div([
        html.H6("Visualization"),
        html.P([
            "TODO"
        ]),
    ]),

    html.Hr(),

    # Controls
    html.Div([

        html.Div([
            html.Label("Select Time Mode"),
            dcc.RadioItems(
                id="states_date-mode",
                options=["Monthly", "Daily"],
                value="Monthly"
            ),
        ], style={"margin-right": "40px"}),

        html.Div([
            html.Label("Select Pollutant"),
            dcc.RadioItems(
                id="states_pollutant-mode",
                options=[
                    {"label": "PM\u2081\u2080", "value": "PM10"},
                    {"label": "PM\u2082.\u2085", "value": "PM2,5"},
                    {"label": "NO\u2082", "value": "NO2"}
                ],
                value="PM10"
            ),
        ], style={"margin-right": "40px"}),

    ], style={"display": "flex", "gap": "40px", "margin-bottom": "20px"}),

    # Month and Year sliders
    html.Div([
        html.Div([
            html.Label("Select Month"),
            dcc.RangeSlider(
                1, 
                12,
                id="states_month-slider",
                allowCross=False,
                marks={i+1: m for i, m in enumerate(MONTH_ORDER)},
                value=[1, 12]
            ),
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Select Year"),
            dcc.RangeSlider(
                2016, 
                2026,
                id="states_year-slider",
                allowCross=False,
                marks={y: str(y) for y in YEARS},
                value=[2016, 2026]
            ),
        ]),
    ]),

    html.Div([
        # Graph
        dcc.Graph(id="states_data-graph", style={"width": "100%"}),
    ], style={
            "display": "flex",
            "gap": "20px",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
            "margin-top":"10px"
            }),

    html.Hr(),

    # Interpretation
    html.Div([
        html.H4("Interpretation"),
        html.P([
            "TODO"
        ])
    ]),

])

#################
### Callbacks ###
#################

@callback(
    Output("states_data-graph", "figure"),
    Input("states_year-slider", "value"),
    Input("states_month-slider", "value"),
    Input("states_date-mode", "value"),
    Input("states_pollutant-mode", "value")
)
def update_graph(selected_year, selected_month, selected_mode, selected_pollutant):

    fig = go.Figure()

    ##################
    ### Select DFs ###
    ##################
        
    if selected_mode == "Daily":
        data = daily_data[selected_pollutant].items()
    else:
        data = monthly_data[selected_pollutant].items()

    
    for country, df in data:

            df["date start"] = pd.to_datetime(df["date start"])
            df["year"] = df["date start"].dt.year
            df["month"] = df["date start"].dt.month

            filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

            filtered_df_month = filtered_df_year[filtered_df_year["month"].between(selected_month[0], selected_month[1])]

            fig.add_trace(
                go.Scatter(
                    x=filtered_df_month["date start"],
                    y=filtered_df_month["value"],
                    mode="lines",
                    name=country_labels[country]
                )
            )
        
    fig.update_layout(
            title=f"Air Pollution [{selected_pollutant[:2]}<sub>{selected_pollutant[2:]}</sub>] in german federal states",
            xaxis_title="Time",
            yaxis_title=f"{selected_pollutant[:2]}<sub>{selected_pollutant[2:]}</sub> concentration (µg/m³)"
    )

    return fig
