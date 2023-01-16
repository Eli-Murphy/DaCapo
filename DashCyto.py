"""
Dash Cytoscape Network Visualization Tool

DaCapo Brainscience, Inc.

Created by Eli Murphy

January 2023
"""

from dash import Dash, html, Input, Output
import dash_cytoscape as cyto
import os

cyto.load_extra_layouts()

for x in os.listdir(r"C:\Users\elija\Documents\GitHub\dcb-network"):
    if x.endswith(".csv"):
        print(x)

fdir = r"C:\Users\elija\Documents\GitHub\dcb-network\datasets"
fname = "PARK17.csv"

file = str(os.path.join(fdir, fname))


print(file)

protienData = []

ncount = 0
ecount = 0
weightAdd = 0

#csv = open(file, "r")

with open(file, "r") as csv:

    next(csv)
    data = csv.readlines()
    for r in range(len(data)):
        temp = {}
        row = data[r].split(",")
        if str(row[0]) in str(protienData):
            continue
        else:
            temp['data'] = {'id': row[0], 'label': row[0], 'sourceCount': 1, 'targetCount': 1}
            ncount += 1
        protienData.append(temp)


    for e in range(len(data)):
        temp = {}
        row = data[e].split(",")
        temp['data'] = {'source': row[0], 'target': row[1], 'weight': row[12]} #Changed for ppi_0.3_subset.csv
        protienData.append(temp)
        ecount += 1
        weightAdd += float(row[12])

    aveWeight = round((weightAdd / ecount), 4)
    #for i in range(len(protienData)):
        #print(protienData[i])

    #print(protienData)

styles = {
    'container': {
        'position': 'fixed',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',
        'width': '100%',
        'font-family': 'Arial, Helvetica, sans-serif'
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
    },
    'NumNodeEdge': {
        'position': 'relative',
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',
        'width': '100%',
        'left': '500px',
        'top':'-50px',
        'font-size' : '16px',
        'font-weight': 'normal',
        'font-family': 'Arial, Helvetica, sans-serif'
    }
}


app = Dash(__name__)

app.layout = html.Div(style=styles['container'], children=[
    html.Div([
        html.Button("Responsive", id='toggle-button'),
            html.Div(id='toggle-text'),
                ]),
    html.Div([
        html.H3("# of Nodes: {n}  |||  # of Edges: {e}  ||| Average Edge Weight: {a}".format(n = ncount, e = ecount, a = aveWeight), style=styles['NumNodeEdge'])
    ]),
    html.Div(className='cy-container', style=styles['cy-container'], children=[
        cyto.Cytoscape(
            id='protienNetwork',
            layout={
                    'name': 'dagre',
                    'spacingFactor': 3,
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
                    'gravity': 0,
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

                #LINE COLORS START

                {
                    'selector': '[weight >= 0][weight <= .2]',
                    'style': {
                        'line-color': '#C5E8B7'
                    }
                },
                {
                    'selector': '[weight > .2 ][weight <= .4]',
                    'style': {
                        'line-color': '#ABE098'
                    }
                },
                {
                    'selector': '[weight > .4 ][weight <= .6]',
                    'style': {
                        'line-color': '#83D475'
                    }
                },
                {
                    'selector': '[weight > .6 ][weight <= .8]',
                    'style': {
                        'line-color': '#57C84D'
                    }
                },
                {
                    'selector': '[weight > .8 ][weight <= 1]',
                    'style': {
                        'line-color': '#2EB62C'
                    }
                },

                #LINE COLOR END

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
                        'source-arrow-color': 'gray',
                        'source-arrow-shape': 'triangle',
                        #'line-color': 'gray'
                    }
                }
            ]
        ),
            html.P(id='cytoscape-tapEdgeData-output'),
            html.P(id='cytoscape-tapNodeData-output')
    ])
])


@app.callback(Output('cytoscape-tapEdgeData-output', 'children'),
              Input('protienNetwork', 'tapEdgeData'))
def displayTapEdgeData(data):
    if data:
        return "EDGE SELECT:   ", "SOURCE: ", data['source'], "  |  TARGET: ", data['target'], '  |  WEIGHT: ', data['weight']


@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              Input('protienNetwork', 'tapNodeData'))
def displayTapEdgeData(data):
    if data:
        return "NODE SELECT:   ", "NAME: ", data['id']


@app.callback(Output('protienNetwork', 'responsive'), 
                [Input('toggle-button', 'n_clicks')])

def toggle_responsive(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    return toggle_on


@app.callback(Output('toggle-text', 'children'), [Input('protienNetwork', 'responsive')])
def update_toggle_text(responsive):
    return '\t' + 'Responsive ' + ('On' if responsive else 'Off')

if __name__ == '__main__':
    app.run_server(debug=True)