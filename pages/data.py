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

    # Ganze Section
    [

        # Oberer Bereich: Beschreibung
        html.Div(

            [
                html.H2(
                    "Data Acquisition",
                    style={
                        "text-align": "LEFT",
                        "margin-bottom": "10px",
                        "font-size": "30px"
                    }
                ),

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
                        "font-size": "18px",
                        "max-width": "900px",
                        "margin": "0 auto"
                    }
                )
            ],

            style={
                "margin-bottom": "40px"
            }
        ),

        # Unterer Bereich: Grid mit 4 Feldern
        html.Div(

            [
                html.Div(
                    [
                        html.H4("UBA API"),
                        html.P("This is where you can access all data related to the " \
                        "measuring stations in Germany."),
                        html.Br(),
                        html.A(
                            html.Button("Open"),
                            href="https://www.umweltbundesamt.de/system/files/medien/358/dokumente/schnittstellenbeschreibung_luftdaten_api_v4.pdf",
                            target="_blank"
                        )
                    ],
                    style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                        "background-color": "#ffffff"
                    }
                ),

                html.Div(
                    [
                        html.H4("Weather API"),
                        html.P("Here, you can select the weather data for the chosen time " \
                        "period and, if desired, specific cities you’d like to view."),
                        html.Br(),
                        html.A(html.Button("Open"), href="https://open-meteo.com/",
                               target="_blank"
                               )
                    ],
                    style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                        "background-color": "#ffffff"
                    }
                ),

                html.Div(
                    [
                        html.H4("Holiday API"),
                        html.P("The API returns the holidays for each federal state."),
                        html.Br(),
                        html.A(html.Button("Open"), href="https://ferien-api.maxleistner.de/",
                               target="_blank"
                               )
                    ],
                    style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                        "background-color": "#ffffff"
                    }
                ),

                html.Div(
                    [
                        html.H4("Comparison API"),
                        html.P("Here, just like with the UBA API, you can access data on " \
                        "air pollution levels in other countries."),
                        html.Br(),
                        html.A(html.Button("Open"), href="https://openaq.org/",
                               target="_blank"
                               )
                    ],
                    style={
                        "border": "1px solid black",
                        "padding": "10px",
                        "text-align": "center",
                        "border-radius": "3px",
                        "border": "1px solid black",
                        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
                        "background-color": "#ffffff"
                    }
                ),

            ],

            # Grid Layout
            style={
                "display": "grid",
                "grid-template-columns": "repeat(4, 1fr)",
                "gap": "20px"
            }

        )

    ],

    # Section Styling
    style={
        "display": "grid",
        "padding": "20px",
        "margin": "30px auto 30px auto",
        "border-radius": "3px",
        "border": "1px solid black",
        "box-shadow": "0 5px 30px rgba(0, 0, 0, 0.63)",
        "background-color": "#ffffff"
    }
)

])