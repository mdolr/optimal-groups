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
        self.matching = Graph()
        self.matched_projects = []
        self.init_matching()

    def init_matching(self):
        self.matching.add_node(starting_node=True, id='start')
        self.matching.add_node(ending_node=True, id='end')

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

        return self.matching

    def find_augmenting_path(self, base_equality_graph, starting_node_id):
        """
        Trouve un chemin tel que le point de depart est un groupe
        le point d'arrive est un projet non sature
        (c'est a dire un projet recevant moins de connexion que sa capacite)
        Le chemin alterne entre groupe et projet
        """

        print(
            f'Finding a full augmenting path, starting_node={starting_node_id}')

        def find_path(last_node, equality_graph, S, T):
            """
            ...
            """
            print(f'Finding path from {last_node.id}\n- S={S}\n- T={T}')
            self.matching.draw(bipartite=False)

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
                            print(
                                f'Final link found {edge.parent_node.id} to {edge.child_node.id} W: {edge.weigh}')

                            # On a trouve une destination non saturee
                            # dans le cote des projets c'est a dire un augmenting path
                            # si on a trouve un tel path alors on a fini, on retourne met a jour le matching

                            # Creer les nodes avant de les ajouter en checkant si nodes existent pas deja

                            if not self.matching.get_node_by_id(edge.child_node.id):
                                matching_child = self.matching.add_node(
                                    id=edge.child_node.id,
                                    name=edge.child_node.name,
                                    label=edge.child_node.label,
                                    limit_capacity=edge.child_node.limit_capacity,
                                    current_capacity=edge.child_node.current_capacity)

                            if not self.matching.get_node_by_id(edge.parent_node.id):
                                matching_parent = self.matching.add_node(
                                    id=edge.parent_node.id,
                                    name=edge.parent_node.name,
                                    label=edge.parent_node.label,
                                    limit_capacity=edge.parent_node.limit_capacity,
                                    current_capacity=edge.parent_node.current_capacity)

                            self.matching.add_edge(
                                matching_parent, matching_child)

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
                self.delta_update_labels(S=S, T=T)
                equality_graph = self.graph.get_equality_graph()

                new_last_node = equality_graph.get_node_by_id(last_node.id)

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

                        new_last_node = equality_graph.get_node_by_id(
                            matching_parent.incoming_edges[0].parent_node.id)

                return find_path(last_node=new_last_node, equality_graph=equality_graph, S=S, T=T)

            # elif 'Projet' in last_node.id:
        return find_path(last_node=base_equality_graph.get_node_by_id(starting_node_id), equality_graph=base_equality_graph, S=[starting_node_id], T=[])

        """
        def find_path(last_node, S, T):
            # Pour les groupes
            if 'Groupe' in last_node.id:
                # On explore les noeuds enfants
                for edge in last_node.outgoing_edges:
                    # A la recherche d'un noeud pas visite
                    if not edge.child_node.id in T:
                        # si le noeud n'est pas sature on s'arrete
                        if not edge.child_node.is_saturated():
                            print(
                                f'{edge.parent_node.id} to {edge.child_node.id} W: {edge.weigh}')
                            last_node = equality_graph.get_node_by_id(
                                edge.child_node.id)
                            T.append(last_node.id)
                            # return f'{edge.parent_node.id} to {edge.child_node.id} W: {edge.weigh}'

                # si on en trouve aucune pas sature
                # sinon on retravaille les poids des noeuds
                # et on refait un nouveau graph d'egalite
                if len([edge for edge in last_node.outgoing_edges if not edge.child_node.is_saturated()]) == 0:
                    self.delta_update_labels(T, S)
                    equality_graph = self.graph.get_equality_graph()
                    return find_path(last_node=last_node, S=S, T=T)

            # Pour les projets
            elif 'Projet' in last_node.id:
                # On explore les noeuds parents
                for edge in last_node.incoming_edges:
                    # A la recherche d'un noeud pas visite
                    if not edge.parent_node.id in S:
                        last_node = equality_graph.get_node_by_id(
                            edge.parent_node.id)
                        S.append(last_node.id)
                        return find_path(last_node=last_node, S=S, T=T)

        return find_path(last_node=equality_graph.get_node_by_id(starting_node_id), S=[starting_node_id], T=[])
        """

    def initalize_labels(self, graph):
        """
        Initialise la valeur de chaque noeud projet
        """
        for edge in graph.starting_node.outgoing_edges:
            # Recherche de la connexion avec le poids le plus haut
            highest_weigh = max(
                [int(edge.weigh) for edge in edge.child_node.outgoing_edges])

            # on met a jour la valeur du noeud comme le plus haut poids
            edge.child_node.label = int(highest_weigh)

    def delta_update_labels(self, S, T):
        """
        Mise a jour des valeurs de chaque noeud avec calcul
        du delta minimum
        """
        print(f'Updating labels using the following\n- S={S}\n- T={T}')
        delta = None

        # On veut calculer le delta minimum
        for node_id in S:

            # Pour chaque noeud dans S
            S_node = self.graph.get_node_by_id(node_id)
            for edge in S_node.outgoing_edges:

                # on veut calculer le delta de chaque connexion vers
                # un noeud pas inclus dans T
                if not(edge.child_node.id in T):

                    # on recherche le delta minimum
                    if not delta or (int(edge.parent_node.label) + int(edge.child_node.label) - int(edge.weigh)) < delta:
                        delta = (int(edge.parent_node.label) +
                                 int(edge.child_node.label) -
                                 int(edge.weigh))

        # Une fois delta trouve on veut update les valeur de chaque noeud
        if delta:
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
