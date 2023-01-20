"""
Excel String-DB API KEGG Pathway Labelling Utilizing Louvain Sorting Algorithms

DaCapo Brainscience, Inc.

Created by Eli Murphy

January, 2023
"""

import requests 
import json
import pandas as pd
import time
import networkx.algorithms.community as nx_comm 
import os
import networkx as nx

os.chdir(r"C:\Users\elija\Documents\GitHub\dcb-network\StatOutput")
csvpath = r"C:\Users\elija\Documents\GitHub\dcb-network\datasets\ppi_simplified.csv"
edgelist = []


string_api_url = "https://version-11-5.string-db.org/api"
output_format = "json"
method = "enrichment"
request_url = "/".join([string_api_url, output_format, method])
cat='Function'                       #'PMID','Component','Process','Function','KEGG','Interpro'
sp=9606                              # species NCBI identifier
p=0.05                               #p-value cutoff

output_file='output'                 #output filename

def main():

    G = nx.Graph()

    file_ext = os.path.basename(csvpath)
    filename = os.path.splitext(file_ext)[0]
    exportFileName = str(filename + "-Protien-Interaction-Network-Stats" + ".xlsx")

    print("Statistic Calculations Starting...\n")

    with open(csvpath, "r") as csv:
        next(csv)
        for row in csv:
            splitRow = row.split(",")
            splitRow[2] = splitRow[2].replace("\n", "")
            edgelist.append((splitRow[0], splitRow[1], float(splitRow[2])))
    G.add_weighted_edges_from(edgelist)

    dfR31 = louvainAndKEGG(G, resolution=3.1)
    dfR32 = louvainAndKEGG(G, resolution=3.2)
    dfR33 = louvainAndKEGG(G, resolution=3.3)
    dfR34 = louvainAndKEGG(G, resolution=3.4)
    dfR35 = louvainAndKEGG(G, resolution=3.5)
    dfR36 = louvainAndKEGG(G, resolution=3.6)
    dfR37 = louvainAndKEGG(G, resolution=3.7)
    dfR38 = louvainAndKEGG(G, resolution=3.8)
    dfR39 = louvainAndKEGG(G, resolution=3.9)

    with pd.ExcelWriter('LouvainAPITest3.1-3.9.xlsx') as writer:

        dfR31[0].to_excel(writer, sheet_name='R3.1 Test', index=False, header=True)
        dfR32[0].to_excel(writer, sheet_name='R3.2 Test', index=False, header=True)
        dfR33[0].to_excel(writer, sheet_name='R3.3 Test', index=False, header=True)
        dfR34[0].to_excel(writer, sheet_name='R3.4 Test', index=False, header=True)
        dfR35[0].to_excel(writer, sheet_name='R3.5 Test', index=False, header=True)
        dfR36[0].to_excel(writer, sheet_name='R3.6 Test', index=False, header=True)
        dfR37[0].to_excel(writer, sheet_name='R3.7 Test', index=False, header=True)
        dfR38[0].to_excel(writer, sheet_name='R3.8 Test', index=False, header=True)
        dfR39[0].to_excel(writer, sheet_name='R3.9 Test', index=False, header=True)
        writer.sheets["R3.1 Test"].set_column(0, len(dfR31[1]), 35)
        writer.sheets["R3.2 Test"].set_column(0, len(dfR32[1]), 35)
        writer.sheets["R3.3 Test"].set_column(0, len(dfR33[1]), 35)
        writer.sheets["R3.4 Test"].set_column(0, len(dfR34[1]), 35)
        writer.sheets["R3.5 Test"].set_column(0, len(dfR35[1]), 35)
        writer.sheets["R3.6 Test"].set_column(0, len(dfR36[1]), 35)
        writer.sheets["R3.7 Test"].set_column(0, len(dfR37[1]), 35)
        writer.sheets["R3.8 Test"].set_column(0, len(dfR38[1]), 35)
        writer.sheets["R3.9 Test"].set_column(0, len(dfR39[1]), 35)
        


def louvainAndKEGG(G, resolution):
    st = time.time()
    print("Louvian Sorting Algorithm Computing...")

    data = {}
    columns = []
    count = 1
    safety = " "
    maxlen = 0

    lc = nx_comm.louvain_communities(G, resolution=resolution)

    lccount = 0
    for i in list(sorted(lc, key=len, reverse=True)):
        resultList = list(i)
        my_genes = resultList

        params = {

        "identifiers" : "%0d".join(my_genes),
        "species" : sp, 
        }

        response = requests.post(request_url, data=params)
        apidata = json.loads(response.text)


        outputs = []

        for row in apidata:

            description = row["description"]
            number_of_genes = str(row["number_of_genes"])
            category = row["category"]
            p_value = float(row["p_value"])
            if category == "KEGG":
                
                outputs.append([number_of_genes, p_value, description])

        outputs = sorted(outputs, key=lambda x: x[1], reverse=False)

        columnName = str("Gene Set "+ str(count))
        count += 1
        
        if len(outputs) >= 3:
            print("")
            resultList.insert(0,"")
            resultList.insert(0, "P Value: "+ str(outputs[2][1]))
            resultList.insert(0, "Number of genes: "+ str(outputs[2][0]))
            resultList.insert(0,outputs[2][2])
            resultList.insert(0, "P Value: "+ str(outputs[1][1]))
            resultList.insert(0, "Number of genes: "+ str(outputs[1][0]))
            resultList.insert(0,outputs[1][2])
            resultList.insert(0, "P Value: "+ str(outputs[0][1]))
            resultList.insert(0, "Number of genes: "+ str(outputs[0][0]))
            resultList.insert(0,outputs[0][2])
            resultList.insert(0,"")
            
    
        else:
            if len(outputs) == 2:
                print("Try 2")
                [resultList.insert(0,"") for i in range(4)]
                resultList.insert(0, "P Value: "+ str(outputs[1][1]))
                resultList.insert(0, "Number of genes: "+ str(outputs[1][0]))
                resultList.insert(0,outputs[1][2])
                resultList.insert(0, "P Value: "+ str(outputs[0][1]))
                resultList.insert(0, "Number of genes: "+ str(outputs[0][0]))
                resultList.insert(0,outputs[0][2])
                resultList.insert(0,"")
            else:
                if len(outputs) == 1:
                    print("Try 3")
                    [resultList.insert(0,"") for i in range(7)]
                    resultList.insert(0, "P Value: "+ str(outputs[0][1]))
                    resultList.insert(0, "Number of genes: "+ str(outputs[0][0]))
                    resultList.insert(0,outputs[0][2])
                    resultList.insert(0,"")
                else:
                    [resultList.insert(0,"") for i in range(9)]
                    resultList.insert(0, "NO KEGG PATHWAYS DETECTED")
                    resultList.insert(0,"")



        if columnName in data.keys():
            columnName = columnName + safety
            safety += " "

        columns.append(columnName)

        


        data[columnName] = resultList
        
        if maxlen < len(resultList):
            maxlen = len(resultList)
        else:
            while len(resultList) < maxlen:
                resultList.append("")

    df = pd.DataFrame.from_dict(data, orient='columns')
    df.columns = columns

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Louvian Sorting Algorithm Complete | Execution time:', elapsed_time, 'seconds\n')

    return [df, columns]

main()
