data = {'nodes': [{'name': 'Mike', 'group': 1},{'name': 'Chloe', 'group': 1},{'name': 'Eli', 'group': 1}], 'links': [{'source': 1, 'target': 0, 'value': 1},{'source': 0, 'target': 2, 'value': 1},{'source': 1, 'target': 2, 'value': 1}]}

from dash import Dash, html
import dash_cytoscape as cyto
import os

# os.chdir(r"C:\Users\elija\Documents\GitHub\DaCapo")

# file = input("Input CSV Filename (include .csv): ")

# with open(file, "r") as csv:
#     next(csv)
#     data = csv.readlines()
#     fromnode = []
#     tonode = []
#     weights = []


app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}},
            {'data': {'id': 'two', 'label': 'Node 2'}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)