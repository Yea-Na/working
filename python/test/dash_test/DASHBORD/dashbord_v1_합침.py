
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from base64 import encode
from pydoc import classname
from tkinter.font import Font
from turtle import bgcolor, color, left, width
from unicodedata import category
from dash import dash, dcc, html, Input, Output, State, callback_context, dash_table
from matplotlib import backend_tools, style
from matplotlib.font_manager import afmFontProperty
from matplotlib.pyplot import legend, margins
from numpy import pad, size
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import openpyxl
import datetime
from plotly.subplots import make_subplots
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
###
print(os.getcwd())
#4,5,6,7월 소파 구매 데이터

df_base = pd.read_csv('./data/df_base.csv')

brand_list = ['자코모', '에싸','까사미아', '일룸', '알로소','한샘', '리바트', '에몬스']
store_list = ['오늘의집','한샘몰','롯데ON','SSG닷컴','GS Shop(TV쇼핑)','NS홈쇼핑(신규)']


category = {
    '가구':['침대', '소파', '책상', '기타'], 
    '패션':['원피스', '재킷', '팬츠', '셔츠', '블라우스','아우터','기타' ],
    '뷰티':['스킨케어', '메이크업'],
    '식음료':['간편식', '음료','간식', '양념', '기타']    
}



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



##############   자주 쓸 오브젝트들 재사용

### 사이드바 체크리스트 
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


### 타이틀 스타일
def title_style(title):
    return html.Div(children=[
                html.P(children=[title]),
            ],style={'background-color':'Gainsboro',
                     'border-radius':'50px',
                     'width':'40%',
                     'text-indent':'55px',
                     'margin-left':'30px',
                     'margin-top':'20px',
                     'font-weight':'bold',
                     'font-size':'20px',
                     'color':'dimgray'
                     })


#######   날짜선택 드롭다운
def date_select_dropdown(year_id, month_id, week_id):
    return html.Div([
            #연도 선택
            dcc.Dropdown(['2021','2022'], '2022',
            id=year_id,
            style={'float' : 'left','width' : '100px','margin-right' : '10px','margin-left' : '10px'}),
            
            #월 선택 > 우선은 리스트 추후 df['month']의 개별값으로
            dcc.Dropdown(
                list(range(1,13)), 4,
                id = month_id,
                style = {'float' : 'left','width' : '100px','margin-right' : '10px','margin-left' : '10px'}
                ),
            #주차 선택
            dcc.Dropdown(
                    list(range(1,6)), 1,
                id = week_id,
                style = {'float' : 'left','width' : '100px','margin-right' : '10px','margin-left' : '10px'}
                )
            ],id='periodselect', style = {'height' : '40px', 'margin' : 'auto'}
            )
            
            

            

                




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
            
        ], style={'float':'left', 'width':'8%', 'border-right':'1px solid black', 'font-size':'17px','color':'dimgray','margin-left' : '10px'})  
        
        ]),
        
        
    html.Div(children=[
        html.Div(children=[
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
            dcc.Tab(label='업종별 온라인 시장 현황', value='tab-1'),
            dcc.Tab(label = '브랜드별 판매 시장 현황', value='tab-2',children=
                dcc.Tabs(id='tab-2sub', vertical=False, value='tab-2sub',children=
                    [dcc.Tab(label='전체브랜드',value = 'brandall'),
                    dcc.Tab(label='경쟁브랜드',value = 'brandcomp'),
                    dcc.Tab(label='개별브랜드',value = 'brandindi')])),
            dcc.Tab(label='브랜드별 판매 채널', value='tab-3')
            ])]),
    html.Div(id='tabs-example-content-1', style={'float':'left', 'width':'80%','font-size':'20px'})])
])


@app.callback(    
    Output("cat_small_0", "value"),
    Output("cat_large_0", "value"),
    Input("cat_small_0", "value"),
    Input("cat_large_0", "value"),
)
def sync_checklists_2(small_selected, large_selected):
    ctg = callback_context
    input_id = ctg.triggered[0]["prop_id"].split(".")[0]

    if input_id == "cat_small_0":
        large_selected = list(category.keys())[0] if set(small_selected) == set(category.get('가구')) else []

    else:
        small_selected = category.get('가구') if large_selected else []
    return small_selected, large_selected



        


######## 탭
@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    ### 월별 그래프 객체정의

    df_month = pd.read_csv('./data/df_month.csv', encoding='utf-8-sig')
    month = list(df_month['month'].astype('str'))
    month_sum_prc=list(df_month['sum_refix_prc'])
    month_date_count=list(df_month['sum_count'])
    
    
    ### 월별 투명도
    month_colors_1 = ['rgb(123,213,195)'] * 12
    month_colors_2 = ['gray'] * 12    
    month_last_year = list(df_month[df_month['year']==datetime.datetime.now().year-1]['month'])

    for i in month_last_year:
        month_colors_1[i-1] = 'rgba(123,213,195,0.3)'
        month_colors_2[i-1] = 'rgba(128,128,128,0.3)'
    
    
    ### 주별 그래프 객체정의
    df_week = pd.read_csv('./data/df_week.csv', encoding='utf-8-sig')
    week = list(df_week['week'].astype('str'))
    week_sum_prc=list(df_week['sum_refix_prc'])
    week_date_count=list(df_week['sum_count'])
    
    ## 주별 투명도
    week_colors_1 = ['rgb(115,198,217)'] * 54
    week_colors_2 = ['gray'] * 54
    last_year_week = list(df_week[df_week['year']==datetime.datetime.now().year-1]['week'])
    
    for i in last_year_week:
        week_colors_1[i] = 'rgba(115,198,217,0.3)'
        week_colors_2[i] = 'rgba(128,128,128,0.3)'
    
    
    if tab == 'tab-1':
        fig_1 = go.Figure(data = [go.Bar(x=month,y=month_sum_prc,name='매출총합',marker_color=month_colors_1,customdata=month_date_count,text=month_sum_prc,textposition='auto',
                                hovertemplate="매출: %{y} 원<br>건수: %{customdata:,d} 건", yaxis='y',offsetgroup=1),
                                go.Bar(x=month,y=month_date_count,name='매출건수',marker_color=month_colors_2,customdata=month_sum_prc,text=month_date_count,textposition='inside',
                                    hovertemplate="매출: %{customdata:,d} 원<br>건수: %{y} 건",yaxis='y2',offsetgroup=2)]
                                )
        fig_1.update_layout(
                        margin=go.layout.Margin(t=0,b=0,r=0),                
                        plot_bgcolor='rgba(243, 249, 252, 0.92)',
                        xaxis=dict(title='월',titlefont_size=12,tickfont_size=8),
                        yaxis1= dict(title='매출 총합(단위 : 억원)',titlefont_size=13,tickfont_size=8,tickformat=',',tickvals=[5000000000,10000000000,15000000000,20000000000,25000000000,30000000000],ticktext=[50,100,150,200,250,300]),
                        yaxis2=dict(title='매출 건수', overlaying='y',side='right', titlefont_size=13,tickfont_size=8,tickformat=','),
                        legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
                        barmode='group',
                        bargap=0.25, # gap between bars of adjacent location coordinates.
                        bargroupgap=0, # gap between bars of the same location coordinate.
                        height=385
                        )      
          
        fig_2 = go.Figure(data = [go.Bar(x=week,y=week_sum_prc,name='매출총합',marker_color=week_colors_1,customdata=week_date_count,
                                hovertemplate="매출: %{y} 원<br>건수: %{customdata:,d} 건", yaxis='y',offsetgroup=1),
                                go.Bar(x=week,y=week_date_count,name='매출건수',marker_color=week_colors_2,customdata=week_sum_prc,
                                    hovertemplate="매출: %{customdata:,d} 원<br>건수: %{y} 건",yaxis='y2',offsetgroup=2)]
                                )
        fig_2.update_layout(
                        margin=go.layout.Margin(t=0,b=0,r=0),                
                        plot_bgcolor='rgba(243, 249, 252, 0.92)',
                        xaxis=dict(title='주차',titlefont_size=12,tickfont_size=8),
                        yaxis1= dict(title='매출 총합(단위 : 억원)',titlefont_size=13,tickfont_size=8,tickformat=',',tickvals=[2000000000,4000000000,6000000000,8000000000,10000000000],ticktext=[20,40,60,80,100]),
                        yaxis2=dict(title='매출 건수', overlaying='y',side='right', titlefont_size=13,tickfont_size=8,tickformat=','),
                        legend=dict(x=0,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
                        barmode='group',
                        bargap=0.25, # gap between bars of adjacent location coordinates.
                        bargroupgap=0, # gap between bars of the same location coordinate.
                        height=385
                        )
        
        

        
        return [html.Div([
            
            title_style("2022년 업종별 온라인 시장 현황 [월별]"),
            
            html.Div(children=[           
                    dcc.Graph(figure=fig_1)
                    ], style={'height':'30%'}),
            
            title_style("2022년 업종별 온라인 시장 현황 [주별]"),           
            
            
            html.Div(children=[            
                    dcc.Graph(figure=fig_2)
                    ], style={'height':'30%'})
        ])]
        
        
    elif tab == 'tab-2':
        
        
            # TODO : 연도 선택도 함수에 포함시킬것
        
        return html.Div([
            
            date_select_dropdown('brand_mk1_year','brand_mk1_month','brand_mk1_week'),
            
            title_style('브랜드별 온라인 시장 현황'),
            
            html.Div(children=[            
            dcc.Graph(id='fig_3')
            ], style={'height':'30%'}),
            
            title_style('브랜드별 온라인 시장점유 현황'),
            
            html.Div(children=[            
            dcc.Graph(id='fig_4')
            ], style={'height':'30%'})
            
            
        ], id = 'tab2-sector')
        
        
        
        
    elif tab == 'tab-3':
        #Dropdown 활용 - 활용 데이터 : df_heat
        # 브랜드별 판매 채널 리스트
    
        return html.Div([
            title_style('  브랜드별 주요 판매 채널'),
            
            date_select_dropdown('brand_ch_year','brand_ch_month','brand_ch_week'), 
            
            html.Div(dcc.Graph(id = 'fig_8',), style={'height':'30%'})
        ]),        









#새로운 input output 적용 방법
#아래는 예시
'''
@app.callback(Output("내보낼 속성id","내보내고자 하는 값"),Input("받고자하는속성id","받을 참조값"))
'''





###########     fig_3     
@app.callback(
    Output('fig_3', 'figure'),
    Input('brand_mk1_month','value'),
    Input('brand_mk1_week','value'))

def tab2_fig3_data_update(monthdata, weekdata):
    # global data
    df_brand = df_base[(df_base['month'] == monthdata) & (df_base['month_week'] == weekdata)]
    df_brand_sum = df_brand.groupby('brand')['refix_prc'].sum()
    df_brand_sum = pd.DataFrame(df_brand_sum).reset_index()
    df_brand_sum = df_brand_sum.sort_values('refix_prc', ascending = False).head(15)
    
    fig_3 = go.Figure(data = go.Bar(x = df_brand_sum['brand'], y = df_brand_sum['refix_prc']))
    fig_3.update_layout(
            margin=go.layout.Margin(t=0,b=0,r=0),
            legend=dict(x=0.85,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
            height=385,
            width=1300
            )
    return fig_3


#   fig_4
@app.callback(
    Output('fig_4', 'figure'),
    Input('brand_mk1_month','value'),
    Input('brand_mk1_week','value'))

def tab2_fig4_data_update(monthdata, weekdata):
    df_brand = df_base[(df_base['month'] == monthdata) & (df_base['month_week'] == weekdata)]
    #df4['refix_prc'] = df4['refix_prc'].str.strip().str.replace(',','')
    
    df_brand_sum = df_brand.groupby('brand')['refix_prc'].sum()
    df_brand_sum = pd.DataFrame(df_brand_sum).reset_index()
    df_brand_sum = df_brand_sum.sort_values('refix_prc', ascending = False)
    
    df_brand_count = pd.DataFrame(df_brand.groupby('brand')['item_title'].count()).reset_index().sort_values('item_title',ascending = False).head(15)

    sales_total = df_brand_sum['refix_prc'].sum()
    count_total = df_brand_count['item_title'].sum()
    df_brand_sum['salesms'] = (df_brand_sum['refix_prc']/sales_total) * 100
    df_brand_count['countms'] = (df_brand_count['item_title']/count_total) * 100    
    
    
    df_fig_3 = pd.merge(df_brand_count, df_brand_sum,'left', on='brand')
    
    fig_4 = make_subplots(specs=[[{"secondary_y" : True}]])
    fig_4.add_trace(go.Bar(x=df_fig_3['brand'],y=df_fig_3['countms'],name='수량MS',textposition='auto',marker_color='rgb(55, 83, 109)',yaxis='y',offsetgroup=1),secondary_y=False)
    fig_4.add_trace(go.Bar(x=df_fig_3['brand'],y=df_fig_3['salesms'],name='매출MS',marker_color='rgb(255,165,0)',yaxis='y2',offsetgroup=2),secondary_y=True)
    fig_4.update_layout(
                margin=go.layout.Margin(t=0,b=0,r=0),
                legend=dict(x=0.85,y=1.0,bgcolor='rgba(255, 255, 255, 0)',bordercolor='rgba(255, 255, 255, 0)',),
                barmode='group',
                )
    return fig_4



#######   fig_7
#히트맵에 대한 일자 드롭다운 설정 함수
@app.callback(
    Output('fig_8', 'figure'),
    Input('brand_ch_month','value'),
    Input('brand_ch_week','value'))
def tab2_fig4_data_update(monthdata, weekdata):
    # global data
    df_heat = df_base[(df_base['month'] == monthdata) & (df_base['month_week'] == weekdata)]
    df_heat = df_heat[df_heat['brand'].isin(brand_list)]
    df_heat = df_heat[df_heat['dq_client_nm'].isin(store_list)]
    
    df_fig8 = pd.pivot_table(df_heat, values = 'item_title',index = 'brand', columns = 'dq_client_nm', aggfunc = 'count', sort = True)

    fig_8 = px.imshow(df_fig8, text_auto = True, color_continuous_scale="reds")

    return fig_8


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', use_reloader=True)




