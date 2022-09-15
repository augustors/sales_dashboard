from pydoc import classname
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

#df = pd.read_csv("dataset_asimov.csv")

#df.loc[df['Mês'] == 'Jan', 'Mês'] = 1
#df.loc[df['Mês'] == 'Fev', 'Mês'] = 2
#df.loc[df['Mês'] == 'Mar', 'Mês'] = 3
#df.loc[df['Mês'] == 'Abr', 'Mês'] = 4
#df.loc[df['Mês'] == 'Mai', 'Mês'] = 5
#df.loc[df['Mês'] == 'Jun', 'Mês'] = 6
#df.loc[df['Mês'] == 'Jul', 'Mês'] = 7
#df.loc[df['Mês'] == 'Ago', 'Mês'] = 8
#df.loc[df['Mês'] == 'Set', 'Mês'] = 9
#df.loc[df['Mês'] == 'Out', 'Mês'] = 10
#df.loc[df['Mês'] == 'Nov', 'Mês'] = 11
#df.loc[df['Mês'] == 'Dez', 'Mês'] = 12

#df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int)
#df['Dia'] = df['Dia'].astype(int)
#df['Mês'] = df['Mês'].astype(int)

#df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
#df['Valor Pago'] = df['Valor Pago'].astype(int)

#df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
#df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

#df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)

#df.to_csv("dataset_sales.csv")


#===========SERVER===========#

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

#===========Styles===========#
tab_card = {"height":"100%"}

main_config = {
    "hovermode": "x unified",
    "legend": {
        "yanchor": "top",
        "y": 0.9,
        "xanchor": "left",
        "x": 0.1,
        "title": {"text": None},
        "font": {"color":"white"},
        "bgcolor":"rgba(0,0,0,0.5)"
    },
    "margin": {"l":10, "r": 10, "t": 10, "b": 10}
}

config_graph = {"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

#===========Dataset===========#
df = pd.read_csv("dataset_sales.csv")
df_cru = pd.read_csv("dataset_asimov.csv")

options_month = [{'label': 'Ano todo', 'value': 0}]
for i,j in zip(df_cru['Mês'].unique(), df['Mês'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value'])

options_team = [{'label': 'Todas equipes', 'value':0}]
for i in df['Equipe'].unique():
    options_team.append({'label': i, 'value': i})

def month_filter(month):
    if month == 0:
        mask = df['Mês'].isin(df['Mês'].unique())
    else:
        mask = df['Mês'].isin([month])
    return mask

def convert_to_text(month):
    lista1 = ['Ano Todo', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
    'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    return lista1[month]

#===========Layout===========#
app.layout = dbc.Container(children=[
    #Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Sales Analytics")                           
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale', 
                            style={"font-size": "300%"})
                        ], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1,url_theme2]),
                            html.Legend("Asimov Academy")
                        ])
                    ])
                ])
            ], style=tab_card),
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, md=5),                                                    
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Escolha o Mês"),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align':'center', 'margin-top': '10px'})
                        ])
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={"margin-top": '7px'}),

    #Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style = tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className = 'dbc', config = config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={"margin-top": "7px"})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className = 'dbc', config = config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className = 'dbc', config = config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph7', className = 'dbc', config = config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph8', className = 'dbc', config = config_graph)
            ], style=tab_card)
        ], sm=12, lg=4)
    ], className='g-2 my-auto', style={"margin-top": "7px"}),

    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Valores de Propaganda convertidos por mês'),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ])
            ],style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Equipe'),
                    dbc.RadioItems(
                        id='radio-team',
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName='text=warning',
                        inputCheckedClassName='border border-warning bg-warning'
                    ),
                    html.Div(id='team-select', style={'text-align':'center', 'margin-top': '30px'})
                ])
            ], style=tab_card)
        ], sm=12, lg=2)
    ], className='g-2 my-auto', style={'margin-top': '7px'})

], fluid=True, style={'height':'100vh'})

#===========Callbacks===========#
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_1 = df.loc[mask]

    df_1 = df_1.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
    df_1 = df_1.sort_values(ascending=False)
    df_1 = df_1.groupby(['Equipe']).head(1).reset_index()

    fig2 = go.Figure(go.Pie(labels=df_1['Consultor'] + ' - ' + df_1['Equipe'], values = df_1['Valor Pago'], hole=0.6))
    fig1 = go.Figure(go.Bar(x=df_1['Consultor'], y= df_1['Valor Pago'], textposition = 'auto', text=df_1['Valor Pago']))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

#===========RUN SERVER===========#
if __name__ == "__main__":
    app.run_server(debug=True)