from src.structures.node import Node
from src.structures.edge import Edge
from src.structures.graph import Graph
import csv


def load_data(path):
    f = open(path) 
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    return reader,header

def create_graph(group_path, project_path):
    graph = Graph()
    graph.add_node(starting_node=True, id='start')
    graph.add_node(ending_node=True, id='end')

    project_rows, project_header = load_data(project_path)

    project_count = 0
    
    for row in project_rows:
        node = graph.add_node(id=row[0], limit_capacity=row[1])
        graph.add_edge(parent_node=node, child_node=graph.ending_node)
        project_count += 1

    graph.ending_node.limit_capacity = project_count

    group_rows, group_header = load_data(group_path)

    for row in group_rows:
        node = graph.add_node(id=row[0])
        graph.add_edge(parent_node=graph.starting_node, child_node=node)
        
        weigh = len(row)

        for i in range(1, weigh):
            edge = graph.add_edge(parent_node=node, child_node=graph.get_node_by_id(row[i]), weigh=weigh - 1)
    

    return graph