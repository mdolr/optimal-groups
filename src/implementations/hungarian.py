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

        for i in range(0, len(equality_graph.starting_node.outgoing_edges)):
            for edge in equality_graph.starting_node.outgoing_edges[i].child_node.outgoing_edges:

                # On commence par verifier que le projet n'existe pas deja dans le matching
                # ou que s'il existe il n'est pas deja sature
                if not(self.matching.get_node_by_id(edge.child_node.id)) or not(self.matching.get_node_by_id(edge.child_node.id).is_saturated()):

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
                        id=edge.child_node.id,
                        name=edge.child_node.name,
                        label=edge.child_node.label,
                        limit_capacity=edge.child_node.limit_capacity,
                        current_capacity=edge.child_node.current_capacity
                    )

                    edge = self.matching.add_edge(parent_node=group_node,
                                                  child_node=project_node,
                                                  weigh=edge.weigh)

                    print(
                        f'{edge.parent_node.id} to {edge.child_node.id} Weigh: {edge.weigh}')
                else:
                    print('Aie aie les problemes')

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
