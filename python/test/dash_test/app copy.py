
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from base64 import encode
from pydoc import classname
from turtle import left
from unicodedata import category

from dash import dash, dcc, html, Input, Output, State, callback_context

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import openpyxl


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

original_data = pd.read_excel('python/test/dash_test/일룸_책상_구매데이터_1차_220513_220626_v0.1_220629_사후분석.xlsx')
oh_test = pd.read_csv("python/test/dash_test/oh_매출테스트.csv")
# python\test\dash_test\oh_매출테스트.csv


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



category = {
    '가구':['침대', '소파', '책상', '기타'], 
    '패션':['원피스', '재킷', '팬츠', '셔츠', '블라우스','아우터','기타' ],
    '뷰티':['스킨케어', '메이크업'],
    '식음료':['간편식', '음료','간식', '양념', '기타']    
}

# print(category.index(category.keys('가구')))
# print(category.items())

# def make_checklist(category):
#     return html.Div([
#         dcc.Checklist([k], className='cat_large'),
#         html.Div([
#             dcc.Checklist(v, className='cat_small'),
#             ], style={'text-indent':'15px'}),
#         html.Br(),
#     ])
        
# checklists = []
# for k,v in category.items():
   
#     checklists.append(make_checklist(category))
    

# original_data = pd.read_excel('일룸_책상_구매데이터_1차_220513_220626_v0.1_220629_사후분석.xlsx')
# date_sum_prc = pd.DataFrame(original_data.groupby('date')['item_prc'].sum())
# date_count = pd.DataFrame(original_data.groupby('date')['item_title'].count())
# result_1 = pd.concat([date_sum_prc,date_count],axis=1).reset_index()



def make_checklist(category):
    return html.Div(children=[
        dcc.Checklist([k], [], id='cat_large_'+ str(index)),
        html.Div(children=[
            dcc.Checklist(v, [], id='cat_small_'+ str(index)),
            ], style={'text-indent':'15px'}),
        html.Br(),
    ])
        
checklists = []
for index,(k,v) in enumerate(category.items()):
    print(index, k,v)
    checklists.append(make_checklist(enumerate(category.items())))

    

small = ["New York City", "Montréal", "San Francisco"]

##### 사이드바 = 체크박스
##
app.layout = html.Div([
    html.Div([
        html.Div(id='test_output',children=[html.Br()], style={'float':'left', 'width':'5%'}),
        html.Div(children=[
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(), 
            
            
            html.Div(checklists),

            
            html.Div([
                    dcc.Checklist(["All"], [], id="large-checklist"),
                    dcc.Checklist(small, [], id="small-checklist"),
                    ])
            
            
            
        ], style={'float':'left', 'width':'10%', 'border-right':'1px solid black', 'font-size':'17px'})  
        
        ]),
        
        
    html.Div(children=[
        html.Div(children=[        
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
        dcc.Tab(label='Tab three', value='tab-3'),
        ]),
        html.Div(id='tabs-example-content-1'),


        ], style={'float':'left', 'width':'75%'})     
         
    ],)
    
])



print(id)


@app.callback(
    Output("small-checklist", "value"),
    Output("large-checklist", "value"),
    Input("small-checklist", "value"),
    Input("large-checklist", "value"),
)
def sync_checklists(small_selected, large_selected):
    ctx = callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(input_id)
    print(small_selected)
    if input_id == "small-checklist":
        large_selected = ["All"] if set(small_selected) == set(small) else []
    else:
        small_selected = small if large_selected else []
    return small_selected, large_selected







@app.callback(
    Output('test_output', 'children'),
    Input('cat_small_0','value')
)

def test_output(value):
    return f'You have selected {value}'

### 탭
@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(children=[            
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Tab content2'
                    }
                }
            )
            ], style={'height':'10%'}),
            
            
            html.Div(children=[            
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                    ],
                    'layout': {
                        'title': 'Tab content2'
                    }
                }
            )
            ], style={'height':'50%'})
        ])
        
        
    elif tab == 'tab-2':
        date_sum_prc = pd.DataFrame(original_data.groupby('date')['item_prc'].sum())
        date_count = pd.DataFrame(original_data.groupby('date')['item_title'].count())
        result_1 = pd.concat([date_sum_prc,date_count],axis=1).reset_index()
        date = list(result_1['date'].astype('str').str[2:])
        sum_prc=list(result_1['item_prc'])
        date_count=list(result_1['item_title'])
        return html.Div([
            html.H3('Tab content 2'),
            
            dcc.Graph(
                figure={
                    'data':[
                        dict(x=date , y= sum_prc, type='go.bar')
                    ]
                }
            )
# fig = px.line(x=date, y=sum_prc, color=px.Constant("This year"),
#                 labels=dict(x="Fruit", y="Amount", color="Time Period"))
# fig.add_trace(go.Bar(x=date, y=date_count, name="Last year"))
# fig.show()
            # dcc.Graph(
            #     figure=dict(
            #         data=[dict(
            #             x=[1, 2, 3],
            #             y=[5, 10, 6],
            #             type='bar'
            #         )]
            #     )
            # )
        ]),
        
        






if __name__ == '__main__':
    app.run_server(host='0.0.0.0')




# 매출 / 전주랑 비교 / 브랜드별 / 품목별 / top5 / ..