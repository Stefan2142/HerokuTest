#!/usr/bin/python3.5.9
# from flask import Flask
# app = Flask(__name__)
# # application = app # our hosting requires application in passenger_wsgi
 
# @app.route("/")
# def hello():
#     return "This is Hello World!\n"
 
# if __name__ == "__main__":
#     app.run(port=80)



# # PLOTLY - DASH APP

# from flask import Flask
# server = Flask(__name__)

# server.suppress_callback_exceptions = True

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')


# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


app = dash.Dash(__name__)

server = app.server
# app.layout = html.Div([
#     html.H4(children='US Agriculture Exports (2011)'),
#     generate_table(df)
# ])

app.layout = html.Div([

    html.H1('Web Application Dashboards widh Dash', style = {'text-align': 'center'}),

    dcc.Dropdown(id='slct_year',
    options=[
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018}],

        multi=False,
        value=2015,
        style={'width':'40%'}
        ),

    html.Div(id='output-container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


if __name__ == '__main__':
    app.run_server()
