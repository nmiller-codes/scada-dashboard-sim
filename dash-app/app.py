import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load updated fake SCADA data
df = pd.read_csv('data/fake_scada_data_updated.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Get unique site names
site_names = df['site'].unique()

# Start Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("SCADA Dashboard Simulation", className="my-3"),
    
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": site, "value": site} for site in site_names],
        value=site_names[0],
        clearable=False,
        className="mb-4"
    ),
    
    dcc.Graph(id="power-graph"),
    dcc.Graph(id="wind-graph"),
    dcc.Interval(
        id="interval-component",
        interval=30*1000,  # 30 seconds
        n_intervals=0
    )
])

@app.callback(
    [Output("power-graph", "figure"),
     Output("wind-graph", "figure")],
    [Input("site-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)
def update_graphs(selected_site, n_intervals):
    filtered = df[df["site"] == selected_site].sort_values("timestamp")
    
    fig1 = px.line(filtered, x="timestamp", y="active_power_kw", title=f"{selected_site} - Active Power (kW)")
    fig1.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    
    fig2 = px.line(filtered, x="timestamp", y="wind_speed_mps", title=f"{selected_site} - Wind Speed (m/s)")
    fig2.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    
    return fig1, fig2

if __name__ == "__main__":
    app.run_server(debug=True)
