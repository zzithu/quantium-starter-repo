#My apologies to any software engineer who has to decipher this.. only god knows but it tests!

from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict

# Import the names of callback functions you want to test
from src.dashVisualizer import update_figure, get_filtered_data_length

import pandas as pd
import pytest

#This method creates a mock figure to test.. can it make a figure and what not
@pytest.fixture
def setup_figure():
    stored_data = [
        {'date': '2024-07-01', 'sales': 150, 'region': 'North'},
        {'date': '2024-07-02', 'sales': 200, 'region': 'South'}
    ]

    df_all = pd.DataFrame({
        'date': ['2024-07-01', '2024-07-02', '2024-07-03', '2024-07-04'],
        'sales': [100, 150, 200, 250],
        'region': ['North', 'South', 'East', 'West']
    })

    start_date = '2024-07-01'
    end_date = '2024-07-03'
    selected_regions = ['North', 'East']  # Make sure this matches exactly
    load_option = 'limited'
    
    fig = update_figure(start_date, end_date, selected_regions, load_option, stored_data, df_all)
    


    return fig

#I really wanted to make this easier, and there is defintely a way to, but this also is very reliable and adaptable
@pytest.fixture
def setup_length():
    stored_data = [
        {'date': '2024-07-01', 'sales': 150, 'region': 'North'},
        {'date': '2024-07-02', 'sales': 200, 'region': 'South'}
    ]

    df_all = pd.DataFrame({
        'date': ['2024-07-01', '2024-07-02', '2024-07-03', '2024-07-04'],
        'sales': [100, 150, 200, 250],
        'region': ['North', 'South', 'East', 'West']
    })

    start_date = '2024-07-01'
    end_date = '2024-07-03'
    selected_regions = ['North', 'East']  # Make sure this matches exactly
    load_option = 'limited'
    
    length = get_filtered_data_length(start_date, end_date, selected_regions, load_option, df_all)

#returns the length of filtered data, IE if element is out of date range it wont count, resulting in 2 regions with this mock data
    return length

#Does it exist?
def test_figure_not_none(setup_figure):
    fig = setup_figure
    assert fig is not None, "Figure should not be None"

#Does dropdown have regions
def test_figure_data_length(setup_length):
    length = setup_length
    #Filtered data will have 2 regions
    assert length == 2
    

#header stuuff
def test_figure_title(setup_figure):
    fig = setup_figure
    assert fig.layout.title.text == 'Sales Bar Graph', "Title should match expected value"

def test_figure_xaxis_title(setup_figure):
    fig = setup_figure
    assert fig.layout.xaxis.title.text == 'Date', "X-axis title should be 'Date'"

def test_figure_yaxis_title(setup_figure):
    fig = setup_figure
    assert fig.layout.yaxis.title.text == 'Sales', "Y-axis title should be 'Sales'"

# Run the tests using: python -m pytest -v