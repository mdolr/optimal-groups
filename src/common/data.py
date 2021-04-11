from src.structures.node import Node
from src.structures.edge import Edge
from src.structures.graph import Graph
from src.common.weight import get_weight
import csv


def load_data(path):
    """
    On charge le fichier csv precise en argument,
    puis on retourne d'un part l'entete
    et d'autre part les valeurs
    """
    f = open(path)
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    return reader, header


def create_output_file(matching_outputs, output_file_path):

    f = open(output_file_path, "w")
    weight_sum = 0

    for group, connection in matching_outputs.items():
        weight_sum += int(connection['weight'])

        line = f"{group} : {connection['destination_node_id']} - Score : {connection['weight']}\n"
        f.write(line)

    # f.write(f'\nSatisfaction score : {weight_sum} / {5 } ({})')

    f.close()


def create_graph(group_path, project_path, weighing_method='decreasing'):
    graph = Graph()
    graph.add_node(starting_node=True, id='start')
    graph.add_node(ending_node=True, id='end')

    """
    On cree notre graph, puis on ajoute les noeuds principaux:
    la source et le puit
    """

    project_rows, project_header = load_data(project_path)

    project_count = 0

    capacity = {}

    for row in project_rows:
        node = graph.add_node(id=row[0], limit_capacity=int(row[1]))

        graph.add_edge(parent_node=node,
                       child_node=graph.ending_node,
                       limit_capacity=1)

        # on stocke la capacite pour plus tard
        capacity[row[0]] = int(row[1])

        project_count += 1

    """
    On utilise la fonction load_data() afin de charger le fichier csv contenant,
    les projets et la capacite maximum (fichier definis par les profs)

    puis on boucle sur l'objet reader qui nous permet de cree au fur et a mesure
    les sommets, une fois le sommet initialise on cree l'arrete entre celui-ci 
    et le puits (ending_node)
    """
    graph.ending_node.limit_capacity = project_count

    group_rows, group_header = load_data(group_path)

    for row in group_rows:
        node = graph.add_node(id=row[0])

        graph.add_edge(parent_node=graph.starting_node,
                       child_node=node, limit_capacity=1)

        for i in range(1, len(row)):
            graph.add_edge(parent_node=node,
                           child_node=graph.get_node_by_id(row[i]),
                           weight=get_weight(
                               int(len(row) - i), method=weighing_method),
                           limit_capacity=capacity.get(row[i], 0))

    """
    On initialise de la meme maniere les groupes grâces au fichier csv
    contenant les groupes et leur choix respectif, de la meme maniere
    on boucle sur l'objet reader et  on initialise les sommets, puis
    on cree les arretes entre les sommets A (ici les groupes) et les sommets B (les projet)
    en attribuant a chaque liaison un poids (qui represente la preference)
    """

    return graph
