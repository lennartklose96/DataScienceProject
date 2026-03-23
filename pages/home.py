import dash
from dash import html


# Labels for pollutants
PM10_LABEL = "PM\u2081\u2080"
PM25_LABEL = "PM\u2082.\u2085"
NO2_LABEL = "NO\u2082"

dash.register_page(__name__, path = "/")

layout = html.Div([
    # first text-section
    html.Div([
        html.H1("What is the state of air pollution in German cities?", 
                style={"font-size": "30px", "margin": "10px 30px 0px 30px"
        }),
        html.Div("In this project, we analyze trends in air quality in Germany from " \
        "January 1, 2016, to March 1, 2026, focusing on the pollutants PM₁₀, PM₂.₅, and NO₂. " \
        "The goal is to analyze trends and patterns in air pollution and to identify potential " \
        "influencing factors. To this end, we examine temporal changes, regional differences, "
        "and the influence of specific events, weather conditions, and seasonal factors. We " \
        "also compare different types of measurement station locations and, in some cases, " \
        "place the results in an international context.",
        style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
    ], style={
            "padding": "20px",
            "margin": "25px auto 25px auto",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
            "background-color": "#ffffff",
        }),

    html.Div([
        # second text-section
        html.P("Essentially, the data provided by the Umweltbundesamt (UBA) forms " \
            "the foundation for all of our questions. Below, we have therefore categorized " \
            "our research questions to indicate whether additional APIs were used. The " \
            "left-hand side shows questions that rely exclusively on the data provided by " \
            "the Federal Environment Agency. The right-hand side, consequently, presents " \
            "the questions for which we have utilized additional APIs in order to place the " \
            "data obtained through our “main API” in a different context.",
            style={"margin": "10px 30px 0px 30px", "font-size": "18px"})
    ], style={
            "padding": "20px",
            "margin": "25px auto 25px auto",
            "border-radius": "3px",
            "border": "1px solid black",
            "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
            "background-color": "#ffffff",
        }),

    html.Div([

            # Box on the right
            html.Div([
                    html.H2("UBA", 
                            style={"font-size": "30px", "margin": "20px 30px 0px 30px"}),
                    html.P("⦁ How did the average values of " + PM10_LABEL + ", " + PM25_LABEL + " and "\
                           + NO2_LABEL + " change in Germany?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How does air pollution in Germany behave around New Years?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How did COVID-19 lockdowns and restrictions affect air "\
                           "pollution in Germany compared to the previous and following years?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How does the air quality vary between the different german "\
                           "federal states?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How does air pollution for " + PM10_LABEL + " vary across urban, suburban and rural "\
                           "areas?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How does air pollution for " + PM10_LABEL + " vary between background, traffic and "\
                           "industrial monitoring stations?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"}),
                    html.P("⦁ How do seasonal changes influence the pollution concentrations"\
                           " in Germany between 2016 and 2025?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"})
            ], style={
                    "grid-row": "span 3",
                    "background-color": "#ffffff",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                    "padding-top": "0px"
                }),

            # Box on the left (top)
            html.Div([
                    html.H2("Weather", 
                            style={"font-size": "30px", "margin": "20px 30px 0px 30px"}),
                    html.P("⦁ How did temperature and precipitation influence PM₁₀ and PM₂.₅ "\
                           "concentrations in major German cities between 2016 and 2025?",
                    style={"margin": "10px 30px 0px 30px", "font-size": "18px"})
            ], style={
                    "background-color": "#ffffff",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                    "padding-top": "0px"
                }),

            # Box on the left (middle)
            html.Div([
                    html.H2("Holidays", 
                            style={"font-size": "30px", "margin": "20px 30px 0px 30px"}),
                    html.P("⦁ How did summer school holidays in German federal states affect "\
                           + PM10_LABEL +" and " + PM25_LABEL + " concentrations over the past ten years?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"})
            ], style={
                    "background-color": "#ffffff",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                    "padding-top": "0px"
                }),

            # Box on the left (bottom)
            html.Div([
                    html.H2("International", 
                            style={"font-size": "30px", "margin": "20px 30px 0px 30px"}),
                    html.P("⦁ How does Germany compare to other countries in terms of the "\
                           "average concentrations of PM₁₀, PM₂.₅ and NO₂?",
                           style={"margin": "10px 30px 0px 30px", "font-size": "18px"})
            ], style={
                    "background-color": "#ffffff",
                    "padding": "25px",
                    "border-radius": "3px",
                    "border": "1px solid black",
                    "box-shadow": "0 1px 7px rgba(0, 0, 0, 0.63)",
                    "padding-top": "0px"
                }),
    ], style={
            "display": "grid",
            "grid-template-columns": "1fr 1fr",
            "grid-template-rows": "auto auto auto",
            "gap": "20px",
            "padding": "0px"
        })
])