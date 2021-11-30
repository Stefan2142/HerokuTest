# -*- coding: utf-8 -*-
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import base64
import os
import gspread
from numpy.lib.shape_base import tile
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import datetime as dt
from dash_bootstrap_templates import load_figure_template

# Overwrite your CSS setting by including style locally
colors = {
    "background": "#2D2D2D",
    "text": "#E1E2E5",
    "figure_text": "#ffffff",
    "confirmed_text": "#3CA4FF",
    "deaths_text": "#f44336",
    "recovered_text": "#5A9E6F",
    "highest_case_bg": "#393939",
    'Sasa':'#FF3333',
    'Janko':'#3372FF',
    'Boris':'#33FF51',
}

# Creating custom style for local use
divBorderStyle = {
    "backgroundColor": "#393939",
    "borderRadius": "12px",
    "lineHeight": 0.9,
    "padding-top": "5px",
    "padding-bottom": "5px"
}

# Creating custom style for local use
boxBorderStyle = {
    "borderColor": "#393939",
    "borderStyle": "solid",
    "borderRadius": "10px",
    "borderWidth": 2,
}

tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

def chunker_list(seq, size):
    """
    Returns a list of lists.
    size - how much sub lists we want
    seq - original list
    Usage tmp = list(chunker_list(l, 10))
    """
    return (seq[i::size] for i in range(size))


gc = gspread.service_account(filename="./emailsending-325211-e5456e88f282.json")

# Nabis Dispatch data
sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1rRwdq2otnXI9d3B9LfYRarQl6RxANP0_TqTQLjTY9A8/edit#gid=1032147445"
)
wks = sh.worksheet("Sheet6")

nabis_dispatch_data = pd.DataFrame(
    wks.get_all_records(),
)

wks = sh.worksheet('Hours')
hubstaff_timings_df = pd.DataFrame(wks.get_all_records())
hubstaff_timings_df['Date'] = pd.to_datetime(hubstaff_timings_df['Date'], format = "%d/%m/%Y")
hubstaff_timings_df.rename(columns = {'Date':'HS_Date'}, inplace = True)
nabis_dispatch_data['Total rescheduled']= nabis_dispatch_data['Total rescheduled'].replace("", 0)
nabis_dispatch_data = nabis_dispatch_data.fillna(value="")
nabis_dispatch_data["City"] = nabis_dispatch_data["City"].astype(str)
nabis_dispatch_data["Your name"] = nabis_dispatch_data["Your name"].astype(str)
nabis_dispatch_data = nabis_dispatch_data[nabis_dispatch_data['Total orders'] != '']
nabis_dispatch_data["Total orders"] = nabis_dispatch_data["Total orders"].astype(int)
nabis_dispatch_data["Date"] = pd.to_datetime(
    nabis_dispatch_data.Date, format="%m/%d/%y"
)
nabis_dispatch_data["Weekday"] = nabis_dispatch_data["Date"].dt.day_name()
nabis_dispatch_data.sort_values(by="Date", inplace=True)
names = list(set(nabis_dispatch_data["Your name"].values.tolist()))
nabis_dispatch_data = pd.merge(nabis_dispatch_data, hubstaff_timings_df, how = 'left', left_on = ['Date', 'Your name'], right_on = ['HS_Date', 'Member'])

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

best_members_df = nabis_dispatch_data.groupby(["Your name"]).sum()
best_members_df.reset_index(inplace=True)
best_member = best_members_df.nlargest(1, "Total orders").to_dict("records")[0]
# best_member['Your Name']
# best_member['Total orders']
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    dbc.themes.SUPERHERO,
]
external_stylesheets = [
    "https://codepen.io/unicorndy/pen/GRJXrvP.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title = 'NABIS')
server = app.server
def create_tabs():
    tabs = []

    fig = go.Figure()
        
    def populate(name, x, y):
        fig.add_trace(go.Scatter(x=x, 
                            y=y,
                            mode='lines',
                            name=name,
                            line=dict(color=colors[name], width=4),
                            fill='tozeroy',
                            line_shape='spline'))
    # TOTAL ORDERS
    for name in names:
        populate(name = name, 
            x = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['Date'],
            y = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['Total orders'])

        
    fig.update_layout(
        hovermode="x",
        font=dict(
            family="sans-serif", # Courier New, monospace
            size=14,
            color=colors["figure_text"],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(family="sans-serif", size=12, color=colors["figure_text"]),
            bgcolor="#393939",
            borderwidth=5,
        ),
        paper_bgcolor=colors["background"],
        plot_bgcolor="#393939",
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A", fixedrange = True,  range = [nabis_dispatch_data['Date'].min(), nabis_dispatch_data['Date'].max()])
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange = True)
    tabs.append(dcc.Tab(label='Total orders', value='Total orders', children=[dcc.Graph(figure=fig, config = {'displayModeBar':False, 'scrollZoom':False}, animate = True)], style=tab_style))

    # TOTAL RESCHEDULED
    fig = go.Figure()
    for name in names:
        populate(name = name, 
            x = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['Date'],
            y = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['Total rescheduled'])

        
    fig.update_layout(
        hovermode="x",
        font=dict(
            family="sans-serif", # Courier New, monospace
            size=14,
            color=colors["figure_text"],
        ),
        legend=dict(
            x=0.02,
            y=1,
            traceorder="normal",
            font=dict(family="sans-serif", size=12, color=colors["figure_text"]),
            bgcolor="#393939",
            borderwidth=5,
        ),
        paper_bgcolor=colors["background"],
        plot_bgcolor="#393939",
        margin=dict(l=0, r=0, t=0, b=0),
        height=300,
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A", fixedrange = True,  range = [nabis_dispatch_data['Date'].min(), nabis_dispatch_data['Date'].max()])
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange = True)
    tabs.append(dcc.Tab(label='Total rescheduled orders', value='Total rescheduled orders', children=[dcc.Graph(figure=fig, config = {'displayModeBar':False, 'scrollZoom':False}, animate = True)], style=tab_style))
    
    # Iteration
    for name in names:
        # fig = go.Figure()
        fig = make_subplots(specs=[[{'secondary_y':True}]])

        # temp_df = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date')['Total orders'].sum().reset_index()
        temp_df = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').agg({'Total orders':'sum','DecimalTime':'first','Total rescheduled':'sum'}).reset_index()
        fig.add_trace(
            go.Bar(
                x=temp_df["Date"],
                y=temp_df["DecimalTime"],
                name='Hours',
                marker_color = '#dc3545'
                
            ), secondary_y = False
        )
        fig.add_trace(
            go.Scatter(
                x=temp_df["Date"],
                y=temp_df["Total orders"],
                mode="lines+markers",
                name='Total orders',
                line=dict(color="#33FF51", width=4),
                fill="tozeroy",
                line_shape='spline',
                marker = dict(size = 7, color = 'rgba(255, 182, 193, .9)')
            ), secondary_y = True
        )
        fig.add_trace(
            go.Scatter(
                x=temp_df["Date"],
                y=temp_df["Total rescheduled"],
                mode="lines+markers",
                name='Total rescheduled orders',
                line=dict(color=colors['Sasa'], width=4),
                fill="tozeroy",
                line_shape='spline',
                marker = dict(size = 5, color = 'rgba(255, 182, 193, .9)')
            ), secondary_y = True
        )
        # fig.add_trace(
        #     go.Scatter(
        #         x=temp_df["Date"],
        #         y=temp_df["DecimalTime"],
        #         mode="lines+markers",
        #         name='Hours',
        #         line=dict(color="#dc3545", width=6),
        #         fill="tozeroy",
        #         line_shape='spline'
        #     )
        # )

        fig.update_layout(
            hovermode="x",
            font=dict(
                family="Courier New, monospace",
                size=14,
                color=colors["figure_text"],
            ),
            legend=dict(
                x=0.02,
                y=1,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color=colors["figure_text"]),
                bgcolor="#393939",
                borderwidth=5,
            ),
            paper_bgcolor=colors["background"],
            plot_bgcolor="#393939",
            margin=dict(l=0, r=0, t=0, b=0),
            height=300,
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A", fixedrange = True)
        # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

        fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange = True)
        tabs.append(dcc.Tab(label=name, value=name, children=[dcc.Graph(figure=fig, config = {'displayModeBar':False, 'scrollZoom':False})], style=tab_style))
        
        
        
        
        
    fig = go.Figure()
    for name in names:
        populate(name = name, 
            x = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['Date'],
            y = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date').sum().reset_index()['DecimalTime'])
        
    fig.update_layout(
    hovermode="x",
    font=dict(
        family="sans-serif", # Courier New, monospace
        size=14,
        color=colors["figure_text"],
    ),
    legend=dict(
        x=0.02,
        y=1,
        traceorder="normal",
        font=dict(family="sans-serif", size=12, color=colors["figure_text"]),
        bgcolor="#393939",
        borderwidth=5,
    ),
    paper_bgcolor=colors["background"],
    plot_bgcolor="#393939",
    margin=dict(l=0, r=0, t=0, b=0),
    height=300,
)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A", fixedrange = True,  range = [nabis_dispatch_data['Date'].min(), nabis_dispatch_data['Date'].max()])
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange = True)
    tabs.append(dcc.Tab(label='Working hours', value='Working hours', children=[dcc.Graph(figure=fig, config = {'displayModeBar':False, 'scrollZoom':False} )], style=tab_style))

    return tabs

tabs = create_tabs()
total_rescheduled = nabis_dispatch_data.groupby(["Your name"]).sum().reset_index(inplace = False)
# total_rescheduled['Total rescheduled percentage'] = total_rescheduled[['Total rescheduled', 'Total orders']].apply(lambda x: str(f"{((x['Total rescheduled'] / x['Total orders']) * 100):.2f}%"), axis = 1)


total_rescheduled_fig = px.pie(total_rescheduled,
                            values = 'Total rescheduled',
                            names = 'Your name')

total_rescheduled_fig.update_layout(paper_bgcolor = "#3A3A3A", margin=dict(t=0, b=0, l=0, r=0), height = 250)
total_rescheduled_fig.update_traces(
    textposition="inside", texttemplate="%{label}: <br>(%{percent})"
)
total_rescheduled_fig.update_layout(showlegend=False)


best_members_fig = px.pie(
    best_members_df,
    values="Total orders",
    names="Your name",
    hole=0.4,
    color_discrete_sequence=px.colors.diverging.Temps,
)
best_members_fig.update_layout(paper_bgcolor = "#3A3A3A", margin=dict(t=0, b=0, l=0, r=0), height = 250)
best_members_fig.update_traces(
    textposition="inside", texttemplate="%{label}: <br>(%{percent})"
)
best_members_fig.update_layout(showlegend=False)


best_cities_df = nabis_dispatch_data.groupby(["City"]).sum()
best_cities_df.reset_index(inplace=True)
best_city_fig = px.pie(
    best_cities_df, values="Total orders", names="City", hole=0.4
)
best_city_fig.update_traces(
    textposition="inside", texttemplate="%{label}: <br>(%{percent})"
)
best_city_fig.update_layout(paper_bgcolor = "#3A3A3A", margin=dict(t=10, b=0, l=0, r=0), height = 250, showlegend = False)


custom_weekday_sort = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}
best_weekday_df = nabis_dispatch_data.groupby(["Weekday"]).sum()
best_weekday_df.reset_index(inplace=True)
best_weekday_df.sort_values(by=['Weekday'], inplace = True, key= lambda x: x.map(custom_weekday_sort))
weekdays_fig = px.bar(
    best_weekday_df,
    x="Weekday",
    y="Total orders",
    text=best_weekday_df['Total orders'].values.tolist(),
    # title="Weekday sales order distribution",
    color="Total orders",
    color_continuous_scale = 'sunsetdark',
    height = 310
)
weekdays_fig.update_layout(
            paper_bgcolor = "#3A3A3A",
            plot_bgcolor="#393939",
            font=dict(
                # family="Courier New, monospace",
                size=14,
                color=colors["figure_text"],
            ),
            legend=dict(
                x=0.02,
                y=1,
                traceorder="normal",
                # font=dict(family="sans-serif", size=12, color=colors["figure_text"]),
                bgcolor="#393939",
                borderwidth=5,
            ))
weekdays_fig.update_xaxes( fixedrange = True)
weekdays_fig.update_yaxes( fixedrange = True)
# weekdays_fig.add_annotation(showarrow=True,
#                    arrowhead=2,
#                    arrowwidth=2,
#                    arrowcolor="#636363",
#                    align = 'right',
#                    ax=20,
#         ay=-30,
#                    x=best_weekday_df.max(axis = 1).idxmax(),
#                    y=best_weekday_df.max(),
#                    text="Max",
#                    opacity=0.7)
# logo_image = os.path.join(os.getcwd(), "Logo.png")
# encoded_image = base64.b64encode(open(logo_image, "rb").read())

PLOTLY_LOGO = "https://assets.website-files.com/5c253860fd28a73e98ee5416/60b7c13e4795f4648fbf7b04_nabis_lockup_n.png"
# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Page 2", href="#"),
#                 dbc.DropdownMenuItem("Page 3", href="#"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     color="primary",
#     dark=True,
# )

#transform every unique date to a number
numdate= [x for x in range(len(nabis_dispatch_data['Date'].unique()))]
# numdate= [x.strftime('%d/%m') for x in nabis_dispatch_data['Date'].dt.date.unique().tolist()]




#then in the Slider
range_slider_marks = {numd:date.strftime('%d/%m/%y') for numd,date in zip(numdate, nabis_dispatch_data['Date'].dt.date.unique().tolist())}
numdate = numdate[::7]
range_slider_marks_sliced = {numd:date.strftime('%d/%m/%y') for numd,date in zip(numdate, nabis_dispatch_data['Date'].dt.date.unique().tolist()[::7])}
slajder = html.Div(dcc.RangeSlider(id = 'date-range-slider',min=numdate[0], #the first date
               max=numdate[-1], #the last date
               value=[numdate[0], numdate[-1]], #default: the first
               marks = range_slider_marks_sliced,
               # tooltip = {'placement':'bottom', 'always_visible':True},
               pushable = 2,
               allowCross = False), style = {"backgroundColor": "#393939"})
# slajder = dcc.Slider(
#     min=0,
#     max=10,
#     step=1,
#     value=5,
#     tooltip={"placement": "bottom", "always_visible": True},
# )
app.layout = html.Div(
    [
        dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            [dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px", style = {'backgroundColor':'white'})),
                    dbc.Col(dbc.NavbarBrand("- Dispatch dashboard", className="ml-2", style = {"font-weight": "bold"})),
                    
                ],
                align="center",
                no_gutters=True,
            )]
            
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        # dbc.Collapse(
        #     navbar, id="navbar-collapse", navbar=True, is_open=False
        # ),
        
    ],
    color="dark",
    dark=True,
),
        
        dbc.Card(
            dbc.CardBody(
                [
                    # dbc.Row(html.Div(style={"height": "50px"})),
                    # dbc.Row(
                    #         dbc.Col(
                    #             dbc.Card(
                    #                     [html.H4(
                    #                             children="Date range",
                    #                             style={
                    #                                 "textAlign": "center",
                    #                                 "color": colors["recovered_text"],
                    #                                 "padding-top":'5px',
                    #                                 "font-weight": "bold"
                    #                             },
                    #                         ),
                    #                     dbc.CardBody(slajder),
                    #                     html.Div(id='output-date-range-slider', style = {'color':colors['recovered_text']})], 
                    #                     style = {"backgroundColor": "#393939",
                    #                              "borderRadius": "12px",
                    #                              "lineHeight": 0.9,}), 
                    #                 className = 'w-100')
                    #         ),
                    html.Br(),
                    
                    
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            dbc.Tabs(children=tabs, id = 'tabs-parent'),
                                            style={
                                                "color": colors["recovered_text"],
                                                "backgroundColor": "#393939",
                                                "borderRadius": "12px",
                                                "lineHeight": 0.9,
                                            },
                                        ),
                                        color="#393939",
                                        style={
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    ),
                                    html.Br(),
                                    
                                ],
                                width=12,
                            ),
                            # dbc.Col(
                            #     [
                            #         dbc.Card(
                            #             dbc.Row(
                            #                 html.Div(
                            #                     [html.H4(
                            #                     children="Total orders by member:",
                            #                     style={
                            #                         "textAlign": "center",
                            #                         "color": colors["recovered_text"],
                            #                         "font-weight": "bold"
                            #                     },
                            #                 ),
                            #                     dcc.Graph(figure=best_members_fig, config = {'displayModeBar':False, 'scrollZoom':False}),
                            #                     ],style={"width": "100%"}
                            #                 )
                            #             ),
                            #             body=True,
                            #             style={
                            #                 "color": colors["recovered_text"],
                            #                 "backgroundColor": "#393939",
                            #                 "borderRadius": "12px",
                            #                 "lineHeight": 0.9,
                            #             },
                            #         ),
                            #         html.Br(),
                            #         dbc.Card(
                            #             dbc.Row(
                            #                 html.Div([
                            #                     html.H4(
                            #                     children="Orders by city:",
                            #                     style={
                            #                         "textAlign": "center",
                            #                         "color": colors["recovered_text"],
                            #                         "font-weight": "bold"
                            #                     },
                            #                 ),
                            #                     dcc.Graph(figure=best_city_fig, style={
                            #                 "color": colors["recovered_text"],
                            #                 "backgroundColor": "#393939",
                            #                 "borderRadius": "12px",
                            #                 "lineHeight": 0.9,
                            #             }, config = {'displayModeBar':False, 'scrollZoom':False},
                            #             )],
                            #                     style={"width": "100%"},
                            #                 )
                            #             ),
                            #             body=True,
                            #             style={
                            #                 "color": colors["recovered_text"],
                            #                 "backgroundColor": "#393939",
                            #                 "borderRadius": "12px",
                            #                 "lineHeight": 0.9,
                            #             },
                            #         ),
                            #         html.Br(),
                            #         dbc.Card(
                            #             dbc.Row(
                            #                 html.Div([
                            #                     html.H4(
                            #                     children="Orders by city:",
                            #                     style={
                            #                         "textAlign": "center",
                            #                         "color": colors["recovered_text"],
                            #                         "font-weight": "bold"
                            #                     },
                            #                 ),
                            #                     dcc.Graph(figure=best_city_fig, style={
                            #                 "color": colors["recovered_text"],
                            #                 "backgroundColor": "#393939",
                            #                 "borderRadius": "12px",
                            #                 "lineHeight": 0.9,
                            #             }, config = {'displayModeBar':False, 'scrollZoom':False},
                            #             )],
                            #                     style={"width": "100%"},
                            #                 )
                            #             ),
                            #             body=True,
                            #             style={
                            #                 "color": colors["recovered_text"],
                            #                 "backgroundColor": "#393939",
                            #                 "borderRadius": "12px",
                            #                 "lineHeight": 0.9,
                            #             },
                            #         ),
                            #     ],
                            #     width=4,
                            # ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col([
                                dbc.Card(
                                        dbc.Col(
                                            html.Div(
                                                [html.H4(
                                                children="Total orders by member:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "font-weight": "bold"
                                                },
                                            ),
                                                dcc.Graph(figure=best_members_fig, config = {'displayModeBar':False, 'scrollZoom':False}),
                                                ],style={"width": "100%"}
                                            )
                                        ),
                                        body=True,
                                        style={
                                            "color": colors["recovered_text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    )
                                ], 
                                    width = 4),
                            # 
                            dbc.Col([ dbc.Card(
                                            dbc.Row(
                                                html.Div([
                                                    html.H4(
                                                    children="Orders by city:",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": colors["recovered_text"],
                                                        "font-weight": "bold"
                                                    },
                                                ),
                                                    dcc.Graph(figure=best_city_fig, style={
                                                "color": colors["recovered_text"],
                                                "backgroundColor": "#393939",
                                                "borderRadius": "12px",
                                                "lineHeight": 0.9,
                                            }, config = {'displayModeBar':False, 'scrollZoom':False},
                                            )],
                                                    style={"width": "100%"},
                                                )
                                            ),
                                            body=True,
                                            style={
                                                "color": colors["recovered_text"],
                                                "backgroundColor": "#393939",
                                                "borderRadius": "12px",
                                                "lineHeight": 0.9,
                                            },
                                        )],width = 4),
                            dbc.Col([
                                dbc.Card(
                                        dbc.Col(
                                            html.Div(
                                                [html.H4(
                                                children="Total rescheduled orders by member:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "font-weight": "bold"
                                                },
                                            ),
                                                dcc.Graph(figure=total_rescheduled_fig, config = {'displayModeBar':False, 'scrollZoom':False}),
                                                ],style={"width": "100%"}
                                            )
                                        ),
                                        body=True,
                                        style={
                                            "color": colors["recovered_text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    )
                                ], 
                                    width = 4)
                        ]),
                    html.Br(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [dbc.Card(
                                        [html.H4(
                                                children="Total order distribution by weekday:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "padding-top":'5px',
                                                    "font-weight": "bold"
                                                },
                                            ),
                                        dbc.CardBody(dcc.Graph(figure=weekdays_fig, config = {'displayModeBar':False, 'scrollZoom':False}))],
                                        style={
                                            "color": colors["recovered_text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    ),
                                    ],
                                width = 12
                            )
                        ]
                    ),
                ],
                style={
                    "color": colors["recovered_text"],
                    "backgroundColor": colors["background"],
                },
            ),
            color=colors["background"],
        )
    ]
)
# @app.callback(
#     dash.dependencies.Output('output-date-range-slider', 'children'),
# #     [dash.dependencies.Input('date-range-slider', 'value')])
# def upate_output(value):
#     return 'You have selected "{}, {}"'.format(range_slider_marks[value[0]], range_slider_marks[value[1]])

if __name__ == "__main__":
    # app.run_server(debug=True, use_reloader=True, threaded=True, port = 1776)
    app.run_server()
    
    
# Things to do for Heroku
# Uncomment 'server' line
# Modify app.run_server method to app.run_server() only
