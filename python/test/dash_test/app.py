
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


oh_test = pd.read_csv("python/test/dash_test/oh_매출테스트.csv")
# python\test\dash_test\oh_매출테스트.csv


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")




aaa = oh_test['상품명'][2:].value_counts().reset_index().head(5)
labels = aaa['index']
values = aaa['상품명']

# Use `hole` to create a donut-like pie chart
fig2 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])


total_sales = str(oh_test['결제가(판매비/조립비/선불)'][1:].astype(int).sum())



app.layout = html.Div(children=[
    html.H1(children='test_dashbord'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    
    html.H3(children="매출총액 : " + total_sales),
    html.H5(children="top 5 매출"),
    
    dcc.Graph(
        id='example-graph2',
        figure=fig2
    ),
    
    
    
    
    ########
    
html.Div([
    html.Div(children=[
        html.Label('Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),

        html.Br(),
        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'],
                     ['Montréal', 'San Francisco'],
                     multi=True),

        html.Br(),
        html.Label('Radio Items'),
        dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal'),
    ], style={'padding': 10, 'flex': 1}),


    html.Div(children=[
        html.Label('Checkboxes'),
        dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
                      ['Montréal', 'San Francisco']
        ),



     
    
    html.Br(),
        html.Label('Text Input'),
        dcc.Input(value='MTL', type='text'),
    
    html.Br(),
    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: f'Label {i}' if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'padding': 10, 'flex': 1})

], style={'display': 'flex', 'flex-direction': 'row'})

    
])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')




# 매출 / 전주랑 비교 / 브랜드별 / 품목별 / top5 / ..