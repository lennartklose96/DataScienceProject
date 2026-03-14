import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

############################
### Initialize Dash page ###
############################

#dash.register_page(__name__)
app = dash.Dash(__name__)

#################
### Constants ###
#################

MONTH_ORDER = ["JAN","FEB","MAR","APR","MAY","JUNE","JULY","AUG","SEPT","OCT","NOV","DEC"]
YEARS = [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]
POLLUTANTS = ["PM10","PM2.5","NO2"]

###########################
### Loading data frames ###
###########################

daily_data = {
    "PM10": {},
    "PM2.5": {},
    "NO2": {}
}
monthly_data = {
    "PM10": {},
    "PM2.5": {},
    "NO2": {}
}

countries = ["austria", "france", "germany", "italy", "poland", "romania", "spain", "uk"]

def add_data(country):

    for p in POLLUTANTS:

        try:
            daily_data[p][country] = pd.read_csv(f"Collected Data/Question 8/{country}/daily_avg_{country}_{p}.csv")
            monthly_data[p][country] = pd.read_csv(f"Collected Data/Question 8/{country}/monthly_avg_{country}_{p}.csv")
        
        except Exception:
            pass

for c in countries:
    add_data(c)


##################
### Page layout ###
##################

app.layout = html.Div(children=[
    
   #Title    
    html.H2("Air Pollution in different Countries"),

    #Research question
    html.Div([
        html.H3("Research Question"),
        # The actual question
        html.H4([
            "How does Germany compare to other countries in terms of the daily and monthly average concentrations of PM2.5, PM10 and NO2?"
        ]),
        # Description of why it is interesting and relevant
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
    
    # Controls (time period + pollutants)
    html.Div([

        html.Div([
            html.Label("Select Time Period"),
            dcc.RadioItems(id="countries_time-period",
                   options=["Monthly", "Daily"],
                   value="Monthly",
                   style={"width": "200px"}
                ),
        ]),

        html.Div([
            html.Label("Select Pollutants"),
            dcc.Dropdown(
                id="countries_pollutant-dropdown",
                options=[
                    {"label": "PM\u2081\u2080", "value": "PM10"},
                    {"label": "PM\u2082.\u2085", "value": "PM2.5"},
                    {"label": "NO\u2082", "value": "NO2"}
                ],
                value="PM10",
                multi=True,
                clearable=False,
                searchable=False,
                style={"width": "200px"}
            ),
        ]),

    ], style={
        "display": "flex",
        "gap": "40px",
        "margin-bottom": "20px"
    }),
    
    # Visualizations side by side
    html.Div([
        dcc.Graph(id="countries_pollution-graph", style={"width": "50%"}),
        #dcc.Graph(id="corona_boxplot-graph", style={"width": "50%"})
    ], 
    style={
        "display": "flex",
        "gap": "20px"
    }),

    # Controls (RangeSlider for months + years)
    html.Div([

        html.Div([
            html.Label("Select Month", style={"textAlign": "center", "width": "100%"}),
            dcc.RangeSlider(
            1, 
            12,
            id="countries_month-slider",
            allowCross=False,
            marks={i+1: m for i, m in enumerate(MONTH_ORDER)},
            value=[1, 12],
            ),
        ]),

        html.Div([
            html.Label("Select Year", style={"textAlign": "center", "width": "100%"}),
            dcc.RangeSlider(
                2016, 
                2026,
                id="countries_year-slider",
                allowCross=False,
                marks={y: str(y) for y in YEARS},
                value=[2016, 2026],
            ),
        ]),

    ], style={
    "width": "50%",
    "display": "flex",
    "flexDirection": "column",
    "gap": "30px",
    "margin": "30px auto"
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
    Output("countries_pollution-graph", "figure"),
    Input("countries_year-slider", "value"),
    Input("countries_month-slider", "value"),
    Input("countries_time-period", "value"),
    Input("countries_pollutant-dropdown", "value")
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

            df["date"] = pd.to_datetime(df["date"])
            df["year"] = df["date"].dt.year
            df["month"] = df["date"].dt.month

            filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

            filtered_df_month = filtered_df_year[filtered_df_year["month"].between(selected_month[0], selected_month[1])]

            fig.add_trace(
                go.Scatter(
                    x=filtered_df_month["date"],
                    y=filtered_df_month["value"],
                    mode="lines+markers",
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

if __name__ == "__main__":
    app.run(debug=True) 