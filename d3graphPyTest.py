from d3graph import d3graph, vec2adjmat


with open(r"C:\Users\elija\Documents\GitHub\DaCapo\PARK17 Interactions.csv", "r") as csv:
    next(csv)
    data = csv.readlines()
    #data = list(csv.reader(csv, delimiter=","))
    source = []
    target = []
    weight = []
    temp = []
    for r in data:
        row = r.split(",")
        source.append(row[0])
        target.append(row[1])
        weight.append(round(float(row[12].replace("\n", "")), 2))

        temp.append((row[0], row[1], float(row[12].replace("\n", ""))))

print(source)
print(target)

print(weight)


# Set source and target nodes
#source = ['node A','node F','node B','node B','node B','node A','node C','node Z']
#target = ['node F','node B','node J','node F','node F','node M','node M','node A']
#weight = [5.56, 0.5, 0.64, 0.23, 0.9, 3.28, 0.5, 0.45]

# Create adjacency matrix
adjmat = vec2adjmat(source, target, weight=weight)

# target  node A  node B  node F  node J  node M  node C  node Z
# source                                                        
# node A    0.00     0.0    5.56    0.00    3.28     0.0     0.0
# node B    0.00     0.0    1.13    0.64    0.00     0.0     0.0
# node F    0.00     0.5    0.00    0.00    0.00     0.0     0.0
# node J    0.00     0.0    0.00    0.00    0.00     0.0     0.0
# node M    0.00     0.0    0.00    0.00    0.00     0.0     0.0
# node C    0.00     0.0    0.00    0.00    0.50     0.0     0.0
# node Z    0.45     0.0    0.00    0.00    0.00     0.0     0.0

# Initialize
# Initialize
d3 = d3graph(charge=1000, collision=1)
d3.graph(adjmat)
d3.set_edge_properties(directed=True, edge_distance=200, scaler='zscore')

d3.set_node_properties(color='#000000', size=5, edge_size=.1, edge_color='#000FFF', cmap='Set4')
d3.show()# Example A: simple interactive network

