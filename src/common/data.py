from src.structures.node import Node
from src.structures.edge import Edge
from src.structures.graph import Graph
import csv

#f=load_data('choix.csv')

graph = Graph()
graph.add_node(starting_node=True)
graph.add_node(ending_node=True)


def load_data(path):
    return open(path)

def load_groups(f):
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    for row in reader:
        graph.add_node(id=row[0])
    prtin(graph)



"""
reader = csv.reader(f, delimiter=',')
header = next(reader)
graph={}
for row in reader:
    pref_count = len(row)
    choix={}
    for i in range(1,pref_count):
        choix.update({ row[i] : {'cost':pref_count -i}})
    groupe = {row[0]:choix}
    graph.update(groupe)
print(graph)
"""