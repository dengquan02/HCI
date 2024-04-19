# _*_ coding : utf-8 _*_
# @Time : 2022/6/20 15:21
# @Author : DengQuan

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
import pandas as pd


app = dash.Dash()
df = pd.read_csv("./google-play-store-apps/googleplaystore.csv", encoding="ANSI")
app_name = df['App']
kind = df["Category"].drop_duplicates()
# print(kind.values.T)
kind = np.append((["ALL"]), kind.values.T)
min_time = np.min(df["Last Updated"])
max_time = np.max(df["Last Updated"])
print(min_time, max_time)
var = df["Size"]

gf = df[var.str.contains("k")]['Size'].str.replace('k', "")
gf = gf.astype("float") / 1024
gf = gf.round(2)
gf = gf.reset_index()
j = 0
for i in range(gf.shape[0]):
    # j=i
    for j in range(j, df.shape[0]):
        if gf.iloc[i, 0] == j:
            print(gf.iloc[i, 0])
            df.iloc[j, 4] = gf.iloc[i, 1]
            # j = i
            break
# gff=df[var.str.contains("M")].loc[:,'Size']
print(11)
df["Size"] = df["Size"].str.replace("M", "").str.replace("Varies with device", "NaN").astype("float")
# df["Size"]=df["Size"]
# df['Size'].to_csv('./size1.csv')
df["Last Updated"] = df["Last Updated"].str.replace("-", "").astype("int")
max_date = int(np.max(df["Last Updated"]))
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in kind],
                value='ALL'
            ),
            # dcc.RadioItems(
            #     id='crossfilter-xaxis-type',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear',
            #     labelStyle={'display': 'inline-block'}
            # )
        ],
            style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            # dcc.Dropdown(
            #     id='crossfilter-yaxis-column',
            #     options=[{'label': i, 'value': i} for i in available_indicators],
            #     value='Life expectancy at birth, total (years)'
            # ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['全部', '免费', '付费']],
                value='全部',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='age-count-bar',
            # x="适宜人群", y="安装人数"
            # hoverData={'points': [{'customdata': 'Japan'}]}
        ),
        html.Div(dcc.Slider(
            id='year-slider',
            min=int(np.min(df["Last Updated"])),
            max=int(np.max(df["Last Updated"])),
            value=max_date,
            step=600,
            tooltip="以3个月为单位",
            marks={int(year): int(year) for year in
                   [np.min(df["Last Updated"]), max_date]}
        ), style={'width': '100%', 'padding': '0px 20px 20px 20px'})
    ], style={'width': '49%', 'display': 'inline-block', 'margin-top': '20px'}),
    html.Div([
        html.Button('重置', id='button'),
        html.Div([
            dcc.Graph(id='score-commit'),

        ], style={'display': 'inline-block', 'width': '100%'}),
        html.Div([
            dcc.Graph(id='require-size'),

        ], style={'display': 'inline-block', 'width': '100%'}),

    ], style={'float': 'right', 'width': '49%'})

])


def calc_bar(xx, yy):
    xy = np.append(xx, yy, axis=0)
    s_x = np.unique(xx)
    s_y = []
    for s in s_x:
        i = 0
        for k in range(xy.shape[1]):
            if xy[0][k] == s:
                i += xy[1][k]
        s_y.append(i)
    return s_x, s_y


@app.callback(
    dash.dependencies.Output('age-count-bar', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     # dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     # dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('year-slider', 'value')
     ])
def update_graph(xaxis_column_name,
                 # yaxis_column_name,
                 # xaxis_type,
                 yaxis_type,
                 year_value
                 ):
    print(year_value)
    dff = df[df["Last Updated"] <= year_value]
    # dff = df[df['Year'] == year_value]
    if xaxis_column_name == 'ALL':
        if yaxis_type == '全部':
            xx = [dff['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in dff['Installs']]]

            # print(s_x, s_y)

            # yy=np.sum(df[''])
        elif yaxis_type == '免费':
            xx = [dff[dff['Type'] == 'Free']['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in dff[dff['Type'] == 'Free']['Installs']]]
        else:
            xx = [dff[dff['Type'] == 'Paid']['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in dff[dff['Type'] == 'Paid']['Installs']]]
    else:
        if yaxis_type == '全部':
            xx = [dff[dff["Category"] == xaxis_column_name]['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in
                   dff[dff["Category"] == xaxis_column_name]['Installs']]]
        elif yaxis_type == '免费':
            df1 = dff[dff["Category"] == xaxis_column_name]
            # print(df1)
            xx = [df1[df1['Type'] == 'Free']['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in
                   df1[df1['Type'] == 'Free']['Installs']]]
        else:
            df1 = dff[dff["Category"] == xaxis_column_name]
            # print(df1)
            xx = [df1[df1['Type'] == 'Paid']['Content Rating']]
            yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in
                   df1[df1['Type'] == 'Paid']['Installs']]]
    s_x, s_y = calc_bar(xx, yy)
    return {
        'data': [go.Bar(
            x=s_x,
            y=s_y,
            name="age_num",
            text=s_x,
            # legendgrouptitle="年龄限制-下载量",
            # mode='markers',
            marker={
                # 'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            plot_bgcolor="snow",
            # color
            title="年龄限制-下载量关系图",
            xaxis={
                'title': '年龄限制',
            },
            yaxis={
                'title': "下载量",
            },
            margin={'l': 50, 'b': 50, 't': 30, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Rating'],
            y=dff['Reviews'],
            mode='markers',
            hovertext='名称：' + dff['App'],
            # hovertemplate='<p>名称:'+dff['App']+'</p><br><p>评分:'+str(dff['Rating'])+'</p>',
            # hoverinfo=dff['App'],
            # customdata=dff['App'],
            xhoverformat="1",
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            plot_bgcolor="snow",
            height=450,
            margin={'l': 50, 'b': 50, 'r': 10, 't': 10},
            annotations=[{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            yaxis={'title': '评论数', },
            xaxis={'showgrid': False, 'title': '评分', },
        )
    }


@app.callback(dash.dependencies.Output('age-count-bar', 'hoverData'), [dash.dependencies.Input('button', 'n_clicks')])
def update_output(n_clicks):
    # n_clicks = 0 if not n_clicks else n_clicks
    print("222")
    return 'T'


# @app.callback(dash.dependencies.Input('age-count-bar', 'hoverData'),
#               [dash.dependencies.Input('button', 'n_clicks'),
#                # dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#                # dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#                ])
# def update_output2(n_clicks):
#     # n_clicks = 0 if not n_clicks else n_clicks
#     print("333")
#     # if xaxis_column_name == 'ALL':
#     #     if yaxis_type == '全部':
#     #         dff = df
#     #
#     #         # print(s_x, s_y)
#     #
#     #         # yy=np.sum(df[''])
#     #     elif yaxis_type == '免费':
#     #         dff = df[df['Type'] == 'Free']
#     #         # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Free']['Installs']]]
#     #     else:
#     #         dff = df[df['Type'] == 'Paid']
#     #         # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Paid']['Installs']]]
#     # else:
#     #     if yaxis_type == '全部':
#     #         dff = df[df["Category"] == xaxis_column_name]
#     #     elif yaxis_type == '免费':
#     #         df1 = df[df["Category"] == xaxis_column_name]
#     #         # print(df1)
#     #         dff = df1[df1['Type'] == 'Free']
#     #     else:
#     #         df1 = df[df["Category"] == xaxis_column_name]
#     #         # print(df1)
#     #         dff = df1[df1['Type'] == 'Paid']
#     # title = '<b>评分-评论表</b>'
#     # return create_time_series(dff, yaxis_type, title)
#     return None


@app.callback(
    dash.dependencies.Output('score-commit', 'figure'),
    [dash.dependencies.Input('age-count-bar', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('year-slider', 'value')
     ])
def update_y_timeseries(hoverData, xaxis_column_name, yaxis_type, year_value):
    dft = df[df["Last Updated"] <= year_value]
    print("111", hoverData)
    if hoverData == None or hoverData == 'T':
        if xaxis_column_name == 'ALL':
            if yaxis_type == '全部':
                dff = dft

                # print(s_x, s_y)

                # yy=np.sum(df[''])
            elif yaxis_type == '免费':
                dff = dft[dft['Type'] == 'Free']
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Free']['Installs']]]
            else:
                dff = dft[dft['Type'] == 'Paid']
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Paid']['Installs']]]
        else:
            if yaxis_type == '全部':
                dff = dft[dft["Category"] == xaxis_column_name]
            elif yaxis_type == '免费':
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Free']
            else:
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Paid']
        title = '<b>{}</b><br>{}'.format('总体', '评分-评论表')
    else:
        if xaxis_column_name == 'ALL':
            if yaxis_type == '全部':
                dff = dft[dft["Content Rating"] == hoverData["points"][0]["label"]]
            elif yaxis_type == '免费':
                dff = dft[dft['Type'] == 'Free']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Free']['Installs']]]
            else:
                dff = dft[dft['Type'] == 'Paid']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Paid']['Installs']]]
        else:
            if yaxis_type == '全部':
                dff = dft[dft["Category"] == xaxis_column_name]
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
            elif yaxis_type == '免费':
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Free']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
            else:
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Paid']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
        title = '<b>{}</b><br>{}'.format(hoverData["points"][0]["label"], '评分-评论表')
    # country_name = hoverData['points'][0]['customdata']
    # dff = df[df['Country Name'] == country_name]
    # dff = dff[dff['Indicator Name'] == xaxis_column_name]
    # title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    # return None
    return create_time_series(dff, yaxis_type, title)


def create_time_series2(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Android Ver'],
            y=np.sort(dff['Size']),
            mode='markers',
            hovertext='名称：' + dff['App'],
            # hovertemplate='<p>名称:'+dff['App']+'</p><br><p>评分:'+str(dff['Rating'])+'</p>',
            # hoverinfo=dff['App'],
            # customdata=dff['App'],
            xhoverformat="1",
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            plot_bgcolor="snow",
            height=450,
            margin={'l': 50, 'b': 100, 'r': 10, 't': 10},
            annotations=[{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            yaxis={'title': '软件大小  单位M', },
            xaxis={'showgrid': False, 'title': '最低要求', 'tickangle': -45},
        )
    }


@app.callback(
    dash.dependencies.Output('require-size', 'figure'),
    [dash.dependencies.Input('age-count-bar', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('year-slider', 'value')
     ])
def update_y_timeseries(hoverData, xaxis_column_name, yaxis_type, year_value):
    dft = df[df["Last Updated"] <= year_value]
    print("111", hoverData)
    if hoverData == None or hoverData == 'T':
        if xaxis_column_name == 'ALL':
            if yaxis_type == '全部':
                dff = dft

                # print(s_x, s_y)

                # yy=np.sum(df[''])
            elif yaxis_type == '免费':
                dff = dft[dft['Type'] == 'Free']
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Free']['Installs']]]
            else:
                dff = dft[dft['Type'] == 'Paid']
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Paid']['Installs']]]
        else:
            if yaxis_type == '全部':
                dff = dft[dft["Category"] == xaxis_column_name]
            elif yaxis_type == '免费':
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Free']
            else:
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Paid']
        title = '<b>{}</b><br>{}'.format('总体', '要求-大小表')
    else:
        if xaxis_column_name == 'ALL':
            if yaxis_type == '全部':
                dff = dft[dft["Content Rating"] == hoverData["points"][0]["label"]]
            elif yaxis_type == '免费':
                dff = dft[dft['Type'] == 'Free']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Free']['Installs']]]
            else:
                dff = dft[dft['Type'] == 'Paid']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
                # yy = [[int(float(i.split("+")[0].replace(',', ""))) for i in df[df['Type'] == 'Paid']['Installs']]]
        else:
            if yaxis_type == '全部':
                dff = dft[dft["Category"] == xaxis_column_name]
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
            elif yaxis_type == '免费':
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Free']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
            else:
                df1 = dft[dft["Category"] == xaxis_column_name]
                # print(df1)
                dff = df1[df1['Type'] == 'Paid']
                dff = dff[dff["Content Rating"] == hoverData["points"][0]["label"]]
        title = '<b>{}</b><br>{}'.format(hoverData["points"][0]["label"], '要求-大小表')
    # country_name = hoverData['points'][0]['customdata']
    # dff = df[df['Country Name'] == country_name]
    # dff = dff[dff['Indicator Name'] == xaxis_column_name]
    # title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    # return None
    return create_time_series2(dff, yaxis_type, title)


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server()
