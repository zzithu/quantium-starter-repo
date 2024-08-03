
import os
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px

app = Dash(__name__)

# Load the entire dataset
filePath = os.path.join(os.path.dirname(__file__), '../data/combined_data_results.csv')
df_all = pd.read_csv(filePath)

# Prepare the dataset with region codes
df_all['Region_Code'] = pd.factorize(df_all['region'])[0]

app.layout = html.Div([
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': region, 'value': region} for region in df_all['region'].unique()],
        placeholder="Select a region",
        multi=True  # Allow multiple region selection
    ),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df_all['date'].min(),
        end_date=df_all['date'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.RadioItems(
        id='data-load-option',
        options=[
            {'label': 'Load All', 'value': 'all'},
            {'label': 'Load Limited (1000 rows)', 'value': 'limited'}
        ],
        value='limited'  # Default option
    ),
    dcc.Graph(id='sales-graph'),
    dcc.Store(id='data-store', data=df_all.head(1000).to_dict('records')),  # Store a subset of initial data
])

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('region-dropdown', 'value'),
     Input('data-load-option', 'value')],
    State('data-store', 'data')
)
def update_figure(start_date, end_date, selected_regions, load_option, stored_data, df_all):
    # Convert stored data back to a DataFrame
    df_current = pd.DataFrame(stored_data)

    # Filter data based on the selected date range
    if start_date and end_date:
        df_filtered = df_all[(df_all['date'] >= start_date) & (df_all['date'] <= end_date)]
        
        # Apply row limit if selected
        if load_option == 'limited':
            df_filtered = df_filtered.head(1000)  # Change 1000 to the desired limit
        
        # Prepare filtered data with region codes
        df_filtered['Region_Code'] = pd.factorize(df_filtered['region'])[0]
        
        # Combine current data with the filtered data
        df_combined = pd.concat([df_current, df_filtered], ignore_index=True)
    else:
        df_combined = df_current

    # Filter data based on selected regions
    if selected_regions:
        df_combined = df_combined[df_combined['region'].isin(selected_regions)]

    # Create a bar graph with Plotly Express
    fig = px.bar(df_combined, x='date', y='sales', color='region', barmode='group')

    # Update the x-axis to reflect the selected date range
    fig.update_xaxes(
        range=[start_date, end_date]
    )

    fig.update_layout(
        title='Sales Bar Graph',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Sales')
    )

    return fig

#Test gave issues, create method to return number of regions essentially
def get_filtered_data_length(start_date, end_date, selected_regions, load_option, df_all):
    # Filter data based on the selected date range
    if start_date and end_date:
        df_filtered = df_all[(df_all['date'] >= start_date) & (df_all['date'] <= end_date)]
        
        # Apply row limit if selected
        if load_option == 'limited':
            df_filtered = df_filtered.head(1000)  # Limit to 1000 rows
        
        # Filter data based on selected regions
        if selected_regions:
            df_filtered = df_filtered[df_filtered['region'].isin(selected_regions)]
    else:
        df_filtered = df_all  # If no date range, use full data

    return len(df_filtered)



if __name__ == '__main__':
    app.run(debug=True)



#Dash website http://127.0.0.1:8050/