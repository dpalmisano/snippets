from flask import Flask

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import random

server = Flask('UK schools cluster analysis')
app = dash.Dash('UK schools cluster analysis', server=server, url_base_pathname='/', csrf_protect=False)


df = pd.read_csv('data/derived/2016-2017_england_clusters.csv')

available_indicators = df.columns.tolist()
available_indicators.remove('urn')
available_indicators.remove('name')
available_indicators.remove('cluster')

indicators_description = {
    'on free meal': 'Absolute number of pupils on free meal.',
    'teacher headcount': 'Absolute number of full time teachers.',
    'idaci score': 'The IDACI (Income deprivation affecting children index) is an index of deprivation used in the United Kingdom. Higher values mean higer levels of deprivation.',
    'english first language': 'Absolute number of pupils with English as first language.',
    'girls on roll': 'Absolute number of girls on roll.',
    'english not first language': 'Absolute number of pupils with English first language.',
    'total income pp': 'Total school income per pupil.',
    'total pupils on roll': 'Total number of pupils on roll.',
    'boys on roll': 'Absolute number of boys on roll.',
    'mean salary fte': 'Mean salary of school full time employees.',
    'total expenditure pp': 'Total school expenditure per pupil.',
    'income score': 'Index describing the level of income in the LSOA where the school is located.',
    'empl score': 'Index describing the level of employment in the LSOA where the school is located.',
    'perc pupils meeting reading standard': 'Percentage of pupils meeting key stage 2 standards results for reading.',
    'perc pupils meeting math standard': 'Percentage of pupils meeting key stage 2 standards results for math.',
    'perc pupils meeting grammar standard': 'Percentage of pupils meeting key stage 2 standards results for grammar.',
    'perc pupils meeting writing standard': 'Percentage of pupils meeting key stage 2 standards results for writing.',
    'avg reading scaled score': 'School average reading scaled score for the given school.',
    'avg grammar scaled score': 'School average grammar scaled score for the given school.',
    'avg math scaled score': 'School average math scaled score for the given school.'
}

app.layout = html.Div([

    html.Div([

        html.Div([
            html.H1('UK Schools cluster analysis'),
            html.Div([
                'an experiment by ',
                html.A('@dpalmisano', href='http://twitter.com/dpalmisano'),
                ' built with ',
                html.A('SherlockML', href='http://sherlockml.com'),
                ' ❤️ '
            ], style={'padding-bottom': '2em'}),
            html.Div([
                'This simple app shows an ',
                html.A('Agglomerative Clustering', href='http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html', target="_blank"),
                ' analysis on some features of more than 7000 UK schools.',
                html.P([
                    'Census, pupil performances, workforce and other features about schools are collected from the gov.uk Comparing School website.',
                    html.Br(),
                    'Data about deprivation is taken from english indices of deprivation 2015.',
                    html.Br(),
                    'The color of a data point shows in which cluster the school belongs to.',
                    html.Br(),
                    'Code can be found ',
                    html.A('here', href='https://github.com/dpalmisano/snippets/tree/master/uk-schools-cluster-analysis', target='_blank')
                ]),
                html.P('The features available is not an exhaustive list and might change in further releases.')
            ]),
        ], style={'padding-left': '8em', 'padding-right': '8em', 'padding-bottom': '2em'}),

        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='on free meal'
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Log',
                    labelStyle={'display': 'inline-block'}
                ),
                html.Div(id='xaxis-expl', style={'width': '96%', 'text-align': 'center', 'margin-top': '0.7em', 'box-shadow': '1px 1px 6px 0px #777'})
            ], style={'width': '100%'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='teacher headcount'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Log',
                    labelStyle={'display': 'inline-block'}
                ),
                html.Div(id='yaxis-expl', style={'width': '96%', 'text-align': 'center', 'margin-top': '0.7em', 'box-shadow': '1px 1px 6px 0px #777'})
            ], style={'width': '100%'}),

            html.Div([
                dcc.Dropdown(
                    id='zaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='idaci score'
                ),
                dcc.RadioItems(
                    id='zaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                ),
                html.Div(id='zaxis-expl', style={'width': '96%', 'text-align': 'center', 'margin-top': '0.7em', 'box-shadow': '1px 1px 6px 0px #777'})
            ], style={'width': '100%'})

        ], style={'display': 'flex', 'justify-content': 'space-between'})
    ]),

    dcc.Graph(id='indicator-graphic', style={ 'height': 600, 'width': 1000 })

], style={'font-family': 'Courier', 'font-size': '0.8em', 'color': 'grey'})

app.title = 'UK Schools analysis with Agglomerative clustering.'

@app.callback(
    dash.dependencies.Output(component_id='xaxis-expl', component_property='children'),
    [dash.dependencies.Input('xaxis-column', 'value')]
)
def update_x_axis_explaination(input_value):
    return indicators_description[input_value]

@app.callback(
    dash.dependencies.Output(component_id='yaxis-expl', component_property='children'),
    [dash.dependencies.Input('yaxis-column', 'value')]
)
def update_y_axis_explaination(input_value):
    return indicators_description[input_value]

@app.callback(
    dash.dependencies.Output(component_id='zaxis-expl', component_property='children'),
    [dash.dependencies.Input('zaxis-column', 'value')]
)
def update_z_axis_explaination(input_value):
    return indicators_description[input_value]

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('zaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('zaxis-type', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, zaxis_column_name,
                 xaxis_type, yaxis_type, zaxis_type):

    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=-1.25, y=-1.25, z=1.75)
    )

    return {
        'data': [go.Scatter3d(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            z=df[zaxis_column_name],
            text=df['name'],
            mode='markers',
            marker={
                'size': 2,
                'color': df['cluster'],
                'colorscale': [[0, 'rgb(18, 90, 206)'], [0.5, 'rgb(135, 135, 10)'], [1, 'rgb(175, 49, 17)']],
                'line': {'width': 0.1, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            font={
                'family':'Courier New, monospace',
                'size':12,
                'color':'#7f7f7f'
            },
            scene=go.Scene(
                camera=camera,
                xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
                },
                yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
                zaxis={
                'title': zaxis_column_name,
                'type': 'linear' if zaxis_type == 'Linear' else 'log'
                }),
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest',
            hoverlabel={
                'bgcolor': 'gray',
                'font': {'color': 'black'}
            }
        )
    }


if __name__ == '__main__':
    app.run_server()
