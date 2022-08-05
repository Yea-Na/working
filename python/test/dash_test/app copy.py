
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from base64 import encode
from pydoc import classname
from tkinter.font import Font
from turtle import bgcolor, color, left, width
from unicodedata import category

from dash import dash, dcc, html, Input, Output, State, callback_context
from matplotlib import backend_tools, style
from matplotlib.font_manager import afmFontProperty
from matplotlib.pyplot import legend, margins
# from matplotlib.font_manager import style, FontEntry, FontProperties
from numpy import pad, size
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import openpyxl
import datetime

from pyrsistent import b


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



## 데이터 불러오기
# original_data = pd.read_excel('python/test/dash_test/일룸_책상_구매데이터_1차_220513_220626_v0.1_220629_사후분석.xlsx')
# oh_test = pd.read_csv("python/test/dash_test/oh_매출테스트.csv")
# python\test\dash_test\oh_매출테스트.csv
week_data = pd.read_csv('python/test/dash_test/week_data.csv')



category = {
    '가구':['침대', '소파', '책상', '기타'], 
    '패션':['원피스', '재킷', '팬츠', '셔츠', '블라우스','아우터','기타' ],
    '뷰티':['스킨케어', '메이크업'],
    '식음료':['간편식', '음료','간식', '양념', '기타']    
}




app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    
date=list(week_data['date'])
week = list(week_data['week'].astype('str'))
sum_prc=list(week_data['item_prc_2'])
date_count=list(week_data['count'])


def make_checklist(category):
    return html.Div(children=[
        dcc.Checklist([k], [], id='cat_large_'+ str(index)),
        html.Div(children=[
            dcc.Checklist(v, [], id='cat_small_'+ str(index)),
            ], style={'text-indent':'15px'}),
        html.Br(),
        html.Br()
    ])
        
checklists = []
for index,(k,v) in enumerate(category.items()):
    # print(index, k,v)
    checklists.append(make_checklist(enumerate(category.items())))

    
large =["All"]
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
            html.Div(checklists),
            html.Br(),
            html.Br(),

            
            # html.Div([
            #         dcc.Checklist(large, [], id="large-checklist"),
            #         dcc.Checklist(small, [], id="small-checklist"),
            #         ])
            
            
        ], style={'float':'left', 'width':'8%', 'border-right':'1px solid black', 'font-size':'17px','color':'dimgray'})  
        
        ]),
        
        
    html.Div(children=[
        html.Div(children=[        
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
            dcc.Tab(label='업종별 온라인 시장 현황', value='tab-1'),
            dcc.Tab(label='브랜드별 시장 포지션', value='tab-2'),
            dcc.Tab(label='브랜드별 판매 채널', value='tab-3'),
        ]),
        html.Div(id='tabs-example-content-1'),        

        ], style={'float':'left', 'width':'80%','font-size':'20px'})     
         
    ],)
    
])



print(id)


# @app.callback(
#     Output("small-checklist", "value"),
#     Output("large-checklist", "value"),
#     Input("small-checklist", "value"),
#     Input("large-checklist", "value"),
# )
# def sync_checklists(small_selected, large_selected):
#     ctx = callback_context
#     input_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     if input_id == "small-checklist":
#         large_selected = ["All"] if set(small_selected) == set(small) else []
#         # print(small_selected)
#         # print(small)
#         # print(large_selected)
#     else:
#         small_selected = small if large_selected else []
#     return small_selected, large_selected

@app.callback(
    
    Output("cat_small_0", "value"),
    Output("cat_large_0", "value"),
    Input("cat_small_0", "value"),
    Input("cat_large_0", "value"),
)
def sync_checklists_2(small_selected, large_selected):
    ctg = callback_context
    input_id = ctg.triggered[0]["prop_id"].split(".")[0]
    # print(input_id)

    if input_id == "cat_small_0":
        large_selected = list(category.keys())[0] if set(small_selected) == set(category.get('가구')) else []
        # print(small_selected)
        # print(category.get('가구'))
        # print(large_selected)
    else:
        small_selected = category.get('가구') if large_selected else []
    return small_selected, large_selected



# @app.callback(
#     for index,(k,v) in enumerate(category.items()):
        
        


# Output("cat_small_0", "value"),
# Output("cat_large_0", "value"),
# Input("cat_small_0", "value"),
# Input("cat_large_0", "value"),
# )

# def sync_checklists_2(small_selected, large_selected):
#     ctg = callback_context
#     input_id = ctg.triggered[0]["prop_id"].split(".")[0]
#     # print(input_id)

#     if input_id == "cat_small_0":
#         large_selected = list(category.keys())[0] if set(small_selected) == set(category.get('가구')) else []
#         # print(small_selected)
#         # print(category.get('가구'))
#         # print(large_selected)
#     else:
#         small_selected = category.get('가구') if large_selected else []
#     return small_selected, large_selected



# def update(ignore):
#     return np.random.uniform()

# for i in range(20):
#     app.callback(
#         dash.dependencies.Output('input %i' % i, 'value'),
#         [dash.dependencies.Input('button populate', 'n_clicks')]
#     )(update)


# ---
# def make_checklist(category):
#     return html.Div(children=[
#         dcc.Checklist([k], [], id='cat_large_'+ str(index)),
#         html.Div(children=[
#             dcc.Checklist(v, [], id='cat_small_'+ str(index)),
#             ], style={'text-indent':'15px'}),
#         html.Br(),
#     ])
        
# checklists = []
# for index,(k,v) in enumerate(category.items()):
#     # print(index, k,v)
#     checklists.append(make_checklist(enumerate(category.items())))





# @app.callback(
#     Output('test_output', 'children'),
#     Input('cat_small_0','value')
# )

# def test_output(value):
#     return f'You have selected {value}'

### 탭
@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week,y=sum_prc,name='매출총합',text=sum_prc,textposition='auto',marker_color='rgb(55, 83, 109)',customdata=date_count,
                             hovertemplate="매출: %{y} (만)원<br>건수: %{customdata} 건",
                                    ))
        fig.add_trace(go.Bar(x=week,y=date_count,name='매출건수',text=date_count,textposition='outside',marker_color='rgb(26, 118, 255)'))
        fig.update_layout(
                        # title='2022년 업종별 온라인 시장 현황 [주별]',titlefont_size=20,                      
                        # title=go.layout.Title(text="2022년 업종별 온라인 시장 현황 [주별]", font=dict(family="Courier New, monospace",size=18,color="RebeccaPurple")),
                        margin=go.layout.Margin(t=0,b=0,r=0),                
                        plot_bgcolor='rgba(243, 249, 252, 0.92)',
                        xaxis=dict(title='주차',titlefont_size=10,tickfont_size=14),
                        yaxis=dict(title='단위:천만',titlefont_size=12,tickfont_size=14),
                        legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
                        barmode='group',
                        bargap=0.2, # gap between bars of adjacent location coordinates.
                        bargroupgap=0.2, # gap between bars of the same location coordinate.
                        height=385
                        
                        )
        
        
        
        return html.Div([
            
            html.Div(children=[
                html.P(children=["2022년 업종별 온라인 시장 현황 [월별]"],),
            ],style={'background-color':'Gainsboro',
                     'border-radius':'50px',
                     'width':'40%',
                     'text-indent':'55px',
                     'margin-left':'30px',
                     'margin-top':'20px',
                     'font-weight':'bold',
                     'font-size':'20px',
                     'color':'dimgray'
                     }),
            
            html.Div(children=[           
                    dcc.Graph(figure=fig)
                    ], style={'height':'30%'}),
            
            
            html.Div(children=[
                html.P(children=["2022년 업종별 온라인 시장 현황 [주별]"],),
            ],style={'background-color':'Gainsboro',
                     'border-radius':'50px',
                     'width':'40%',
                     'text-indent':'55px',
                     'margin-left':'30px',
                     'margin-top':'20px',
                     'font-weight':'bold',
                     'font-size':'20px',
                     'color':'dimgray'
                     }),
            
            
            html.Div(children=[            
                    # html.H3('Tab content 2'),
                    dcc.Graph(figure=fig)
                    ], style={'height':'30%'})
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
        # fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week,y=sum_prc,name='매출총합',text=sum_prc,textposition='auto',marker_color='rgb(26, 118, 255)'))
        fig.update_layout(
                        margin=go.layout.Margin(t=0,r=0),
                        height=300                     
                        )   
        return html.Div([
            
            html.H3('Tab content 3'),   
            dcc.Graph(figure=fig)


        ]),        
        






if __name__ == '__main__':
    app.run_server(host='0.0.0.0')




# 매출 / 전주랑 비교 / 브랜드별 / 품목별 / top5 / ..