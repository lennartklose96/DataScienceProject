from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
import numpy as np

data = {
    "PM10":  pd.read_csv("Collected Data/Question 1.2/neujahr_PM10.csv"),
    "PM2.5":  pd.read_csv("Collected Data/Question 1.2/neujahr_PM2,5.csv"),
    "NO2":  pd.read_csv("Collected Data/Question 1.2/neujahr_NO2.csv")
}

for df in data.values():
    df["date start"] = pd.to_datetime(df["date start"])

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Air Quality"),

    html.Label("Select Pollutants"),
    dcc.Dropdown(
        id="pollutant-dropdown",
        options=[
            {"label": "PM\u2081\u2080", "value": "PM10"},
            {"label": "PM\u2082.\u2085", "value": "PM2.5"},
            {"label": "NO\u2082", "value": "NO2"}
        ],
        value=["PM10"],
        clearable=False,
        multi=True
    ),

    dcc.Graph(id="pollutant-graph")
])

# Callback für dynamische Graphen
@app.callback(
    Output("pollutant-graph", "figure"),
    Input("pollutant-dropdown", "value")
)
def update_graph(selected_pollutants):
    fig = go.Figure()

    for name in selected_pollutants:
        df = data[name]

        # Scatterpunkte
        fig.add_trace(
            go.Scatter(
                x=df["date start"],
                y=df["value"],
                mode="markers",
                name=name,
            )
        )

        # Regression
        if len(df) > 3:
            x_num = df["date start"].map(pd.Timestamp.toordinal)
            y = df["value"]
            coeff = np.polyfit(x_num, y, 3)
            poly = np.poly1d(coeff)
            y_reg = poly(x_num)

            fig.add_trace(
                go.Scatter(
                    x=df["date start"],
                    y=y_reg,
                    mode="lines",
                    name=name + " trend",
                )
            )

    fig.update_layout(
        title="Germany around New Year",
        xaxis_title="Date",
        yaxis_title="Concentration in µg/m³",
        hovermode="closest",
        showlegend=False
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)