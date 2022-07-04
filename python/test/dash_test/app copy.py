
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from turtle import left
import dash
from dash import dcc
from dash import html

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


oh_test = pd.read_csv("python/test/dash_test/oh_매출테스트.csv")
# python\test\dash_test\oh_매출테스트.csv


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)




app.layout = html.Div([
    html.Div([
        html.Div(children=[
            html.Br(),
            html.Br(),
            html.Label('가구'),
            dcc.Checklist(['침대', '소파', '책상', '기타', ]  ),                      
            
            html.Br(),
            html.Label('패션'),
            dcc.Checklist(['원피스', '재킷', '팬츠', '셔츠', '블라우스','아우터','기타' ]),
            
            html.Br(),
            html.Label('뷰티'),
            dcc.Checklist(['스킨케어', '메이크업' ]),

            html.Br(),
            html.Label('식음료'),
            dcc.Checklist(['간편식', '음료','간식', '양념', '기타' ]),
            html.Br(),
            html.Br(),

            
        ], style={'float':'left', 'width':'20%', 'margin':'10px', 'border-right':'1px solid black'})  
        
        ]),
        
        
    html.Div(children=[
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
        ], style={'float':'left'}) 

    
    
         
    ],)


    
])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0')




# 매출 / 전주랑 비교 / 브랜드별 / 품목별 / top5 / ..