from ..structures.graph import Graph


class Hungarian:
    """
    Algorithme hongrois avec poids

    Sources: 
    - https://www-m9.ma.tum.de/graph-algorithms/matchings-hungarian-method/index_en.html
    - https://yasenh.github.io/post/hungarian-algorithm-2/

    Prend en parametre un graph biparti
    """

    def __init__(self, **kwargs):
        self.matching = Graph()
        self.matching.add_node(starting_node=True, id='start')
        self.matching.add_node(ending_node=True, id='end')

    def solve(self, graph):
        """
        Une fonction qui applique tout l'algorithme en appelant
        des fonctions complementaires

        Elle renvoit les resultats
        """
        self.initalize_labels(graph)

        equality_graph = graph.get_equality_graph(graph)

        for i in range(0, 5):
            # On veut trouver un chemin
            print(i)
            for edge in equality_graph.starting_node.outgoing_edges[i].child_node.outgoing_edges:
                print(edge.child_node.id)
                if not(edge.child_node.is_saturated()):
                    print('ALLO')
                    # On ajoute le groupe
                    group_node = self.matching.add_node(
                        id=equality_graph.starting_node.outgoing_edges[i].child_node.id,
                        name=equality_graph.starting_node.outgoing_edges[i].child_node.name,
                        label=equality_graph.starting_node.outgoing_edges[i].child_node.label,
                        limit_capacity=equality_graph.starting_node.outgoing_edges[
                            i].child_node.limit_capacity,
                        current_capacity=equality_graph.starting_node.outgoing_edges[
                            i].child_node.current_capacity
                    )

                    # Puis le projet
                    project_node = self.matching.add_node(
                        id=edge.parent_node.id,
                        name=edge.parent_node.name,
                        label=edge.parent_node.label,
                        limit_capacity=edge.parent_node.limit_capacity,
                        current_capacity=edge.parent_node.current_capacity
                    )

                    edge = self.matching.add_edge(parent_node=group_node,
                                                  child_node=project_node,
                                                  weigh=edge.weigh)

                    print(
                        f'{edge.parent_node.id} to {edge.child_node.id} Weigh: {edge.weigh}')

        return self.matching

    def initalize_labels(self, graph):
        """
        Initialise la valeur de chaque noeud projet
        """
        for edge in graph.starting_node.outgoing_edges:
            # Recherche de la connexion avec le poids le plus haut
            highest_weigh = max(
                [edge.weigh for edge in edge.child_node.outgoing_edges])

            # on met a jour la valeur du noeud comme le plus haut poids
            edge.child_node.update_label(highest_weigh)
