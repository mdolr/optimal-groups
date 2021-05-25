from .node import Node
from .edge import Edge

# Seulement utilise pour representer les graphiques
# dans le but de debugger de maniere plus pratique
import matplotlib.pyplot as plt
import networkx as nx


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

    def remove_node(self, delete_node):
        """
        Supprime une node et ses edges du reseau
        """
        for edge in delete_node.outgoing_edges:
            self.remove_edge(delete_node, edge.child_node)

        for edge in delete_node.incoming_edges:
            self.remove_edge(edge.parent_node, delete_node)

        # On filtre la node qu'on veut supprimer
        self.nodes = [node for node in self.nodes if delete_node.id != node.id]

        return True

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

        parent_node.outgoing_edges.append(edge)
        child_node.incoming_edges.append(edge)

        return edge

    def get_edge(self, parent_node, child_node):
        return [edge for edge in parent_node.outgoing_edges if (
            edge.parent_node.id == parent_node.id and edge.child_node.id == child_node.id)][0] if len([edge for edge in parent_node.outgoing_edges if edge.parent_node.id == parent_node.id and edge.child_node.id == child_node.id]) > 0 else None

    def remove_edge(self, parent_node, child_node):
        """
        Supprime une connexion entre 2 nodes
        Renvoi True si succes
        False sinon
        """

        delete_edge = self.get_edge(parent_node, child_node)

        if delete_edge:
            # On filtre l'edge qu'on veut supprimer
            parent_node.outgoing_edges = [
                edge for edge in parent_node.outgoing_edges if delete_edge.id != edge.id]

            child_node.incoming_edges = [
                edge for edge in child_node.incoming_edges if delete_edge.id != edge.id]

            self.edges = [
                edge for edge in self.edges if delete_edge.id != edge.id]

            return True

        else:
            return False

    def get_node_by_id(self, node_id):
        """
        Renvoi une node par rapport a son id
        """
        return [node for node in self.nodes if node.id == node_id][0] if len([node for node in self.nodes if node.id == node_id]) > 0 else None

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

    def draw(self, bipartite, step, save=True, **kwargs):
        """
        Permet de dessiner le graphique pour debugger
        avec plus de confort

        Credits:
        affichage des couleurs d'edge: https://stackoverflow.com/a/25651827
        affichage des labels d'edge: https://stackoverflow.com/a/28372251
        """
        g = nx.Graph()
        title = kwargs.pop('title', 'Unnamed graph')
        print(f'Title {title}')

        for node in self.nodes:
            if node.id != 'start' and node.id != 'end':
                # Trouver le numero du projet ou de la node
                node_pos = node.id.replace('Groupe', '').replace('Projet', '')

                g.add_node(f'{node.id}:{node.label}', pos=(
                    int(node_pos), 2 if 'Projet' in node.id else 0))

        for edge in self.edges:
            if edge.parent_node.id not in ['start', 'end'] and edge.child_node.id not in ['start', 'end']:

                color = 'gray'

                if edge.parent_node.label + edge.child_node.label == edge.weight:
                    color = 'black'

                g.add_edge(f'{edge.parent_node.id}:{edge.parent_node.label}',
                           f'{edge.child_node.id}:{edge.child_node.label}', weightt=edge.weight, length=100, color=color)

        if bipartite:
            X, Y = nx.bipartite.sets(g)
            pos = dict()
            pos.update((n, (1, i))
                       for i, n in enumerate(X))  # put nodes from X at x=1
            pos.update((n, (2, i))
                       for i, n in enumerate(Y))  # put nodes from Y at x=2

            edges = g.edges()
            colors = [g[u][v]['color'] for u, v in edges]
            weightts = [g[u][v]['weightt'] for u, v in edges]

            positions = nx.get_node_attributes(g, 'pos')
            nx.draw(g, pos=positions, edge_color=colors,
                    width=weightts, with_labels=True)

            labels = nx.get_edge_attributes(g, 'weightt')

            nx.draw_networkx_edge_labels(
                g, positions, edge_labels=labels, label_pos=0.2)

            plt.savefig(f'./{step}.png')
            plt.title(title)
            plt.show()
        else:

            edges = g.edges()
            colors = [g[u][v]['color'] for u, v in edges]
            weightts = [2 for u, v in edges]

            positions = nx.get_node_attributes(g, 'pos')
            nx.draw(g, positions, edge_color=colors,
                    width=weightts, with_labels=True)

            labels = nx.get_edge_attributes(g, 'weightt')

            nx.draw_networkx_edge_labels(
                g, positions, edge_labels=labels, label_pos=0.2)

            plt.savefig(f'./{step}.png')
            plt.title(title)
            plt.show()

    def get_equality_graph(self):
        """
        Retourne le graph egalitaire, c'est a dire un graph dans lequel
        la somme des valeurs des noeuds de depart et d'arrivee d'une connexion
        est egale au poids de la connexion
        """

        # On construit un objet graph
        equality_graph = Graph()
        equality_graph.add_node(starting_node=True, id='start')
        equality_graph.add_node(ending_node=True, id='end')

        # On ajoute chaque projet en parent du noeud
        # d'arrivee
        for edge in self.ending_node.incoming_edges:
            node = equality_graph.add_node(
                id=edge.parent_node.id,
                name=edge.parent_node.name,
                label=edge.parent_node.label,
                limit_capacity=edge.parent_node.limit_capacity,
                current_capacity=edge.parent_node.current_capacity
            )

            equality_graph.add_edge(parent_node=node,
                                    child_node=equality_graph.ending_node)

        # De meme pour chaque noeud enfant du
        # point de depart
        for edge in self.starting_node.outgoing_edges:
            node = equality_graph.add_node(
                id=edge.child_node.id,
                name=edge.child_node.name,
                label=edge.child_node.label,
                limit_capacity=edge.child_node.limit_capacity,
                current_capacity=edge.child_node.current_capacity
            )

            equality_graph.add_edge(parent_node=equality_graph.starting_node,
                                    child_node=node)

            # Puis on relie les noeuds remplissant la condition d'egalite
            for middle_edge in edge.child_node.outgoing_edges:
                if middle_edge.weight == (middle_edge.parent_node.label + middle_edge.child_node.label):
                    edge = equality_graph.add_edge(
                        parent_node=equality_graph.get_node_by_id(
                            middle_edge.parent_node.id),
                        child_node=equality_graph.get_node_by_id(
                            middle_edge.child_node.id),
                        weight=middle_edge.weight)

        return equality_graph
