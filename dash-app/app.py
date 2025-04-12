import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime

app = dash.Dash(__name__)
server = app.server

# Constants
WIND_FARMS = ["Genesis", "Foster", "Whirl"]
TURBINES_PER_FARM = 28
REFRESH_INTERVAL = 30 * 1000  # 30 seconds in milliseconds

# Generate fake initial data
def generate_fake_data():
    now = datetime.datetime.now()
    timestamps = [now - datetime.timedelta(minutes=i) for i in range(60)][::-1]
    data = {
        "timestamp": timestamps,
        "wind_speed": np.random.uniform(2.5, 15, size=60),
        "power_output": np.random.uniform(0, 2.5, size=60),
    }
    return pd.DataFrame(data)

data = {
    farm: generate_fake_data() for farm in WIND_FARMS
}

app.layout = html.Div([
    html.H1("SCADA Dashboard Simulation", style={"textAlign": "center"}),

    dcc.Dropdown(
        id='site-dropdown',
        options=[{"label": farm, "value": farm} for farm in WIND_FARMS],
        value="Genesis",
        style={"width": "300px", "margin": "auto"}
    ),

    dcc.Graph(id='wind-speed-graph'),
    dcc.Graph(id='power-output-graph'),

    dcc.Interval(
        id='interval-component',
        interval=REFRESH_INTERVAL,
        n_intervals=0
    )
])

@app.callback(
    [Output('wind-speed-graph', 'figure'),
     Output('power-output-graph', 'figure')],
    [Input('site-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graphs(site, n):
    df = data[site]

    # Simulate appending new data every refresh
    new_row = pd.DataFrame({
        "timestamp": [datetime.datetime.now()],
        "wind_speed": [np.random.uniform(2.5, 15)],
        "power_output": [np.random.uniform(0, 2.5)]
    })
    df = pd.concat([df.iloc[1:], new_row])
    data[site] = df

    wind_fig = go.Figure([
        go.Scatter(x=df['timestamp'], y=df['wind_speed'], mode='lines', name='Wind Speed')
    ])
    wind_fig.update_layout(title=f"{site} - Wind Speed", yaxis_title="m/s")

    power_fig = go.Figure([
        go.Scatter(x=df['timestamp'], y=df['power_output'], mode='lines', name='Power Output')
    ])
    power_fig.update_layout(title=f"{site} - Power Output", yaxis_title="MW")

    return wind_fig, power_fig

if __name__ == '__main__':
    app.run_server(debug=True)
