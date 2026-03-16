import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

layout = html.Div([
    html.Div(

    # entire section
    [

        # Top section: Description
        html.Div([
                html.H2(
                    "Data Acquisition",
                    style={
                        "text-align": "left",
                        "margin-bottom": "10px",
                        "font-size": "30px",
                        "margin": "20px",
                    }),

                html.P(
                    """
                    For our project, we combined various data sources to conduct a 
                    comprehensive analysis of air quality in Germany. Our analysis covers 
                    the period from January 1, 2016 to March 1, 2026. We used data from the 
                    Federal Environment Agency on the air pollutants PM₁₀, PM₂.₅, and NO₂ 
                    for different time periods and federal states. This data is measured 
                    hourly by 427 stations distributed across Germany. Additionally, weather 
                    data such as temperature and precipitation were collected via a weather 
                    API to investigate correlations between meteorological conditions and 
                    air pollution. To analyze seasonal effects, the summer vacation periods 
                    of the individual federal states were taken into account. Finally, data 
                    from neighboring countries, such as France, were included to enable an 
                    international comparison of air quality. The collected data serve to 
                    identify trends, differences, and factors influencing air pollution.
                    """,
                    style={
                        "text-align": "left",
                        "margin": "0 auto",
                        "padding": "25px",
                        "padding-top": "0px",
                        "margin": "0px",
                    })
        ], style={
            "margin-bottom": "40px"
            }),

        # Lower section: Grid with 4 cells for the different APIs
        html.Div([
                # UBA API cell + button
                html.Div([
                        html.H4("UBA API"),
                        html.P("This is where you can access all data related to the " \
                        "measuring stations in Germany."),
                        html.Div(
                            html.A(
                                html.Button("Open", style={
                            "backgroundColor": "rgb(53, 167, 187)",
                            "color": "black",
                            "cursor": "pointer",
                        }),
                                href="https://www.umweltbundesamt.de/system/files/medien/358/dokumente/schnittstellenbeschreibung_luftdaten_api_v4.pdf",
                                target="_blank"
                            ), style={"margin-top": "auto"}
                        )
                    ], style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "background-color": "#ffffff",
                        "display": "flex",
                        "flexDirection": "column",
                        "height": "auto"
                    }),

                # Weather API cell + button
                html.Div([
                        html.H4("Weather API"),
                        html.P("Here, you can select the weather data for the chosen time " \
                        "period and, if desired, specific cities you’d like to view."),
                        html.Div(
                            html.A(html.Button("Open", style={
                            "backgroundColor": "rgb(53, 167, 187)",
                            "color": "black",
                            "cursor": "pointer"
                        }), href="https://open-meteo.com/",
                                target="_blank"
                            ), style={"margin-top": "auto"}
                        )
                    ], style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "background-color": "#ffffff",
                        "display": "flex",
                        "flexDirection": "column",
                        "height": "auto"
                    }),

                # Holiday API cell + button
                html.Div([
                        html.H4("Holiday API"),
                        html.P("The API returns the holidays for each federal state."),
                        html.Div(
                            html.A(html.Button("Open", style={
                            "backgroundColor": "rgb(53, 167, 187)",
                            "color": "black",
                            "cursor": "pointer"
                        }), href="https://ferien-api.maxleistner.de/",
                                target="_blank"
                            ), style={"margin-top": "auto"}
                        )
                    ], style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "background-color": "#ffffff",
                        "display": "flex",
                        "flexDirection": "column",
                        "height": "auto"
                    }),

                # Comparison API cell + button
                html.Div([
                        html.H4("Comparison API"),
                        html.P("Here, just like with the UBA API, you can access data on " \
                        "air pollution levels in other countries."),
                        html.Div(
                            html.A(html.Button("Open", style={
                            "backgroundColor": "rgb(53, 167, 187)",
                            "color": "black",
                            "cursor": "pointer"
                        }), href="https://openaq.org/",
                                target="_blank"
                            ), style={"margin-top": "auto"}
                        )
                    ], style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "background-color": "#ffffff",
                        "display": "flex",
                        "flexDirection": "column",
                        "height": "auto"
                    }),

            ],

            # Grid Layout
            style={
                "display": "grid",
                "grid-template-columns": "repeat(4, 1fr)",
                "gap": "20px"
            }

        )

    ], style={  # Section Styling
            "display": "grid",
            "padding": "20px",
            "margin": "25px auto 25px auto",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
            "background-color": "#ffffff"
        }),

    html.Div([

            # Text on the left
            html.Div([
                    html.H2("Our Data", style={"font-size": "30px"}),

                    html.P("The foundation of our analysis is the air quality data provided " \
                    "by the Federal Environment Agency (Umweltbundesamt). Using their public " \
                    "API, we retrieved measurements for the pollutants PM₁₀, PM₂.₅, and NO₂ "
                    "(components) " \
                    "from January 1, 2016 to March 1, 2026. The raw data was cleaned and " \
                    "preprocessed in order to remove incomplete records and unnecessary " \
                    "attributes. After this preparation step, the relevant information was " \
                    "stored as CSV files, which are then used for the " \
                    "visualizations and analyses presented in this project."),
                ],

                style={
                    "grid-row": "span 4",
                    "background-color": "#ffffff",
                    "padding": "25px",
                    "padding-top": "0px"
                }),

            # Box on the right (top) for API request
            html.Div([
                html.Details([
            html.Summary("UBA API request", style={
            "font-size": "18px",
            "margin-top": "10px",
            "margin-bottom": "-15px"
        }),

            html.Pre(
"""GET https://luftdaten.umweltbundesamt.de/api/air-data/v4/measures/json

{
{'request': {'component': '1',
  'scope': '1',
  'station': '21',
  'date_from': '2024-09-01',
  'date_to': '2025-09-01',
  'time_from': '09:00:00',
  'time_to': '09:00:00',
  'recent': False,
  'index': 'id',
  'lang': 'en',
  'datetime_from': '2024-09-01 08:00:00',
  'datetime_to': '2025-09-01 08:00:00'},
 'indices': {'data': {'station id': {'date start': ['component id',
     'scope id',
     'value',
     'date end',
     'index']}}},
 'data': {'21': {'2024-09-01 11:00:00': [1, 1, 16, '2024-09-01 12:00:00', '3'],
   '2024-09-02 11:00:00': [1, 1, 19, '2024-09-02 12:00:00', '3'],
   '2024-09-03 11:00:00': [1, 1, 35, '2024-09-03 12:00:00', '6'],
   '2024-09-04 11:00:00': [1, 1, 38, '2024-09-04 12:00:00', '7'],
   '2024-09-05 11:00:00': [1, 1, 55, '2024-09-05 12:00:00', '10'],
   ...
}""",
                style={
                    "background-color": "#f4f4f4",
                    "padding": "15px",
                    "border-radius": "5px",
                    "margin-top": "10px"
                })
        ])
                ], style={
                    "background-color":  "rgb(53, 167, 187)",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "padding-top": "0px"
                }),

            # Box on the right (middle - top) for API request
            html.Div(
                [
                   html.Details([
            html.Summary("Weather API request", style={
            "font-size": "18px",
            "margin-top": "10px",
            "margin-bottom": "-15px"
        }),

            html.Pre(
"""GET https://www.umweltbundesamt.de/api/airdata

{
    "station": "Berlin",
    "parameter": "pm10"
}""",
                style={
                    "background-color": "#f4f4f4",
                    "padding": "15px",
                    "border-radius": "5px",
                    "margin-top": "10px"
                })
        ])
                ], style={
                    "background-color":  "rgb(53, 167, 187)",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "padding-top": "0px"
                }),

            # Box on the right (middle - bottom) for API request
            html.Div(
                [
                   html.Details([
            html.Summary("Holiday API request", style={
            "font-size": "18px",
            "margin-top": "10px",
            "margin-bottom": "-15px"
        }),

            html.Pre(
"""GET https://www.umweltbundesamt.de/api/airdata

{
    "station": "Berlin",
    "parameter": "pm10"
}""",
                style={
                    "background-color": "#f4f4f4",
                    "padding": "15px",
                    "border-radius": "5px",
                    "margin-top": "10px"
                })
        ])
                ],
                style={
                    "background-color":  "rgb(53, 167, 187)",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "padding-top": "0px"
                }),

            # Box on the right (bottom) for API request
            html.Div(
                [
                   html.Details([
            html.Summary("International API request", style={
            "font-size": "18px",
            "margin-top": "10px",
            "margin-bottom": "-15px"
        }),

            html.Pre(
"""GET https://www.umweltbundesamt.de/api/airdata

{
    "station": "Berlin",
    "parameter": "pm10"
}""",
                style={
                    "background-color": "#f4f4f4",
                    "padding": "15px",
                    "border-radius": "5px",
                    "margin-top": "10px"
                })
        ])
                ],
                style={
                    "background-color":  "rgb(53, 167, 187)",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "padding-top": "0px"
                }),

        ],

        # Section Styling
        style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr", 
            "gridTemplateRows": "auto auto auto auto",
            "gap": "25px",
            "padding": "20px",
            "margin": "25px auto 25px auto",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
            "background-color": "#ffffff"
        }),


    html.Div([

        html.Div([
                # Large Textbox
            html.H2("Used Attributes", 
                    style={
                        "padding-top": "0px",
                        "margin-top": "40px",
                        "font-size": "30px"
                    }),
            html.P("Each measurement station in the dataset is described by several " \
            "attributes that provide information about its location, operational period, "
            "and classification within the monitoring network. Important attributes include:"),
            html.P("⦁ Station identification: station id, station code, station name"),
            html.P("⦁ Location information: city, street, street number, ZIP code, " \
            "longitude, latitude"),
            html.P("⦁ Operational information: active from, active to"),
            html.P("⦁ Network information: network id, network code, network name"),
            html.P("⦁ Station classification: station type, station setting (e.g. urban, " \
            "suburban, rural)"),
            html.P("Together with the pollutant measurements, these attributes allow us to " \
            "analyze spatial patterns, compare different types of monitoring stations, and " \
            "examine regional differences in air pollution levels across Germany."),
            html.P("The attributes we considered important for our research questions are as " \
            "follows:"),
        ], style={
                "padding": "25px",
                "padding-top": "0px",
                "margin-top": "20px",
                "margin-left": "20px",
                "margin-right": "20px",
            }),

        html.Div([
            
                # top row, left
                html.Div([html.H2("PM₁₀", style={"font-size": "20px"}),

                        html.P("PM₁₀ refers to particulate matter with a diameter of 10 " \
                        "micrometers or smaller. These particles originate from sources such " \
                        "as road traffic, industrial processes, and natural sources like " \
                        "dust. Due to their small size, they can enter the respiratory " \
                        "system and affect human health."),
                    ], style={
                        "grid-row": "span 1",
                        "background-color": "#ffffff",
                        "padding": "25px",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "padding-top": "0px",
                        "margin": "10px",
                    }),

                # top row, middle
                html.Div([html.H2("PM₂.₅", style={"font-size": "20px"}),
                          
                        html.P("PM₂.₅ consists of even finer particles with a diameter of " \
                        "2.5 micrometers or smaller. They are mainly produced by combustion " \
                        "processes, such as vehicle emissions, heating systems, and power " \
                        "plants. Because of their extremely small size, these particles " \
                        "can penetrate deep into the lungs and even enter the bloodstream.")
                    ], style={
                        "background-color": "#ffffff",
                        "padding": "25px",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "padding-top": "0px",
                        "margin": "10px",
                    }),

                # top row, right
                html.Div([html.H2("NO₂", style={"font-size": "20px"}),
                          
                        html.P("Nitrogen dioxide is a gaseous air pollutant primarily " \
                        "produced by combustion processes, especially from road traffic "
                        "and industrial activities. High concentrations of NO₂ can irritate " \
                        "the respiratory system and contribute to the formation of other " \
                        "pollutants such as ozone and particulate matter.")
                    ], style={
                        "background-color": "#ffffff",
                        "padding": "25px",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "padding-top": "0px",
                        "margin": "10px",
                    }),

            ], style={
                    "display": "grid",
                    "gridTemplateColumns": "33% 33% 33%", 
                    "gridTemplateRows": "auto auto auto auto",
                    "padding": "20px",
                    "margin": "auto auto auto auto"
                })
        ],style={
                "background-color": "#ffffff",
                "border-radius": "3px",
                "border": "1px solid black",
                "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                "padding-top": "0px",
                "margin": "25px auto 0px auto",
            }),
])