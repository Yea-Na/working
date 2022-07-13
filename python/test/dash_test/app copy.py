
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
import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



## 데이터 불러오기
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


    

date_sum_prc = pd.DataFrame(original_data.groupby('date')['item_prc'].sum())
date_count = pd.DataFrame(original_data.groupby('date')['item_title'].count())
result_1 = pd.concat([date_sum_prc,date_count],axis=1).reset_index()
test = []
for i in result_1['date']:
    test.append(datetime.datetime.strptime(str(i),'%Y%m%d').date())
result_1 = pd.concat([result_1,pd.DataFrame(test)], axis=1,names='date_3')

test = []
for i in result_1[0]:
    test.append(datetime.datetime.isocalendar(i).week)
result_1 = pd.concat([result_1,pd.DataFrame(test)], axis=1)
result_1.columns=['date','item_prc','count','date_2','week']
result_2 = result_1.groupby('week').sum().reset_index()
result_2['item_prc_2'] = result_2['item_prc'].astype('str').str[:-7]

week = list(result_2['week'].astype('str'))
sum_prc=list(result_2['item_prc_2'])
date_count=list(result_2['count'])



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
            # html.Div([   ])

            
            html.Div([
                    dcc.Checklist(["All"], [], id="large-checklist"),
                    dcc.Checklist(small, [], id="small-checklist"),
                    ])
            
            
            
        ], style={'float':'left', 'width':'10%', 'border-right':'1px solid black', 'font-size':'17px'})  
        
        ]),
        
        
    html.Div(children=[
        html.Div(children=[        
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
        dcc.Tab(label='업종별 온라인 시장 현황', value='tab-1',),
        dcc.Tab(label='브랜드별 시장 포지션', value='tab-2'),
        dcc.Tab(label='브랜드별 판매 채널', value='tab-3'),
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
    # Output("cat_small_0", "value"),
    Output("cat_large_0", "value"),
    Input("cat_small_0", "value"),
    Input("cat_large_0", "value"),
)
def sync_checklists_2(small_selected, large_selected):
    ctg = callback_context
    input_id = ctg.triggered[0]["prop_id"].split(".")[0]
    print(input_id)
    print(small_selected)
    print(category[0])
    # if input_id == "cat_small_0":
    #     large_selected = large_selected if set(small_selected) == set(cat_small_0) else []
    # else:
    #     small_selected = ["침대"] if large_selected else []
    return large_selected





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
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week,y=sum_prc,name='매출총합',marker_color='rgb(55, 83, 109)'))
        fig.add_trace(go.Bar(x=week,y=date_count,name='매출건수',marker_color='rgb(26, 118, 255)'))
        fig.update_layout(
                        title='2022년 업종별 온라인 시장 현황 [주별]',
                        xaxis=dict(title='주차',tickfont_size=14),
                        yaxis=dict(title='단위:천만',titlefont_size=16,tickfont_size=14),
                        legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)'),
                        barmode='group',
                        bargap=0.5, # gap between bars of adjacent location coordinates.
                        bargroupgap=0.5 # gap between bars of the same location coordinate.
                        ,
                        )
        
        return html.Div([
            html.Div(children=[      
      
            dcc.Graph(figure=fig)
            ], style={'height':'10%'}),
            
            
            html.Div(children=[            
            # html.H3('Tab content 2'),
            dcc.Graph(figure=fig)
            ], style={'height':'50%'})
        ])
        
        
    elif tab == 'tab-2':

        return html.Div([
            html.H3('Tab content 2'),
            
            dcc.Graph(
                figure={
                    'data':[
                        dict(x=week , y= sum_prc, type='bar', )
                        
                    ]
                }
            )

        ]),
    elif tab == 'tab-3':
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

        return html.Div([
            
            html.H3('Tab content 3'),   


            dcc.Graph(figure=fig)


        ]),        
        






if __name__ == '__main__':
    app.run_server(host='0.0.0.0')




# 매출 / 전주랑 비교 / 브랜드별 / 품목별 / top5 / ..