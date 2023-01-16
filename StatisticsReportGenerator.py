"""
Excel Network Statistics Generator Tool

DaCapo Brainscience, Inc.

Created by Eli Murphy

January, 2023
"""

import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt
import xlsxwriter
import os
import time
import pandas as pd

#Modifiable Variables
os.chdir(r"C:\Users\elija\Documents\GitHub\dcb-network\StatOutput")
csvpath = r"C:\Users\elija\Documents\GitHub\dcb-network\datasets\ppi_simplified.csv"
weightMin = .95

def main():
    edgelist = []

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

    dataWeightMin = generalDataWeightMin()

    basicData = basicInfo(G)

    louvianDataFrame = louvain(G)

    histogramGen(G, filename)

    topHubsDict = topHubs(G)

    exportData(basicData, louvianDataFrame, topHubsDict, dataWeightMin, exportFileName)

    print('Absolute path of file: ',os.path.abspath(exportFileName),"\n")
    
    print("Done!")   

def basicInfo(G):
    st = time.time()
    print("Basic Info Computing...")

    data = {}
    SG = [G.subgraph(c).copy() for c in nx.connected_components(G)]

    confidenceTag = "Confidence Limit (" + str(weightMin).replace(".", "") + "%)"

    data[confidenceTag] = ["# of Nodes:", "# of Edges:", "Density", "Diameter", "Transitivity", "Average Clustering Coefficient"] # 

    for i in range(len(SG)):
        nodeCount = nx.number_of_nodes(SG[i])
        edgeCount = nx.number_of_edges(SG[i])
        print("density")
        density = nx.density(SG[i])
        print("diameter")
        diameter = nx.diameter(SG[i])
        print("transitivity")
        transitivity = nx.transitivity(SG[i])
        print("clustering")
        averageClustering = nx.average_clustering(SG[i])
        compName = str("Component #"+ str(i+1))
        data[compName] = [nodeCount, edgeCount, density , diameter, transitivity, averageClustering] #

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Basic Info Complete | Execution time:', elapsed_time, 'seconds\n')
    return data

def louvain(G):

    st = time.time()
    print("Louvian Sorting Algorithm Computing...")

    data = {}
    columns = []
    count = 1
    maxlen = 0

    lc = nx_comm.louvain_communities(G)

    lccount = 0
    for i in list(sorted(lc, key=len, reverse=True)):
        resultList = list(i)

        if maxlen < len(resultList):
            maxlen = len(resultList)
        else:
            while len(resultList) < maxlen:
                resultList.append("")

        columnName = str("Gene Set "+ str(count))
        columns.append(columnName)
        data[columnName] = resultList
        count += 1


    df = pd.DataFrame.from_dict(data, orient='columns')
    df.columns = columns

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Louvian Sorting Algorithm Complete | Execution time:', elapsed_time, 'seconds\n')

    return df

def kCliques(G):
    st = time.time()
    print("K-Clique Sorting Algorithm Computing...")

    data = {}
    columns = []
    count = 1
    maxlen = 0

    lc = nx_comm.louvain_communities(G)

    lccount = 0
    for i in list(sorted(lc, key=len, reverse=True)):
        resultList = list(i)

        if maxlen < len(resultList):
            maxlen = len(resultList)
        else:
            while len(resultList) < maxlen:
                resultList.append("")

        columnName = str("Gene Set "+ str(count))
        columns.append(columnName)
        data[columnName] = resultList
        count += 1


    df = pd.DataFrame.from_dict(data, orient='columns')
    df.columns = columns

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Louvian Sorting Algorithm Complete | Execution time:', elapsed_time, 'seconds\n')

    return df

def histogramGen(G, filename):

    st = time.time()
    print("Histogram Generation Computing...")
    
    weight_sequence = []
    for i in G.edges(data=True):
        weight_sequence.append(i[2]['weight'])
    weight_sequence = sorted(weight_sequence, reverse=False)

    degree_sequence = sorted((d for n, d in G.degree()), reverse=False)
    dmax = max(degree_sequence)


    fig, ax = plt.subplots()

    n_bins=80

    #ax2 = fig.add_subplot(axgrid[1:,2:])
    ax.hist(degree_sequence, bins=n_bins)
    title = "Degree histogram of '" + filename + "'"
    ax.set_title(title)
    ax.set_xlabel("Degree")
    ax.set_ylabel("# of Nodes")
    ax.text(800,240, '', fontsize=12) #Add Legend Data
    plt.savefig("degree_histogram.png")




    fig2, ax2 = plt.subplots()

    n_bins = 80
    ax2.hist(weight_sequence, bins=n_bins)
    title = "Weight histogram of '" + filename + "'"
    ax2.set_title(title) 
    ax2.set_xlabel("Weight")
    ax2.set_ylabel("# of Edges")
    plt.savefig("weight_histogram.png")

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Histogram Generation Complete | Execution time:', elapsed_time, 'seconds\n')

    return ax, ax2

def topHubs(G):

    st = time.time()
    print("Degree Organized Nodes Computing...")

    degreeSort = sorted(G.degree, key=lambda x: x[1], reverse=True)
    output = {}
    protienList = []
    degreeList = []
    for i in range(len(degreeSort)):
        protienList.append(degreeSort[i][0])
        degreeList.append(degreeSort[i][1])

    output["Hubs:"] = protienList
    output["Degrees:"] = degreeList

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Degree Organized Nodes Complete | Execution time:', elapsed_time, 'seconds\n')

    return output

def generalDataWeightMin():
    H = nx.Graph()
    edgelist = []
    with open(csvpath, "r") as csv:
        next(csv)
        for row in csv:
            splitRow = row.split(",")
            splitRow[2] = splitRow[2].replace("\n", "")
            if float(splitRow[2]) >= weightMin: 
                edgelist.append((splitRow[0], splitRow[1], float(splitRow[2])))
    H.add_weighted_edges_from(edgelist)

    return basicInfo(H)

def exportData(basicData, louvianDataFrame, topHubsDict, dataWeightMin, exportFileName):
    st = time.time()
    print("Spreadsheet Generatiing...")

    basicDataDF = pd.DataFrame.from_dict(basicData)
    tophubDF = pd.DataFrame.from_dict(topHubsDict)
    dataWeightMinDF = pd.DataFrame.from_dict(dataWeightMin)

    with pd.ExcelWriter(exportFileName) as writer:
        basicDataDF.to_excel(writer, sheet_name='General PPI Network Data', index=False, header=True)
        dataWeightMinDF.to_excel(writer, sheet_name='Weight Limited Network Data', index=False, header=True)
        tophubDF.to_excel(writer, sheet_name='Top Hubs', index=False, header=True)
        louvianDataFrame.to_excel(writer, sheet_name='Louvian Sorting Algorithm', index=False, header=True)

        workbook  = writer.book
        degWorksheet = workbook.add_worksheet("Degree Histogram") 
        weightWorksheet = workbook.add_worksheet("Weight Histogram") 

        degWorksheet.insert_image('A1', 'degree_histogram.png')
        weightWorksheet.insert_image('A1', 'weight_histogram.png')
    os.remove("degree_histogram.png")
    os.remove("weight_histogram.png")

    et = time.time()
    elapsed_time = round((et - st), 4)
    print('Spreadsheet Generation Complete | Execution time:', elapsed_time, 'seconds\n')

main()