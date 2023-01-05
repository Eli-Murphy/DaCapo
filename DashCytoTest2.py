import json
from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import os
from num2words import num2words

cyto.load_extra_layouts()

file = r"C:\Users\elija\Documents\GitHub\DaCapo\PARK17.csv"

protienData = []

with open(file, "r") as csv:
    next(csv)
    data = csv.readlines()
    for r in range(len(data)):
        temp = {}
        row = data[r].split(",")
        if str(row[0]) in str(protienData):
            continue
        else:
            temp['data'] = {'id': row[0], 'label': row[0]}
        protienData.append(temp)


    for e in range(len(data)):
        temp = {}
        row = data[e].split(",")
        temp['data'] = {'source': row[0], 'target': row[1], 'weight': row[12]}
        protienData.append(temp)


    #for i in range(len(protienData)):
        #print(protienData[i])

    #print(protienData)

styles = {
    'container': {
        'position': 'fixed',
        'display': 'flex',
        'flex-direction': 'column',
        'height': '100%',
        'width': '100%'
    },
    'cy-container': {
        'flex': '1',
        'position': 'relative'
    },
    'cytoscape': {
        'position': 'absolute',
        'width': '100%',
        'height': '100%',
        'z-index': 999
    }
}


app = Dash(__name__)

app.layout = html.Div(style=styles['container'], children=[
    html.Div([
        html.Button("Responsive Toggle", id='toggle-button'),
            html.Div(id='toggle-text')
    ]),
    html.Div(className='cy-container', style=styles['cy-container'], children=[
        cyto.Cytoscape(
            id='PARK17',
            layout={
                    'name': 'dagre',
                    'idealEdgeLength': 100,
                    'nodeOverlap': 20,
                    'refresh': 20,
                    'fit': True,
                    'padding': 30,
                    'randomize': False,
                    'componentSpacing': 100,
                    'nodeRepulsion': 400000,
                    'edgeElasticity': 100,
                    'nestingFactor': 5,
                    'gravity': 80,
                    'numIter': 1000,
                    'initialTemp': 200,
                    'coolingFactor': 0.95,
                    'minTemp': 1.0
                },
            style={'width': '100%', 'height': '600px'},
            elements = protienData,
            responsive=True,
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(id)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'label': 'data(weight)'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        # The default curve style does not work with certain arrows
                        'curve-style': 'bezier'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'source-arrow-color': 'black',
                        'source-arrow-shape': 'triangle',
                        'line-color': 'gray'
                    }
                }
            ]
        ),
            html.P(id='cytoscape-tapEdgeData-output')
    ])
])


@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              Input('PARK17', 'tapEdgeData'))
def displayTapEdgeData(data):
    if data:
        return "EDGE SELECT:   ", "SOURCE: ", data['source'], "  |  TARGET: ", data['target'], '  |  WEIGHT: ', data['weight']


@app.callback(Output('PARK17', 'responsive'), 
                [Input('toggle-button', 'n_clicks')])

def toggle_responsive(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    return toggle_on


@app.callback(Output('toggle-text', 'children'), [Input('PARK17', 'responsive')])
def update_toggle_text(responsive):
    return '\t' + 'Responsive ' + ('On' if responsive else 'Off')

if __name__ == '__main__':
    app.run_server(debug=True)