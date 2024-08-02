from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)

# Load your data
filePath = "./combined_data_results.csv"
df = pd.read_csv(filePath)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    # Dropdown for selecting regions
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df['region'].unique()],
        placeholder="Select a region",
        multi=True  # Allow multiple region selection
    ),

    # Graph that will be updated based on the dropdown selection
    dcc.Graph(id='sales-graph'),
])

# Callback to update the graph based on dropdown selection
@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_figure(selected_regions):
    if selected_regions:
        filtered_df = df[df['region'].isin(selected_regions)]
    else:
        filtered_df = df

    # Create the bar chart with the filtered data
    fig = px.bar(filtered_df, x="date", y="sales", color="region", barmode="group")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
