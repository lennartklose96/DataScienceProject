from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import numpy as np

df_1 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_baden-württemberg_PM10.csv")
df_2 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_bayern_PM10.csv")
df_3 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_berlin_PM10.csv")
df_4 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_brandenburg_PM10.csv")
df_5 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_bremen_PM10.csv")
df_6 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_hamburg_PM10.csv")
df_7 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_hessen_PM10.csv")
df_8 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_mecklenburg-vorpommern_PM10.csv")
df_9 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_niedersachsen_PM10.csv")
df_10 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_nordrhein-westfalen_PM10.csv")
df_11 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_rheinland-pfalz_PM10.csv")
df_12 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_saarland_PM10.csv")
df_13 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_sachsen_PM10.csv")
df_14 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_sachsen-anhalt_PM10.csv")
df_15 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_schleswig-holstein_PM10.csv")
df_16 = pd.read_csv("Collected Data/Question 2/PM10/daily_avg_thüringen_PM10.csv")

data = {
    "Baden-Württemberg": df_1,
    "Bayern": df_2,
    "Berlin": df_3,
    "Brandenburg": df_4,
    "Bremen": df_5,
    "Hamburg": df_6,
    "Hessen": df_7,
    "Mecklenburg-Vorpommern": df_8,
    "Niedersachsen": df_9,
    "Nordrhein-Westfalen": df_10,
    "Rheinland-Pfalz": df_11,
    "Saarland": df_12,
    "Sachsen": df_13,
    "Sachsen-Anhalt": df_14,
    "Schleswig-Holstein": df_15,
    "Thüringen": df_16
}

for df in data.values():
    df["date start"] = pd.to_datetime(df["date start"])
    df["year"] = df["date start"].dt.year

years = sorted(df_1["year"].unique())

years = sorted(data["Baden-Württemberg"]["year"].unique())

app = Dash()

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),

    dcc.Slider(
        min(years),
        max(years),
        step=None,
        value=min(years),
        marks={str(year): str(year) for year in years},
        id='year-slider'
    )
])


@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value')
)

def update_figure(selected_year):

    fig = go.Figure()

    for state, df in data.items():

        filtered_df = df[df["year"] == selected_year]

        fig.add_trace(
            go.Scatter(
                x=filtered_df["date start"],
                y=filtered_df["value"],
                mode="lines",
                name=state
            )
        )

    fig.update_layout(
        title="PM10 Air Pollution by German Federal State",
        xaxis_title="Date",
        yaxis_title="PM<sub>10</sub> µg/m³",
        width=1000,
        height=500
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)