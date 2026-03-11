import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

###############
### Styling ###
###############

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

#########################
### App initilization ###
#########################

# Initialize Dash app
app = dash.Dash(
    __name__,
    use_pages = True,
    external_stylesheets=external_stylesheets
)
# Start server for render
server = app.server

##################
### App layout ###
##################

app.layout = html.Div([
    html.H1('Data Science Project pages - Air Pollution'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])


# Run the app
if __name__ == "__main__":
    app.run(debug=True)