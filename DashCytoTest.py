
from dash import Dash, html
import dash_cytoscape as cyto
import os
from num2words import num2words

os.chdir(r"C:\Users\elija\Documents\GitHub\DaCapo")

file = input("Input CSV Filename (include .csv): ")

protienData = []

with open(file, "r") as csv:
    next(csv)
    data = csv.readlines()
    fromnode = []
    tonode = []
    weights = []
    count = 1
    for r in range(len(data)):
        temp = {}
        row = data[r].split(",")
        if str(row[0]) in str(protienData):
            continue
        else:
            temp['data'] = {'id': num2words(count), 'label': row[0]}
        protienData.append(temp)
        count += 1
    protienData.append({'data': {'source': 'one', 'target': 'two'}})
    protienData.append({'data': {'source': 'two', 'target': 'three'}})
    protienData.append({'data': {'source': 'three', 'target': 'four'}})
    protienData.append({'data': {'source': 'four', 'target': 'five'}})
    protienData.append({'data': {'source': 'five', 'target': 'six'}})
    protienData.append({'data': {'source': 'six', 'target': 'seven'}})
    protienData.append({'data': {'source': 'seven', 'target': 'eight'}})
    protienData.append({'data': {'source': 'eight', 'target': 'nine'}})
    protienData.append({'data': {'source': 'nine', 'target': 'ten'}})
    protienData.append({'data': {'source': 'ten', 'target': 'eleven'}})
    protienData.append({'data': {'source': 'eleven', 'target': 'one'}})

    for i in range(len(protienData)):
        print(protienData[i])

    print(protienData)



app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='PARK17',
        layout={'name': 'cose'},
        style={'width': '500%', 'height': '2000px'},
        elements = protienData
        # elements=[
        #     {'data': {'id': 'one', 'label': 'RAB7A'}},
        #     {'data': {'id': 'two', 'label': 'SNX1'}},
        #     {'data': {'id': 'three', 'label': 'SNX2'}},
        #     {'data': {'id': 'four', 'label': 'SNX3'}},
        #     {'data': {'id': 'five', 'label': 'SNX5'}},
        #     {'data': {'id': 'six', 'label': 'SNX6'}},
        #     {'data': {'id': 'seven', 'label': 'TBC1D5'}},
        #     {'data': {'id': 'eight', 'label': 'VPS26A'}},
        #     {'data': {'id': 'nine', 'label': 'VPS26B'}},
        #     {'data': {'id': 'ten', 'label': 'VPS29'}},
        #     {'data': {'id': 'eleven', 'label': 'VPS35'}},
        #     {'data': {'source': 'one', 'target': 'two'}},
        #     {'data': {'source': 'two', 'target': 'three'}},
        #     {'data': {'source': 'three', 'target': 'four'}},
        #     {'data': {'source': 'four', 'target': 'five'}},
        #     {'data': {'source': 'five', 'target': 'six'}},
        #     {'data': {'source': 'six', 'target': 'seven'}},
        #     {'data': {'source': 'seven', 'target': 'eight'}},
        #     {'data': {'source': 'eight', 'target': 'nine'}},
        #     {'data': {'source': 'nine', 'target': 'ten'}},
        #     {'data': {'source': 'ten', 'target': 'eleven'}},
        #     {'data': {'source': 'eleven', 'target': 'one'}}
        #     ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)