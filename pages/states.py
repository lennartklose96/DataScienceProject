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

layout = html.Div(children=[
    
    ###############
    ### Weather ###
    ###############
    
    html.H2("Air Quality in different Countries"),
    
    html.Div(children='''
        Compare the Air Quality in different Countries from 2016-2026.
    '''),

    dcc.RadioItems(id="states_date-mode",
                   options=["Monthly", "Daily"],
                   value="Monthly"
                   ),

    dcc.RadioItems(id="states_pollutant-mode",
                   options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2,5"},
            {"label": "NO\u2082", "value": "NO2"}
        ],
                   value="PM10"
                   ),

    dcc.RangeSlider(
        1, 
        12,
        id="states_month-slider",
        allowCross=False,
        marks={i+1: m for i, m in enumerate(MONTH_ORDER)},
        value=[1, 12]
        ),

    dcc.RangeSlider(
        2016, 
        2026,
        id="states_year-slider",
        allowCross=False,
        marks={y: str(y) for y in YEARS},
        value=[2016, 2026]
        ),

    dcc.Graph(id="states_data-graph")
    
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
                    name=country
                )
            )
        
    fig.update_layout(
            title=f"{selected_pollutant[:2]}<sub>{selected_pollutant[2:]}</sub> Air Pollution by Countries",
            xaxis_title="Time",
            yaxis_title=f"{selected_pollutant[:2]}<sub>{selected_pollutant[2:]}</sub> µg/m³",
            width=1000,
            height=500
    )

    return fig
