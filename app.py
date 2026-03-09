import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go



# Load data
df_weather = pd.read_csv("Collected Data/Question 5_6/MonthlyWeighted.csv")
df_weather['date'] = pd.to_datetime(df_weather['date'])
df_weather['month'] = df_weather['date'].dt.month_name()
df_weather['year'] = df_weather['date'].dt.year

# Ensure months are in calendar order
month_order = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
df_weather['month'] = pd.Categorical(df_weather['month'], categories=month_order, ordered=True)

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Layout
app.layout = html.Div([
    html.H1("Air Quality and Weather Dashboard"),
    
    html.H3("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df_weather['year'].unique())],
        value=df_weather['year'].unique()[0],
        clearable=False
    ),

    html.H3("Select weather variable:"),
    dcc.Dropdown(
        id='weather-dropdown',
        options=[
            {'label': 'Peak Temperature', 'value': 'peak_temperature'},
            {'label': 'Precipitation', 'value': 'precipitation_mm'}
        ],
        value='peak_temperature',
        clearable=False
    ),

    dcc.Graph(id='pm-graph'),
    dcc.Graph(id='weather-graph')
])

# Callback
@callback(
    Output('pm-graph', 'figure'),
    Output('weather-graph', 'figure'),
    Input('year-dropdown', 'value'),
    Input('weather-dropdown', 'value')
)
def update_graphs(selected_year, selected_weather):
    # Filter for selected year
    df_filtered = df_weather[df_weather['year'] == selected_year].sort_values('month')

    # PM line chart
    fig_pm = px.line(
        df_filtered,
        x='month',
        y=['pm10','pm25'],
        markers=True,
        title=f"PM10 and PM2.5 Trends in {selected_year}"
    )
    fig_pm.update_layout(yaxis_title='Concentration (µg/m³)')

    # Weather line chart
    fig_weather = px.line(
        df_filtered,
        x='month',
        y=selected_weather,
        markers=True,
        title=f"{selected_weather.replace('_',' ').title()} Trends in {selected_year}"
    )
    fig_weather.update_layout(yaxis_title=selected_weather.replace('_',' ').title())

    return fig_pm, fig_weather

if __name__ == '__main__':
    app.run(debug=True)