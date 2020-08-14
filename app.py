# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
companies = ['Deloitte Haskin', 'Deloitte Touche Toumatsu', 'Deloitte and Co.']

# Put names of firms instead ^^^

ratios = ['open_ratio', 'click_ratio']

# Put column names of ratio variables instead ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6


df = pd.read_csv('ratios.csv')

# Ye file same folder mai daal de

fig = px.scatter(df[df['Company'] == companies[0]],
                 x='Department', y=ratios[0], color='Department', )
val = 'Chart of {} for {}'.format(ratios[0], companies[0])
app.layout = html.Div([
])

app.layout = html.Div(style={
    'background-image': 'url("https://images.unsplash.com/photo-1534237710431-e2fc698436d0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2134&q=80")',
    'background-repeat': 'no-repeat',
    'background-position': 'center',
    'background-size': '1920px 2880px'
},
    children=[
        html.H1(children='Dashboard of ratios across firms'),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-company',
                options=[{'label': i, 'value': i} for i in companies],
                value=companies[0]
            ),
        ],
            style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-variable',
                options=[{'label': i, 'value': i} for i in ratios],
                value=ratios[0],
            ),
        ],
            style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
            dcc.Markdown(children=val,
                         id='crossfilter-title',
                         # value=val,
                         # style={'width': '30%', 'display': 'inline-block','outline-width':0}
                         )
        ],
            style={'margin-top': '10px', 'margin-left': '100px', 'font-size': 24}
        ),
        html.Div([
            dcc.Graph(
                id='crossfilter-indicator-scatter',
                figure=fig,
                # layout=fig.layout,
            ),
        ],
            style={'width': '50%', 'display': 'inline-block', 'margin-top': '150px', 'margin-left':'25%'}),

])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-company', 'value'),
     dash.dependencies.Input('crossfilter-variable', 'value')])
def update_graph(company, variable):
    dff = df[df['Company'] == company]
    print(dff)
    fig = px.scatter(dff, x='Department',
                     y=variable,
                     color='Department',
                     size='Email Status',
                    #  hover_data={'Email Status': True, 'Department': False},
                     # hover_name=dff[variable]
                     )

    fig.update_xaxes(title={'text': company})
    fig.update_yaxes(title=variable)
    fig.update_layout(
        title_text='Chart of {} for {}'.format(variable, company))
    fig.update_layout(
        margin={'l': 50, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig


@app.callback(
    dash.dependencies.Output('crossfilter-title', 'children'),
    [dash.dependencies.Input('crossfilter-company', 'value'),
     dash.dependencies.Input('crossfilter-variable', 'value')])
def update_title(company, variable):
    return 'Chart of {} for {}'.format(variable, company)


if __name__ == '__main__':
    app.run_server(debug=True)
