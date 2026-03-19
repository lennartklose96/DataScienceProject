import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

############################
### Initialize Dash page ###
############################

dash.register_page(__name__)

#################
### Constants ###
#################

MONTH_ORDER = ["JAN","FEB","MAR","APR","MAY","JUNE","JULY","AUG","SEPT","OCT","NOV","DEC"]
YEARS = [2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026]
POLLUTANTS = ["PM10","PM2.5","NO2"]

# Labels for pollutants
PM10_LABEL = "PM\u2081\u2080"   # PM₁₀
PM25_LABEL = "PM\u2082.\u2085"  # PM₂.₅
NO2_LABEL = "NO\u2082"          # NO₂

# Dictionary for labels per pollutant
POLLUTANT_LABELS = {
    "PM10": "PM\u2081\u2080",   # PM₁₀
    "PM2.5": "PM\u2082.\u2085",  # PM₂.₅
    "NO2":  "NO\u2082"          # NO₂
}

COUNTRIES = ["austria", "france", "germany", "italy", "poland", "romania", "spain", "uk"]

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

def add_data(country):

    for p in POLLUTANTS:

        try:
            daily_df = pd.read_csv(f"Collected Data/Question 8/{country}/daily_avg_{country}_{p}.csv")
            monthly_df = pd.read_csv(f"Collected Data/Question 8/{country}/monthly_avg_{country}_{p}.csv")

            for df in [daily_df, monthly_df]:
                df["date"] = pd.to_datetime(df["date"])
                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

            country_label = "UK" if country == "uk" else country.capitalize()
            
            daily_data[p][country_label] = daily_df
            monthly_data[p][country_label] = monthly_df
        
        except Exception:
            pass

for c in COUNTRIES:
    add_data(c)


##################
### Page layout ###
##################

layout = html.Div(children=[
    
    # Research question
    html.Div([
        html.Div([
            # The actual question
            html.H4([
                "How does Germany compare to other countries in terms of the average concentrations of PM₁₀, PM₂.₅ and NO₂?"
            ], style={"font-size": "30px"}),
            # Description of why it is interesting and relevant
            html.P([
            "Comparing Germany with other European countries helps to understand how severe air pollution levels are in Germany relative to its neighbors. "
            "In addition, future research could explore the underlying reasons for differences in air pollution levels between these countries, "
            "particularly by examining domestic factors and environmental policy measures. "
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),
        
        # Data description
        html.Div([
            html.H4("Used Data"),
            html.P([
                "The Air Quality data for Germany were derived from an API provided by the German Environmental Agency (Umweltbundesamt), whereas "
                "for the other countries we collected data through the OpenAQ API. The datasets include measurements of PM\u2081\u2080, PM\u2082.\u2085, and NO₂. "
                "To analyze trends over time, the data was aggregated into daily and monthly averages. "
                "Each dataset contains a timestamp (date) and the corresponding pollutant concentration value in µg/m³. "
                "“It should be noted that not all countries had continuous measurements between 2016 and 2026. Moreover, Italy and Romania did not have enough PM\u2082.\u2085 measurements "
                "to provide meaningful results. "
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 0px 30px"}),

        # Visualization description
        html.Div([
            html.H4("Visualization"),
            html.P([
            "The first graph shows the recorded pollutant concentrations in µg/m³ for the listed countries over time. " 
            "The box plot illustrates how the countries differ in terms of their recorded air pollution levels. "
            ], style={"font-size": "18px"}),
        ],style={"margin": "10px 30px 10px 30px"}),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 25px auto",
                }),

    # Layout for the visualization
    html.Div([
        html.Div([
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
                        value=["PM10"],
                        multi=True,
                        clearable=False,
                        searchable=False,
                        style={"width": "200px"}
                    ),
                ]),

                html.Div([
                    html.Label("Select Countries"),
                    dcc.Dropdown(
                        id="countries_countries-dropdown",
                        options=[
                            {"label": "Austria", "value": "Austria"},
                            {"label": "France", "value": "France"},
                            {"label": "Germany", "value": "Germany"},
                            {"label": "Italy", "value": "Italy"},
                            {"label": "Poland", "value": "Poland"},
                            {"label": "Romania", "value": "Romania"},
                            {"label": "Spain", "value": "Spain"},
                            {"label": "UK", "value": "UK"},
                        ],
                        value=["Austria", "France", "Germany", "Italy",
                               "Poland", "Romania", "Spain", "UK"],
                        multi=True,
                        clearable=False,
                        searchable=False,
                        style={"width": "100%", "maxWidth": "750px"}
                    ),
                ]),

                
            ], style={
                "display": "flex",
                "gap": "40px",
                "margin-bottom": "20px",
                "margin": "30px 30px 0px 30px"
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

            ],style={
                "width": "80%",
                "display": "flex",
                "flexDirection": "column",
                "gap": "30px",
                "margin": "30px auto"
            }),
            
            html.Div([
                dcc.Graph(id="countries_pollution-graph", style={"width": "100%"}),
            ], style={
                "display": "flex",
                "gap": "20px",
                }),

        ]),
    
        html.Div([
                    
            html.Div([
                dcc.Graph(id="countries_boxplot-graph", style={"width": "100%"}),
            ], style={
                "display": "flex",
                "gap": "20px",
            }),

        ]),
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 25px auto",
                }),

    # Interpretation
    html.Div([
        html.H4("Interpretation",style={"margin": "10px 30px 0px 30px"}),
        html.P([            
            "Compared to the average across all countries, Germany's recorded "
            "PM\u2081\u2080 and PM\u2082.\u2085 concentrations are below average. For NO₂, however, "
            "Germany has above-average concentrations, which could be explained by "
            "the lack of a general speed limit on the Autobahn and the continued "
            "popularity of gasoline-powered cars in Germany. "
            
        ],style={"whiteSpace": "pre-line", "margin": "10px 30px 10px 30px", "font-size": "18px"})
    ], style={
                "display": "flex",
                "flex-direction": "column",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "background-color":"white",
                "min-height":"auto",
                "margin": "25px auto 0px auto",
                }),
])
    

#################
### Callbacks ###
#################

@callback(
    Output("countries_pollution-graph", "figure"),
    Input("countries_year-slider", "value"),
    Input("countries_month-slider", "value"),
    Input("countries_time-period", "value"),
    Input("countries_pollutant-dropdown", "value"),
    Input("countries_countries-dropdown", "value")
)
def update_graph(selected_year, selected_month, selected_mode, selected_pollutant, selected_countries):

    fig = go.Figure()

    ##################
    ### Select DFs ###
    ##################
    
    # Update each pollutant
    for pollutant in selected_pollutant:

        if selected_mode == "Daily":
            data = daily_data[pollutant]
        
        else:
            data = monthly_data[pollutant]

        for country in selected_countries:

            if country not in data:
                continue

            df = data[country]   

            temp = df.copy()
            
            temp = temp[
                (temp["year"].between(selected_year[0], selected_year[1])) &
                (temp["month"].between(selected_month[0], selected_month[1]))
            ]

            fig.add_trace(
                go.Scatter(
                    x=temp["date"],
                    y=temp["value"],
                    mode="lines+markers",
                    name=f"{country} ({POLLUTANT_LABELS[pollutant]})"
                )
            )

    # Get proper labels
    selected_labels = [POLLUTANT_LABELS[p] for p in selected_pollutant]
    fig.update_layout(
        title=f"Air Pollution ({', '.join(selected_labels)}) by Countries",
        xaxis_title="Time",
        yaxis_title="Concentration (µg/m³)"
    ) 
    
    return fig


@callback(
    Output("countries_boxplot-graph", "figure"),
    Input("countries_year-slider", "value"),
    Input("countries_month-slider", "value"),
    Input("countries_time-period", "value"),
    Input("countries_pollutant-dropdown", "value"),
    Input("countries_countries-dropdown", "value")
)
def update_boxplot(selected_year, selected_month, selected_mode, selected_pollutant, selected_countries):

    df_list = []

    for p in selected_pollutant:

        if selected_mode == "Daily":
            data = daily_data[p]
        else:
            data = monthly_data[p]

        for country in selected_countries:

            if country not in data:
                continue

            df = data[country]

            temp = df.copy()

            temp = temp[
                (temp["year"].between(selected_year[0], selected_year[1])) &
                (temp["month"].between(selected_month[0], selected_month[1]))
            ]

            temp["country"] = country
            temp["pollutant"] = POLLUTANT_LABELS[p]

            df_list.append(temp)

    if not df_list:
        return go.Figure()

    combined_df = pd.concat(df_list)

    avg_df = combined_df.copy()
    avg_df["country"] = "Average"

    combined_df = pd.concat([combined_df, avg_df])

    fig = px.box(
        combined_df,
        x="country",
        y="value",
        color="pollutant",
        points="outliers"
    )

    fig.update_layout(
        title="Distribution of Air Pollution by Country",
        xaxis_title="Country",
        yaxis_title="Concentration (µg/m³)"
    )

    return fig



    


    
    
