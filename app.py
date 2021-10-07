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


def chunker_list(seq, size):
    """
    Returns a list of lists.
    size - how much sub lists we want
    seq - original list
    Usage tmp = list(chunker_list(l, 10))
    """
    return (seq[i::size] for i in range(size))


gc = gspread.service_account(filename="./emailsending-325211-e5456e88f282.json")
# gc = gspread.service_account(filename='/home/ec2-user/ReportSender/service_acc.json')

sh = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1rRwdq2otnXI9d3B9LfYRarQl6RxANP0_TqTQLjTY9A8/edit#gid=1032147445"
)
wks = sh.worksheet("Main_working_sheet")

nabis_dispatch_data = pd.DataFrame(
    wks.get_all_records(),
)
nabis_dispatch_data = nabis_dispatch_data.fillna(value="")
nabis_dispatch_data["City"] = nabis_dispatch_data["City"].astype(str)
nabis_dispatch_data["Your name"] = nabis_dispatch_data["Your name"].astype(str)
nabis_dispatch_data["Total orders"] = nabis_dispatch_data["Total orders"].astype(int)
nabis_dispatch_data["Date"] = pd.to_datetime(
    nabis_dispatch_data.Date, format="%m/%d/%y"
)
nabis_dispatch_data["Weekday"] = nabis_dispatch_data["Date"].dt.day_name()
nabis_dispatch_data.sort_values(by="Date", inplace=True)
names = list(set(nabis_dispatch_data["Your name"].values.tolist()))

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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
def create_tabs():
    tabs = []

  
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=nabis_dispatch_data['Date'], 
                            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == names[0]]['Total orders'],
                            mode='lines',
                            name=names[0],
                            line=dict(color='#3372FF', width=4),
                            fill='tozeroy',
                            line_shape='spline'))
    fig.add_trace(go.Scatter(x=nabis_dispatch_data['Date'], 
                            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == names[1]]['Total orders'],
                            mode='lines',
                            name=names[1],
                            line=dict(color='#33FF51', width=4),
                            fill='tozeroy',
                            line_shape='spline'))
    fig.add_trace(go.Scatter(x=nabis_dispatch_data['Date'], 
                            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == names[2]]['Total orders'],
                            mode='lines',
                            name=names[2],
                            line=dict(color='#FF3333', width=4),
                            fill='tozeroy',
                            line_shape='spline'))
    fig.update_layout(
        hovermode="x",
        font=dict(
            family="Courier New, monospace",
            size=14,
            color=colors["figure_text"],
        ),
        legend=dict(
            x=0.02,
            y=0,
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
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A")
    tabs.append(dcc.Tab(label='All Names', value='All Names', children=[dcc.Graph(figure=fig)]))

    # Iteration
    for name in names:
        fig = go.Figure()

        temp_df = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
        fig.add_trace(
            go.Scatter(
                x=temp_df["Date"],
                y=temp_df["Total orders"],
                mode="lines+markers",
                name=name,
                line=dict(color="#33FF51", width=4),
                fill="tozeroy",
                line_shape='spline'
            )
        )

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
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")
        # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

        fig.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A")
        tabs.append(dcc.Tab(label=name, value=name, children=[dcc.Graph(figure=fig)]))

    return tabs

tabs = create_tabs()

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


best_weekday_df = nabis_dispatch_data.groupby(["Weekday"]).sum()
best_weekday_df.reset_index(inplace=True)
weekdays_fig = px.bar(
    best_weekday_df,
    x="Weekday",
    y="Total orders",
    # title="Weekday sales order distribution",
    color="Total orders",
    color_continuous_scale = px.colors.sequential.YlOrRd,
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
logo_image = os.path.join(os.getcwd(), "Logo.png")
encoded_image = base64.b64encode(open(logo_image, "rb").read())

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

app.layout = html.Div(
    [
        dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px", style = {'backgroundColor':'white'})),
                    dbc.Col(dbc.NavbarBrand("- Dispatch dashboard", className="ml-2", style = {"font-weight": "bold"})),
                ],
                align="center",
                no_gutters=True,
            ),
            
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
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            dbc.Tabs(children=tabs),
                                            style={
                                                "color": colors["text"],
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
                                    dbc.Card(
                                        [html.H4(
                                                children="Weekday sales order distribution:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "padding-top":'5px',
                                                    "font-weight": "bold"
                                                },
                                            ),
                                        dbc.CardBody(dcc.Graph(figure=weekdays_fig))],
                                        style={
                                            "color": colors["text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    ),
                                ],
                                width=8,
                            ),
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.H4(
                                                children="Best worker:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "font-weight": "bold"
                                                },
                                            ),
                                            html.P(
                                                f"{best_member['Your name']}",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "fontSize": 30,
                                                },
                                            ),
                                            html.P(
                                                f"with {best_member['Total orders']} orders.",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                },
                                            ),
                                        ],
                                        style=divBorderStyle,
                                    ),
                                    html.Br(),
                                    dbc.Card(
                                        dbc.Row(
                                            html.Div(
                                                dcc.Graph(figure=best_members_fig),
                                                style={"width": "100%"},
                                            )
                                        ),
                                        body=True,
                                        style={
                                            "color": colors["text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    ),
                                    html.Br(),
                                    dbc.Card(
                                        dbc.Row(
                                            html.Div([
                                                html.H4(
                                                children="Sales by city:",
                                                style={
                                                    "textAlign": "center",
                                                    "color": colors["recovered_text"],
                                                    "font-weight": "bold"
                                                },
                                            ),
                                                dcc.Graph(figure=best_city_fig, style={
                                            "color": colors["text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                        )],
                                                style={"width": "100%"},
                                            )
                                        ),
                                        body=True,
                                        style={
                                            "color": colors["text"],
                                            "backgroundColor": "#393939",
                                            "borderRadius": "12px",
                                            "lineHeight": 0.9,
                                        },
                                    ),
                                ],
                                width=4,
                            ),
                        ]
                    ),
                ],
                style={
                    "color": colors["text"],
                    "backgroundColor": colors["background"],
                },
            ),
            color=colors["background"],
        )
    ]
)



if __name__ == "__main__":
    app.run_server()
