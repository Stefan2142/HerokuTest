import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from app_style import *
from routines import *


def create_tabs():
    tabs = []

    fig = go.Figure()

    def populate(name, x, y):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name=name,
                line=dict(color=colors[name], width=4),
                fill="tozeroy",
                line_shape="spline",
            )
        )

    # TOTAL ORDERS
    for name in names:
        populate(
            name=name,
            x=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["Date"],
            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["Total orders"],
        )

    fig.update_layout(
        hovermode="x",
        font=dict(
            family="sans-serif",  # Courier New, monospace
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
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#3A3A3A",
        fixedrange=True,
        range=[nabis_dispatch_data["Date"].min(), nabis_dispatch_data["Date"].max()],
    )
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(
        zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange=True
    )
    tabs.append(
        dcc.Tab(
            label="Total orders",
            value="Total orders",
            children=[
                dcc.Graph(
                    figure=fig,
                    config={"displayModeBar": False, "scrollZoom": False},
                    animate=True,
                )
            ],
            style=tab_style,
        )
    )

    # TOTAL RESCHEDULED
    fig = go.Figure()
    for name in names:
        populate(
            name=name,
            x=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["Date"],
            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["Total rescheduled"],
        )

    fig.update_layout(
        hovermode="x",
        font=dict(
            family="sans-serif",  # Courier New, monospace
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
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#3A3A3A",
        fixedrange=True,
        range=[nabis_dispatch_data["Date"].min(), nabis_dispatch_data["Date"].max()],
    )
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(
        zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange=True
    )
    tabs.append(
        dcc.Tab(
            label="Total rescheduled orders",
            value="Total rescheduled orders",
            children=[
                dcc.Graph(
                    figure=fig,
                    config={"displayModeBar": False, "scrollZoom": False},
                    animate=True,
                )
            ],
            style=tab_style,
        )
    )

    # Iteration
    for name in names:
        # fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # temp_df = nabis_dispatch_data[nabis_dispatch_data["Your name"] == name].groupby(by='Date')['Total orders'].sum().reset_index()
        temp_df = (
            nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .agg(
                {
                    "Total orders": "sum",
                    "DecimalTime": "first",
                    "Total rescheduled": "sum",
                }
            )
            .reset_index()
        )
        fig.add_trace(
            go.Bar(
                x=temp_df["Date"],
                y=temp_df["DecimalTime"],
                name="Hours",
                marker_color="#dc3545",
            ),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=temp_df["Date"],
                y=temp_df["Total orders"],
                mode="lines+markers",
                name="Total orders",
                line=dict(color="#33FF51", width=4),
                fill="tozeroy",
                line_shape="spline",
                marker=dict(size=7, color="rgba(255, 182, 193, .9)"),
            ),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(
                x=temp_df["Date"],
                y=temp_df["Total rescheduled"],
                mode="lines+markers",
                name="Total rescheduled orders",
                line=dict(color=colors["Sasa"], width=4),
                fill="tozeroy",
                line_shape="spline",
                marker=dict(size=5, color="rgba(255, 182, 193, .9)"),
            ),
            secondary_y=True,
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
        fig.update_xaxes(
            showgrid=True, gridwidth=1, gridcolor="#3A3A3A", fixedrange=True
        )
        # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

        fig.update_yaxes(
            zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange=True
        )
        tabs.append(
            dcc.Tab(
                label=name,
                value=name,
                children=[
                    dcc.Graph(
                        figure=fig,
                        config={"displayModeBar": False, "scrollZoom": False},
                    )
                ],
                style=tab_style,
            )
        )

    fig = go.Figure()
    for name in names:
        populate(
            name=name,
            x=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["Date"],
            y=nabis_dispatch_data[nabis_dispatch_data["Your name"] == name]
            .groupby(by="Date")
            .sum()
            .reset_index()["DecimalTime"],
        )

    fig.update_layout(
        hovermode="x",
        font=dict(
            family="sans-serif",  # Courier New, monospace
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
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#3A3A3A",
        fixedrange=True,
        range=[nabis_dispatch_data["Date"].min(), nabis_dispatch_data["Date"].max()],
    )
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#3A3A3A")

    fig.update_yaxes(
        zeroline=True, zerolinewidth=2, zerolinecolor="#3A3A3A", fixedrange=True
    )
    tabs.append(
        dcc.Tab(
            label="Working hours",
            value="Working hours",
            children=[
                dcc.Graph(
                    figure=fig, config={"displayModeBar": False, "scrollZoom": False}
                )
            ],
            style=tab_style,
        )
    )

    return tabs


def total_rescheduled():

    total_rescheduled = (
        nabis_dispatch_data.groupby(["Your name"]).sum().reset_index(inplace=False)
    )
    # total_rescheduled['Total rescheduled percentage'] = total_rescheduled[['Total rescheduled', 'Total orders']].apply(lambda x: str(f"{((x['Total rescheduled'] / x['Total orders']) * 100):.2f}%"), axis = 1)

    total_rescheduled_fig = px.pie(
        total_rescheduled, values="Total rescheduled", names="Your name"
    )

    total_rescheduled_fig.update_layout(
        paper_bgcolor="#3A3A3A", margin=dict(t=0, b=0, l=0, r=0), height=250
    )
    total_rescheduled_fig.update_traces(
        textposition="inside", texttemplate="%{label}: <br>(%{value})"
    )
    total_rescheduled_fig.update_layout(showlegend=False)
    return total_rescheduled_fig


def orders_by_member():
    best_members_df = nabis_dispatch_data.groupby(["Your name"]).sum()
    best_members_df.reset_index(inplace=True)
    best_member = best_members_df.nlargest(1, "Total orders").to_dict("records")[0]
    best_members_fig = px.pie(
        best_members_df,
        values="Total orders",
        names="Your name",
        hole=0.4,
        color_discrete_sequence=px.colors.diverging.Temps,
    )
    best_members_fig.update_layout(
        paper_bgcolor="#3A3A3A", margin=dict(t=0, b=0, l=0, r=0), height=250
    )
    best_members_fig.update_traces(
        textposition="inside", texttemplate="%{label}: <br>(%{percent})"
    )
    best_members_fig.update_layout(showlegend=False)
    return best_members_fig


def order_by_city():
    best_cities_df = nabis_dispatch_data.groupby(["City"]).sum()
    best_cities_df.reset_index(inplace=True)
    best_city_fig = px.pie(
        best_cities_df, values="Total orders", names="City", hole=0.4
    )
    best_city_fig.update_traces(
        textposition="inside", texttemplate="%{label}: <br>(%{percent})"
    )
    best_city_fig.update_layout(
        paper_bgcolor="#3A3A3A",
        margin=dict(t=10, b=0, l=0, r=0),
        height=250,
        showlegend=False,
    )
    return best_city_fig


def orders_by_weekday():
    custom_weekday_sort = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    best_weekday_df = nabis_dispatch_data.groupby(["Weekday"]).sum()
    best_weekday_df.reset_index(inplace=True)
    best_weekday_df.sort_values(
        by=["Weekday"], inplace=True, key=lambda x: x.map(custom_weekday_sort)
    )
    weekdays_fig = px.bar(
        best_weekday_df,
        x="Weekday",
        y="Total orders",
        text=best_weekday_df["Total orders"].values.tolist(),
        # title="Weekday sales order distribution",
        color="Total orders",
        color_continuous_scale="sunsetdark",
        height=310,
    )
    weekdays_fig.update_layout(
        paper_bgcolor="#3A3A3A",
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
        ),
    )
    weekdays_fig.update_xaxes(fixedrange=True)
    weekdays_fig.update_yaxes(fixedrange=True)
    return weekdays_fig


PLOTLY_LOGO = "https://assets.website-files.com/5c253860fd28a73e98ee5416/60b7c13e4795f4648fbf7b04_nabis_lockup_n.png"

nabis_dispatch_data = prepare_dataset()
names = list(set(nabis_dispatch_data["Your name"].values.tolist()))
# transform every unique date to a number
numdate = [x for x in range(len(nabis_dispatch_data["Date"].unique()))]
# numdate= [x.strftime('%d/%m') for x in nabis_dispatch_data['Date'].dt.date.unique().tolist()]


# then in the Slider
range_slider_marks = {
    numd: date.strftime("%d/%m/%y")
    for numd, date in zip(
        numdate, nabis_dispatch_data["Date"].dt.date.unique().tolist()
    )
}
numdate = numdate[::7]
range_slider_marks_sliced = {
    numd: date.strftime("%d/%m/%y")
    for numd, date in zip(
        numdate, nabis_dispatch_data["Date"].dt.date.unique().tolist()[::7]
    )
}
slajder = html.Div(
    dcc.RangeSlider(
        id="date-range-slider",
        min=numdate[0],  # the first date
        max=numdate[-1],  # the last date
        value=[numdate[0], numdate[-1]],  # default: the first
        marks=range_slider_marks_sliced,
        # tooltip = {'placement':'bottom', 'always_visible':True},
        pushable=2,
        allowCross=False,
    ),
    style={"backgroundColor": "#393939"},
)


layout = (
    dbc.Card(
        dbc.CardBody(
            [
                # Slider row
                dbc.Row(
                    dbc.Col(
                        dbc.Card(
                            [
                                html.H4(
                                    children="Date range",
                                    style={
                                        "textAlign": "center",
                                        "color": colors["recovered_text"],
                                        "padding-top": "5px",
                                        "font-weight": "bold",
                                    },
                                ),
                                dbc.CardBody(slajder),
                                html.Div(
                                    id="output-date-range-slider",
                                    style={"color": colors["recovered_text"]},
                                ),
                            ],
                            style={
                                "backgroundColor": "#393939",
                                "borderRadius": "12px",
                                "lineHeight": 0.9,
                            },
                        ),
                        className="w-100",
                    )
                ),
                html.Br(),
                # Tabs row
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        dbc.Tabs(
                                            children=create_tabs(), id="tabs-parent"
                                        ),
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
                    ]
                ),
                # Three pie charts row
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.Col(
                                        html.Div(
                                            [
                                                html.H4(
                                                    children="Total orders by member:",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": colors[
                                                            "recovered_text"
                                                        ],
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                dcc.Graph(
                                                    figure=orders_by_member(),
                                                    config={
                                                        "displayModeBar": False,
                                                        "scrollZoom": False,
                                                    },
                                                ),
                                            ],
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
                                )
                            ],
                            width=4,
                        ),
                        #
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.Row(
                                        html.Div(
                                            [
                                                html.H4(
                                                    children="Orders by city:",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": colors[
                                                            "recovered_text"
                                                        ],
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                dcc.Graph(
                                                    figure=order_by_city(),
                                                    style={
                                                        "color": colors[
                                                            "recovered_text"
                                                        ],
                                                        "backgroundColor": "#393939",
                                                        "borderRadius": "12px",
                                                        "lineHeight": 0.9,
                                                    },
                                                    config={
                                                        "displayModeBar": False,
                                                        "scrollZoom": False,
                                                    },
                                                ),
                                            ],
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
                                )
                            ],
                            width=4,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.Col(
                                        html.Div(
                                            [
                                                html.H4(
                                                    children="Total rescheduled orders by member:",
                                                    style={
                                                        "textAlign": "center",
                                                        "color": colors[
                                                            "recovered_text"
                                                        ],
                                                        "font-weight": "bold",
                                                    },
                                                ),
                                                dcc.Graph(
                                                    figure=total_rescheduled(),
                                                    config={
                                                        "displayModeBar": False,
                                                        "scrollZoom": False,
                                                    },
                                                ),
                                            ],
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
                                )
                            ],
                            width=4,
                        ),
                    ]
                ),
                html.Br(),
                # Weekday row
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        html.H4(
                                            children="Total order distribution by weekday:",
                                            style={
                                                "textAlign": "center",
                                                "color": colors["recovered_text"],
                                                "padding-top": "5px",
                                                "font-weight": "bold",
                                            },
                                        ),
                                        dbc.CardBody(
                                            dcc.Graph(
                                                figure=orders_by_weekday(),
                                                config={
                                                    "displayModeBar": False,
                                                    "scrollZoom": False,
                                                },
                                            )
                                        ),
                                    ],
                                    style={
                                        "color": colors["recovered_text"],
                                        "backgroundColor": "#393939",
                                        "borderRadius": "12px",
                                        "lineHeight": 0.9,
                                    },
                                ),
                            ],
                            width=12,
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
    ),
)
