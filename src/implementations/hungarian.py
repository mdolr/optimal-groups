import json
from ..structures.graph import Graph


class Hungarian:
    """
    Algorithme hongrois avec poids

    Sources:
    - https://www-m9.ma.tum.de/graph-algorithms/matchings-hungarian-method/index_en.html
    - https:/yasenh.github.io/post/hungarian-algorithm-2/

    Prend en parametre un graph biparti
    """

    def __init__(self, **kwargs):
        self.graph = kwargs.pop('graph', Graph())
        self.debug = kwargs.pop('debug', False)

        self.matching = Graph()
        self.outputs = {}
        self.logs = ''
        self.step = 0

        self.init_matching()

    def init_matching(self):
        self.matching.add_node(starting_node=True, id='start')
        self.matching.add_node(ending_node=True, id='end')

    def log(self, message):
        self.step += 1
        self.logs += message + '\n'
        print(message)

    def solve(self):
        """
        Une fonction qui applique tout l'algorithme en appelant
        des fonctions complementaires

        Elle renvoit les resultats
        """
        self.initalize_labels(self.graph)

        equality_graph = self.graph.get_equality_graph()

        for edge in equality_graph.starting_node.outgoing_edges:
            self.find_augmenting_path(
                self.graph.get_equality_graph(), edge.child_node.id)

        # 1. on fait un graph d'egalite
        # 2. on cherche le chemin alternatif le plus court
        # on considere un chemin comme alternatif si son point
        # d'arrivee se trouve dans les projets, son point de depart est un groupe
        # et le projet d'arrivee n'est pas sature
        # Si le projet est sature alors on update les poids avec delta
        # puis on continu la recherche d'un chemin alternatif
        # une fois trouve on cherche la version du chemin alternatif la plus courte
        # et on fait les echanges necessaires

        return {'graph': self.matching, 'outputs': self.outputs}

    def find_augmenting_path(self, base_equality_graph, starting_node_id):
        """
        Trouve un chemin tel que le point de depart est un groupe
        le point d'arrive est un projet non sature
        (c'est a dire un projet recevant moins de connexion que sa capacite)
        Le chemin alterne entre groupe et projet
        """

        if self.debug:
            self.log(
                f'Finding a full augmenting path, starting_node={starting_node_id}')

        def find_path(last_node, equality_graph, S, T, starting_node_id, rewrite_matching=False):
            """
            ...
            """

            if self.debug:
                self.log(f'Finding path from {last_node.id}\n- S={S}\n- T={T}')

                # self.graph.draw(bipartite=False,
                #                title=f'Find path from {last_node.id} - Full graph')

                self.log(f'Saving equality graph - Step: {self.step}')

                equality_graph.draw(
                    bipartite=False, title=f'Find path from {last_node.id} - Equality graph', step=self.step)

            # On a un groupe
            # On veut trouver un augmenting path (i.e un chemin qui zig zag)
            # qui termine dans un projet non sature
            if 'Groupe' in last_node.id:

                saturated_projects = []

                # On veut explorer toutes les connexions
                # sortantes de ce groupe (donc vers des projet)
                # pour acceder aux projets enfants
                for edge in last_node.outgoing_edges:

                    # On cherche un noeud pas visite et pas sature
                    # si l'on en trouve un
                    if not edge.child_node.id in T:

                        # On va iterer la boucle entierement mais on garde en memoire
                        # les projets satures que l'on a pas visite

                        # Utiliser la node du graph de matching pour tester saturation
                        # en checkant d'abord si la node existe

                        matching_child = self.matching.get_node_by_id(
                            edge.child_node.id)

                        matching_parent = self.matching.get_node_by_id(
                            edge.parent_node.id)

                        if not matching_child or not matching_child.is_saturated():
                            # Si c'est le lien final
                            if self.debug:
                                self.log(
                                    f'Final link found {edge.parent_node.id} to {edge.child_node.id} W: {edge.weight}')

                            # On a trouve une destination non saturee
                            # dans le cote des projets c'est a dire un augmenting path
                            # si on a trouve un tel path alors on a fini, on retourne met a jour le matching

                            # Creer les nodes avant de les ajouter en checkant si nodes existent pas deja
                            if rewrite_matching:
                                T.append(edge.child_node.id)
                                self.update_matching(S=S, T=T)

                            return self.matching

                        else:
                            saturated_projects.append(edge.child_node)

                # Si on en arrive la, cela veut dire que l'on a pas
                # obtenu de destination satisfaisante pour terminer notre
                # augmenting path.

                # S'il existe un projet sature mais non visite (pas dans T)
                # on veut alors update les labels en calculant delta pour
                # se donner de nouvelles options

                # On applique la mise a jour des labels de chaque noeud
                # en utilisant le calcul de delta

                # On remonte la connexion de notre projet sature dans le matching
                if len(saturated_projects) > 0:

                    # On rajoute le noeud d'un projet dans T
                    # choisi arbitrairement parmi les projets satures
                    T.append(saturated_projects[0].id)

                    matching_parent = self.matching.get_node_by_id(
                        saturated_projects[0].id)

                    # On utilise le premier enfant du projet
                    if len(matching_parent.incoming_edges) > 0:
                        S.append(
                            matching_parent.incoming_edges[0].parent_node.id)

                # Si S a d'autres possibilites on relance avec
                # C'est a dire le noeud ayant la possibilite de connecter a d'autres projets
                possible_edges = [edge for edge in equality_graph.get_node_by_id(
                    S[-1]).outgoing_edges if edge.child_node.id not in T]

                if len(possible_edges) > 0:
                    equality_graph = self.graph.get_equality_graph()
                    new_last_node = equality_graph.get_node_by_id(S[-1])

                # Sinon on delta update
                else:
                    delta = self.update_delta_labels(S=S, T=T)

                    if delta == 0:
                        raise Exception(
                            f'Probleme potentiel pour le groupe {starting_node_id}, pas de solution ? (Delta 0)')

                    S = [starting_node_id]
                    T = []

                    equality_graph = self.graph.get_equality_graph()
                    new_last_node = equality_graph.get_node_by_id(
                        starting_node_id)

                return find_path(last_node=new_last_node, equality_graph=equality_graph, S=S, T=T, starting_node_id=starting_node_id, rewrite_matching=rewrite_matching)

        # On fait tourner une premiere fois la fonction pour trouver un augmenting path
        find_path(last_node=base_equality_graph.get_node_by_id(starting_node_id),
                  equality_graph=base_equality_graph, S=[
                      starting_node_id], T=[],
                  starting_node_id=starting_node_id, rewrite_matching=False)

        if self.debug:
            self.log('Found path, recomputing shortest path to update matching')

        # Puis une 2nde fois en lui demandant de reecrire le matching avec le chemin le plus court cette fois ci
        return find_path(last_node=self.graph.get_equality_graph().get_node_by_id(starting_node_id), equality_graph=self.graph.get_equality_graph(), S=[starting_node_id], T=[], starting_node_id=starting_node_id, rewrite_matching=True)

    def update_matching(self, S, T):
        """
        Regenere le graph de matching depuis 0 en y
        changeant les connexions qui doivent etre 
        changees a chaque nouvel ajout
        """

        if self.debug:
            self.log(f'Update matching using\n- S={S}\n- T={T}')

        for i in range(0, len(S)):
            edge = self.graph.get_edge(self.graph.get_node_by_id(
                S[i]), self.graph.get_node_by_id(T[i]))

            self.outputs[S[i]] = {'weight': int(edge.weight),
                                  'destination_node_id': T[i]}

        self.matching = Graph()

        for source_node_id, connection in self.outputs.items():

            source_node_original = self.graph.get_node_by_id(source_node_id)
            destination_node_original = self.graph.get_node_by_id(
                connection['destination_node_id'])

            source_node = self.matching.get_node_by_id(source_node_id)

            if not source_node:
                source_node = self.matching.add_node(
                    id=source_node_original.id,
                    name=source_node_original.name,
                    label=source_node_original.label,
                    limit_capacity=source_node_original.limit_capacity,
                    current_capacity=source_node_original.current_capacity)

            destination_node = self.matching.get_node_by_id(
                connection['destination_node_id'])

            if not destination_node:
                destination_node = self.matching.add_node(
                    id=destination_node_original.id,
                    name=destination_node_original.name,
                    label=destination_node_original.label,
                    limit_capacity=destination_node_original.limit_capacity,
                    current_capacity=destination_node_original.current_capacity)

            self.matching.add_edge(
                source_node, destination_node, weight=int(connection['weight']))

        if self.debug:
            self.log(f'Saving matching graph - Step: {self.step}')

            self.matching.draw(
                bipartite=False, title='Updated matching - Matching graph', step=self.step)

            self.log(json.dumps(self.outputs, indent=4))

            # self.graph.draw(bipartite=False,
            #                title='Updated matching - Full graph')

        return self.matching

    def initalize_labels(self, graph):
        """
        Initialise la valeur de chaque noeud projet
        """
        for edge in graph.starting_node.outgoing_edges:
            # Recherche de la connexion avec le poids le plus haut
            highest_weight = max(
                [int(edge.weight) for edge in edge.child_node.outgoing_edges])

            # on met a jour la valeur du noeud comme le plus haut poids
            edge.child_node.label = int(highest_weight)

        if self.debug:
            self.log(f'Initializing label saving graph - Step: {self.step}')
            self.graph.draw(bipartite=False,
                            title='Initialize labels', step=self.step)

    def update_delta_labels(self, S, T):
        """
        Mise a jour des valeurs de chaque noeud avec calcul
        du delta minimum
        """
        if self.debug:
            self.log(f'Updating labels using the following\n- S={S}\n- T={T}')

        delta = None

        # On veut calculer le delta minimum
        for node_id in S:

            # Pour chaque noeud dans S
            S_node = self.graph.get_node_by_id(node_id)
            for edge in S_node.outgoing_edges:

                # on veut calculer le delta de chaque connexion vers
                # un noeud pas inclus dans T
                if not(edge.child_node.id in T):

                    if self.debug:
                        self.log(
                            f'Calculating Delta : {(int(edge.parent_node.label) + int(edge.child_node.label) - int(edge.weight))} {edge.parent_node.label} ({edge.parent_node.id}) + {edge.child_node.label} ({edge.child_node.id}) - {edge.weight}')

                    # on recherche le delta minimum
                    edge_delta = (int(edge.parent_node.label) +
                                  int(edge.child_node.label) - int(edge.weight))

                    if delta is None or edge_delta < delta:
                        delta = edge_delta

        if self.debug:
            self.log(f'Delta={delta}')

        # Une fois delta trouve on veut update les valeur de chaque noeud
        if delta is not None:
            # Les noeuds de la categorie S (les groupes)
            # se font enlever delta
            for node_id in S:
                node = self.graph.get_node_by_id(node_id)
                node.label -= delta

            # Les noeuds de la categorie T (les projets)
            # se font ajouter delta
            for node_id in T:
                node = self.graph.get_node_by_id(node_id)
                node.label += delta

        if self.debug:
            # self.graph.get_equality_graph().draw(
            #    bipartite=False, title='Updated labels - Equality graph')

            # self.graph.draw(bipartite=False,
            #                title='Updated labels - Full graph')

            return delta
