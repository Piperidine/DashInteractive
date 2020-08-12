# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


app = dash.Dash(__name__)
cities = ['Mumbai', 'Delhi', 'Chennai']

## Put names of firms instead ^^^ 

ratios = ['open_ratio', 'click_ratio']

# Put column names of ratio variables instead ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6


df = pd.read_excel('ratios.xlsx')

# Ye file same folder mai daal de

fig = px.bar(df, x='Grade', y=ratios[0], color="Grade", barmode="group")
val = 'Chart of {} for {}'.format(ratios[0], cities[0])
app.layout = html.Div([
])

app.layout = html.Div(children=[
    html.H1(children='Dashboard of ratios across firms'),
    html.Div([
        dcc.Dropdown(
            id='crossfilter-city',
            options=[{'label': i, 'value': i} for i in cities],
            value=cities[0]
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
        style={'width': '100%', 'display': 'inline-block', 'margin-top': '100px'}),

])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-city', 'value'),
     dash.dependencies.Input('crossfilter-variable', 'value')])
def update_graph(city, variable):
    dff = df[df['City'] == city]

    fig = px.bar(dff, x='Grade',
                 y=variable,
                 color='Grade',
                 # hover_name=dff[variable]
                 )

    fig.update_xaxes(title={'text': city})
    fig.update_yaxes(title=variable)
    fig.update_layout(title_text='Chart of {} for {}'.format(variable, city))
    fig.update_layout(margin={'l': 300, 'b': 40, 't': 10, 'r': 300}, hovermode='closest')
    return fig


@app.callback(
    dash.dependencies.Output('crossfilter-title', 'children'),
    [dash.dependencies.Input('crossfilter-city', 'value'),
     dash.dependencies.Input('crossfilter-variable', 'value')])
def update_title(city, variable):
    return 'Chart of {} for {}'.format(variable, city)


if __name__ == '__main__':
    app.run_server(debug=True)
