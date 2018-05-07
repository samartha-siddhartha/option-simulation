# -*- coding: utf-8 -*-
"""
Created on Mon May  7 08:49:42 2018

@author: SamarthaS
"""

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import numpy as np
import dash_auth

from option_simulation import call_table,put_table

#APP_NAME = 'Option Simulation'
#APP_URL = 'https://127.0.0.1:8050/'

app = dash.Dash(__name__)
 
VALID_USERNAME_PASSWORD_PAIRS = [
    ['optionstrade', 'greek@321']   
]
app = dash.Dash('auth')
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server =app.server
app.scripts.config.serve_locally = True


greeks =['Option Price','Delta','Gamma','Vega','Theta']
app.config['suppress_callback_exceptions']=True
app.layout = html.Div([
        
     html.Div([
            html.H4('Option Greek Simulation'), 
            html.Div([dcc.Markdown('''>Underlying''')],style={'width': '10%', 'display': 'inline-block'}),
            
            html.Div([dcc.Input(id='underlying',type='int',value='9000')],style={'width': '18%', 'display': 'inline-block'}),
             html.Div([dcc.Markdown('''>Strike''')],style={'width': '10%', 'display': 'inline-block'}),
            
            html.Div([dcc.Input(id='strike',type='int',value='9800')],style={'width': '18%', 'display': 'inline-block'}),
            
            html.Div([dcc.Markdown('''>Days To Expiry''')],style={'width': '17%', 'display': 'inline-block'}),
            
            html.Div([dcc.Input(id='dayexpiry',type='int',value='15')],style={'width': '18%', 'display': 'inline-block'}),
            
            html.Div([dcc.Markdown('''>Volatility ''')],style={'width': '11%', 'display': 'inline-block'}),
            
            html.Div([dcc.Input(id='vol',type='int',value='15')],style={'width': '18%', 'display': 'inline-block'}),
            
            html.Div([dcc.Markdown('''>Price Difference''')],style={'width': '20%', 'display': 'inline-block'}),
            
            html.Div([dcc.Input(id='diff',type='int',value ='100')],style={'width': '40%', 'display': 'inline-block'}),
            
            html.Div([dcc.Dropdown(id ='greek',options = [{'label': i, 'value': i} for i in greeks],value='Option Price')],style={'width': '15%', 'display': 'inline-block'}),
            
            html.Div(html.Button(id='submit-button',n_clicks=0,children='Submit'),style={'float': 'right', 'display': 'inline-block'}),
            
            html.Div(id='output1'),
            ]),
    html.Div([
    html.Div(id='content'),
    dcc.Location(id='location', refresh=False),
    html.Div(dt.DataTable(rows=[{}]), style={'display':'none'})
]),

    
    html.Div(id='output2'),
     
           
    
], className="container",)

@app.callback(Output('output2', 'children'),
              [Input('submit-button', 'n_clicks')],
               [State(component_id='underlying', component_property='value'),
                State(component_id='strike', component_property='value'),
                State(component_id='dayexpiry', component_property='value'),
                State(component_id='vol', component_property='value'),
                State(component_id='diff', component_property='value'),
                State(component_id='greek', component_property='value'),
                ])

def update_greeks(click,underlying,strike,dayexpiry,vol,diff,greek ):
    call_data = call_table(underlying,strike,dayexpiry,vol,diff,greek )
    put_data = put_table(underlying,strike,dayexpiry,vol,diff,greek)
    return html.Div([
            html.H4('Call'),
            dt.DataTable(
           
                rows=call_data.to_dict('records'),
                # optional - sets the order of columns
#                columns=sorted(call_data.columns),
                row_selectable=False,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                id='datatable1'
    ),
            html.Hr(),
            
            html.H4('Put'),
            dt.DataTable(
    
                rows=put_data.to_dict('records'),
        # optional - sets the order of columns
               #columns=sorted(data.columns),
                row_selectable=False,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                id='datatable2'
    ),html.H5('Owner: Samartha.Siddhartha@gmail.com'),])   





app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)