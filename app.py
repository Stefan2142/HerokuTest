from flask import Flask
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# from app import app, server
from apps import dashboard

server = app.server 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="NABIS", suppress_callback_exceptions=True)
server.config.update(SECRET_KEY='291a47103f3cd8fc26d05ffc7b31e33f73ca3d459d6259bd')
# auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/"

# User data model. It has to have at least self.id as a minimum


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the user from a user database.
    We won't be registering or looking up users in this example, since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)



NABIS_LOGO = "https://assets.website-files.com/5c253860fd28a73e98ee5416/60b7c13e4795f4648fbf7b04_nabis_lockup_n.png"


login = html.Div(
    [
        dbc.Container(
            [
                html.Br(),
                html.Br(),
                dbc.Container(
                    [
                        # dcc.Location(id="urlLogin", refresh=True),
                        html.Div(
                            [
                                dbc.Container(
                                    id="loginType",
                                    children=[
                                        dbc.Input(
                                            placeholder="Enter your username",
                                            type="login",
                                            id="usernameBox",
                                            className="fadeIn second",
                                            n_submit=0,
                                            size="xs",
                                            style={"width": "30%"},
                                        ),
                                        html.Br(),
                                        dbc.Input(
                                            placeholder="Enter your password",
                                            type="password",
                                            id="password",
                                            className="fadeIn third",
                                            n_submit=0,
                                            size="xs",
                                            style={"width": "30%"},
                                        ),
                                        html.Br(),
                                        dbc.Button(
                                            children="Login",
                                            n_clicks=0,
                                            type="submit",
                                            id="loginButton",
                                            className="fadeIn fourth",
                                            color="success",
                                        ),
                                        html.Br(),
                                        html.Br(),
                                    ],
                                    className="wrapper fadeInDown",
                                ),
                            ],
                            style={"height": "100%"},
                        ),
                    ],
                    className="jumbotron h-100",
                ),
            ],
            style={"backgroundColor": "#393939"},
            className="w-100",
        ),
        html.Div(
            children="",
            id="output-state",
            style={"textAlign": "center"},
            className="container-fluid",
        ),
    ],
    className="h-100",
    style={
        "height": "100%",
        "width": "100%",
        "background-color": "#393939",
        "color": "#393939",
        "min-height": "95vh",
    },
)

# Successful login
# success = html.Div([html.Div([html.H2('Login successful.{}'.format(current_user.get_id())),
success = html.Div(
    [
        html.Div(
            [
                html.H2("Redirecting..."),
                html.Br(),
                # dcc.Link("Home", href="/"),
            ]
        )  # end div
    ]
)  # end div

# # Failed Login
# failed = html.Div(
#     [
#         html.Div(
#             [
#                 html.H2("Log in Failed. Please try again."),
#                 html.Br(),
#                 html.Div([login]),
#                 dcc.Link("Home", href="/"),
#             ]
#         )  # end div
#     ]
# )  # end div

# logout
logout = html.Div(
    [
        html.Div(html.H2("You have been logged out - Please login")),
        html.Br(),
        dcc.Link("Home", href="/"),
    ]
)  # end div


@app.callback(
    Output("url_login", "pathname"),
    Output("output-state", "children"),
    [Input("loginButton", "n_clicks")],
    [State("usernameBox", "value"), State("password", "value")],
)
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if username == "test" and password == "test":
            user = User(username)
            login_user(user)
            return [
                "/success",
                html.P(
                    "Logging in!",
                    className="text-success",
                    style={"textAlign": "center"},
                ),
            ]
        else:
            return [
                "/",
                html.P(
                    "Incorrect username or password",
                    className="text-danger",
                    style={"textAlign": "center"},
                ),
            ]
    return "/", ""


# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='page-content'),
#     dcc.Link('Go to App1', href='/apps/app1/'),
#     html.Br(),
#     dcc.Link('Go to App2', href='/apps/app2/'),
# ])

NABIS_LOGO = "https://assets.website-files.com/5c253860fd28a73e98ee5416/60b7c13e4795f4648fbf7b04_nabis_lockup_n.png"
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="redirect", refresh=True),
        dcc.Location(id="url_login", refresh=True),
        dbc.Navbar(
            [
                dbc.NavItem(
                    html.Img(
                        src=NABIS_LOGO,
                        height="30px",
                        style={"backgroundColor": "white"},
                    ),
                    className="mr-auto",
                ),
                dbc.NavItem(
                    children=dbc.NavbarBrand(
                        "Dispatch dashboard",
                        className="text-center mx-auto ml-2",
                        style={"font-weight": "bold"},
                    ),
                    className="mx-auto ml-2",
                    # className = "d-flex justify-content-center",
                    style={"font-weight": "bold"},
                ),
                dbc.NavItem(
                    [
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dcc.Store(id="login-status", storage_type="session"),
                        dbc.NavItem(id="user-status-div", className="ml-auto"),
                    ],
                    className="ml-auto",
                ),
            ],
            color="dark",
            dark=True,
            className="container-fluid",
        ),
        # dcc.Store(id="login-status", storage_type="session"),
        html.Div(id="page-content"),
    ]
)

index_page = html.Div(
    [
        dbc.Card(dbc.CardBody(dcc.Link("Go to Page 1", href="/apps/dash_test2"))),
    ]
)


@app.callback(
    Output("user-status-div", "children"),
    Output("login-status", "data"),
    [Input("url", "pathname")],
)
def login_status(url):
    """callback to display login/logout link in the header"""
    if (
        hasattr(current_user, "is_authenticated")
        and current_user.is_authenticated
        and url != "/logout"
    ):  # If the URL is /logout, then the user is about to be logged out anyways

        return (
            dbc.Button("Logout", href="/logout", color="danger"),
            current_user.get_id(),
        )
        # return dcc.Link("logout", href="/logout"), current_user.get_id()
    else:
        return dbc.Button("Login", href="/", color="info"), "loggedout"
        # return dcc.Link("login", href="/"), "loggedout"


@app.callback(
    Output("page-content", "children"),
    Output("redirect", "pathname"),
    [Input("url", "pathname")],
)
def display_page(pathname):
    """callback to determine layout to return"""
    # We need to determine two things for everytime the user navigates:
    # Can they access this page? If so, we just return the view
    # Otherwise, if they need to be authenticated first, we need to redirect them to the login page
    # So we have two outputs, the first is which view we'll return
    # The second one is a redirection to another page is needed
    # In most cases, we won't need to redirect. Instead of having to return two variables everytime in the if statement
    # We setup the defaults at the beginning, with redirect to dash.no_update; which simply means, just keep the requested url
    view = None
    url = dash.no_update
    print(f"PATH {pathname}")
    if pathname == "/":
        view = login
    elif pathname == "/success":
        if current_user.is_authenticated:
            view = success
            url = "apps/dash_test2"
        else:
            view = login  # failed
            url = "/"
    elif pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
        view = login
        url = "/"

    elif pathname == "/apps/dash_test2":
        if current_user.is_authenticated:
            view = dash_test2.layout
        else:
            view = "Redirecting to login..."
            url = "/"
    else:
        view = index_page
    # You could also return a 404 "URL not found" page here
    return view, url


if __name__ == "__main__":
    app.run_server()
