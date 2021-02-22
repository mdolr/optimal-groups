from .node import Node
from .edge import Edge


class Graph:
    """
    Represente un graph contenant des nodes et des edges
    """

    def __init__(self, **kwargs):
        self.starting_node = kwargs.pop('starting_node', None)
        self.ending_node = kwargs.pop('ending_node', None)

        self.nodes = kwargs.pop('nodes', [])
        self.edges = kwargs.pop('edges', [])

        self.next_id = 0

    def add_node(self, starting_node=False, ending_node=False, **kwargs):
        """
        Rajoute une node
        """
        kwargs['graph'] = self

        # systeme d'identifiant automatique
        if not(kwargs.get('id', False)):
            kwargs['id'] = str(self.next_id)
            self.next_id += 1

        node = Node(**kwargs)
        self.nodes.append(node)

        if starting_node:
            self.set_starting_node(node)

        if ending_node:
            self.set_ending_node(node)

        return node

    def remove_node(self, node):
        """
        Supprime une node et ses edges du reseau
        """

    def add_edge(self, parent_node, child_node, **kwargs):
        """
        Ajoute une connexion entre 2 nodes
        """
        kwargs['graph'] = self

        if not(kwargs.get('id', False)):
            kwargs['id'] = str(self.next_id)
            self.next_id += 1

        edge = Edge(parent_node=parent_node, child_node=child_node, **kwargs)

        self.edges.append(edge)
        parent_node.edges.append(edge)

        return edge

    def get_node_by_id(self, node_id):
        """
        Renvoi une node par rapport a son id
        """
        return [node for node in self.nodes if node.id == node_id][0]

    def set_starting_node(self, node):
        """
        Definit une node comme le point de depart
        """
        self.starting_node = node

    def set_ending_node(self, node):
        """
        Definit une node comme le point d'arrivee
        """
        self.ending_node = node
