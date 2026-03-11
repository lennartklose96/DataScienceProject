import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

dash.register_page(__name__)

# Order of the months in the year
MONTH_ORDER = ["January","February","March","April","May","June","July","August","September","October","November","December"]
#MONTH_DIGIT = [1,2,3,4,5,6,7,8,9,10,11,12]

###############
### Styling ###
###############

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

###########################
### Loading data frames ###
###########################


### Austria
#### Daily 
df_aut_d_no2 = pd.read("Collected Data/Question 8/austria/daily_avg_austria_NO2.csv")
df_aut_d_pm10 = pd.read("Collected Data/Question 8/austria/daily_avg_austria_PM10.csv")
df_aut_d_pm25 = pd.read("Collected Data/Question 8/austria/daily_avg_austria_PM25.csv")
#### Monthly 
df_aut_m_no2 = pd.read("Collected Data/Question 8/austria/monthly_avg_austria_NO2.csv")
df_aut_m_pm10 = pd.read("Collected Data/Question 8/austria/monthly_avg_austria_PM10.csv")
df_aut_m_pm25 = pd.read("Collected Data/Question 8/austria/monthly_avg_austria_PM25.csv")


### France
#### Daily 
df_fr_d_no2 = pd.read("Collected Data/Question 8/france/daily_avg_france_NO2.csv")
df_fr_d_pm10 = pd.read("Collected Data/Question 8/france/daily_avg_france_PM10.csv")
df_fr_d_pm25 = pd.read("Collected Data/Question 8/france/daily_avg_france_PM25.csv")
#### Monthly 
df_fr_m_no2 = pd.read("Collected Data/Question 8/france/monthly_avg_france_NO2.csv")
df_fr_m_pm10 = pd.read("Collected Data/Question 8/france/monthly_avg_france_PM10.csv")
df_fr_m_pm25 = pd.read("Collected Data/Question 8/france/monthly_avg_france_PM25.csv")


### Germany
#### Daily 
df_de_d_no2 = pd.read("Collected Data/Question 8/germany/daily_avg_germany_NO2.csv")
df_de_d_pm10 = pd.read("Collected Data/Question 8/germany/daily_avg_germany_PM10.csv")
df_de_d_pm25 = pd.read("Collected Data/Question 8/germany/daily_avg_germany_PM25.csv")
#### Monthly 
df_de_m_no2 = pd.read("Collected Data/Question 8/germany/monthly_avg_germany_NO2.csv")
df_de_m_pm10 = pd.read("Collected Data/Question 8/germany/monthly_avg_germany_PM10.csv")
df_de_m_pm25 = pd.read("Collected Data/Question 8/germany/monthly_avg_germany_PM25.csv")


### Italy
#### Daily 
df_it_d_no2 = pd.read("Collected Data/Question 8/italy/daily_avg_italy_NO2.csv")
df_it_d_pm10 = pd.read("Collected Data/Question 8/italy/daily_avg_italy_PM10.csv")
#### Monthly 
df_it_m_no2 = pd.read("Collected Data/Question 8/italy/monthly_avg_italy_NO2.csv")
df_it_m_pm10 = pd.read("Collected Data/Question 8/italy/monthly_avg_italy_PM10.csv")


### Poland
#### Daily 
df_pl_d_no2 = pd.read("Collected Data/Question 8/poland/daily_avg_poland_NO2.csv")
df_pl_d_pm10 = pd.read("Collected Data/Question 8/poland/daily_avg_poland_PM10.csv")
df_pl_d_pm25 = pd.read("Collected Data/Question 8/poland/daily_avg_poland_PM25.csv")
#### Monthly 
df_pl_m_no2 = pd.read("Collected Data/Question 8/poland/monthly_avg_poland_NO2.csv")
df_pl_m_pm10 = pd.read("Collected Data/Question 8/poland/monthly_avg_poland_PM10.csv")
df_pl_m_pm25 = pd.read("Collected Data/Question 8/poland/monthly_avg_poland_PM25.csv")


### Romania
#### Daily 
df_ro_d_no2 = pd.read("Collected Data/Question 8/romania/daily_avg_romania_NO2.csv")
df_ro_d_pm10 = pd.read("Collected Data/Question 8/romania/daily_avg_romania_PM10.csv")
#### Monthly 
df_ro_m_no2 = pd.read("Collected Data/Question 8/romania/monthly_avg_romania_NO2.csv")
df_ro_m_pm10 = pd.read("Collected Data/Question 8/romania/monthly_avg_romania_PM10.csv")


### Spain
#### Daily 
df_es_d_no2 = pd.read("Collected Data/Question 8/spain/daily_avg_spain_NO2.csv")
df_es_d_pm10 = pd.read("Collected Data/Question 8/spain/daily_avg_spain_PM10.csv")
df_es_d_pm25 = pd.read("Collected Data/Question 8/spain/daily_avg_spain_PM25.csv")
#### Monthly 
df_es_m_no2 = pd.read("Collected Data/Question 8/spain/monthly_avg_spain_NO2.csv")
df_es_m_pm10 = pd.read("Collected Data/Question 8/spain/monthly_avg_spain_PM10.csv")
df_es_m_pm25 = pd.read("Collected Data/Question 8/spain/monthly_avg_spain_PM25.csv")


### United Kingdom
#### Daily 
df_uk_d_no2 = pd.read("Collected Data/Question 8/uk/daily_avg_uk_NO2.csv")
df_uk_d_pm10 = pd.read("Collected Data/Question 8/uk/daily_avg_uk_PM10.csv")
df_uk_d_pm25 = pd.read("Collected Data/Question 8/uk/daily_avg_uk_PM25.csv")
#### Monthly 
df_uk_m_no2 = pd.read("Collected Data/Question 8/uk/monthly_avg_uk_NO2.csv")
df_uk_m_pm10 = pd.read("Collected Data/Question 8/uk/monthly_avg_uk_PM10.csv")
df_uk_m_pm25 = pd.read("Collected Data/Question 8/uk/monthly_avg_uk_PM25.csv")

##################
### Daily data ###
##################

daily_data_no2 = {
    'Austria': df_aut_d_no2,
    'France': df_fr_d_no2,
    'Germany':  df_de_d_no2,
    'Italy':  df_it_d_no2,
    'Poland': df_pl_d_no2,
    'Romania': df_ro_d_no2,
    'Spain': df_es_d_no2,
    'UK': df_uk_d_no2
}

daily_data_pm10 = {
    'Austria': df_aut_d_pm10,
    'France': df_fr_d_pm10,
    'Germany':  df_de_d_pm10,
    'Italy':  df_it_d_pm10,
    'Poland':  df_pl_d_pm10,
    'Romania': df_ro_d_pm10,
    'Spain': df_es_d_pm10,
    'UK': df_uk_d_pm10
}

daily_data_pm25 = {
    'Austria': df_aut_d_pm25,
    'France': df_fr_d_pm25,
    'Germany':  df_de_d_pm25,
    'Poland': df_pl_d_pm25,
    'Spain': df_es_d_pm25,
    'UK': df_uk_d_pm25
}

####################
### Monthly data ###
####################

monthly_data_no2 = {
    'Austria': df_aut_m_no2,
    'France': df_fr_m_no2,
    'Germany':  df_de_m_no2,
    'Italy':  df_it_m_no2,
    'Poland': df_pl_m_no2,
    'Romania': df_ro_m_no2,
    'Spain': df_es_m_no2,
    'UK': df_uk_m_no2
}

monthly_data_pm10 = {
    'Austria': df_aut_m_pm10,
    'France': df_fr_m_pm10,
    'Germany':  df_de_m_pm10,
    'Italy':  df_it_m_pm10,
    'Poland':  df_pl_m_pm10,
    'Romania': df_ro_m_pm10,
    'Spain': df_es_m_pm10,
    'UK': df_uk_m_pm10
}

monthly_data_pm25 = {
    'Austria': df_aut_m_pm25,
    'France': df_fr_m_pm25,
    'Germany':  df_de_m_pm25,
    'Poland': df_pl_m_pm25,
    'Spain': df_es_m_pm25,
    'UK': df_uk_m_pm25
}


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

    dcc.RadioItems(id="date-mode",
                   options=["Monthly", "Daily"],
                   value="Monthly"
                   ),

    dcc.RadioItems(id="pollutant-mode",
                   options=["PM<sub>10</sub>", "PM<sub>2.5</sub>", "NO<sub>2</sub>"],
                   value="PM<sub>10</sub>"
                   ),

    dcc.RangeSlider(
        1, 
        12,
        id="month-slider",
        allowCross=False,
        marks={i+1: m for i, m in enumerate(MONTH_ORDER)},
        value=[1, 12]
        ),

    dcc.RangeSlider(
        0, 
        10,
        id="year-slider",
        allowCross=False,
        marks={i: i for i in range(2016, 2027)},
        value=[0, 10]
        ),

    dcc.Graph(id="data-graph")
    
])

#################
### Callbacks ###
#################

@callback(
    Output("data-graph", "figure"),
    Input("year-slider", "value"),
    Input("month-slider", "value"),
    Input("date-mode", "value"),
    Input("pollutant-mode", "value")
)
def update_graph(selected_year, selected_month, selected_mode, selected_pollutant):

    fig = go.Figure()

    ##################
    ### Select DFs ###
    ##################

    if selected_mode == "Monthly":


        if selected_pollutant == "NO2":

            for country, df in monthly_data_no2.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="NO<sub>2</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="NO<sub>2</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig


        elif selected_pollutant == "PM<sub>10</sub>":

            for country, df in monthly_data_pm10.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="PM<sub>10</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="PM<sub>10</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig


        else:

            for country, df in monthly_data_no2.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="PM<sub>2.5</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="PM<sub>2.5</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig
        
    
    else:

        
        if selected_pollutant == "NO2":

            for country, df in daily_data_no2.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="NO<sub>2</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="NO<sub>2</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig


        elif selected_pollutant == "PM<sub>10</sub>":

            for country, df in daily_data_pm10.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="PM<sub>10</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="PM<sub>10</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig


        else:

            for country, df in daily_data_no2.items():

                df["year"] = df["date"].dt.year
                df["month"] = df["date"].dt.month

                filtered_df_year = df[df["year"].between(selected_year[0], selected_year[1])]

                filtered_df_month = filtered_df_year[df["month"].between(selected_month[0], selected_month[1])]

                fig.add_trace(
                    go.Scatter(
                        x=filtered_df_month["date"],
                        y=filtered_df_month["value"],
                        mode="lines+markers",
                        name=country
                    )
                )
            
            fig.update_layout(
                title="PM<sub>2.5</sub> Air Pollution by Countries",
                xaxis_title="Time",
                yaxis_title="PM<sub>2.5</sub> µg/m³",
                width=1000,
                height=500
            )

            return fig

    
    


    
    
