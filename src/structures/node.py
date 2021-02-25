class Node:
    """
    Represente un point dans le graph
    """

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)

        self.graph = kwargs.pop('graph', None)

        self.outgoing_edges = kwargs.pop('outgoing_edges', [])
        self.incoming_edges = kwargs.pop('incoming_edges', [])

        self.label = kwargs.pop('label', 0)

        self.current_capacity = kwargs.pop('current_capacity', 0)
        self.limit_capacity = kwargs.pop('limit_capacity', 0)

    def is_saturated(self):
        """
        Retourne un booleen derivant si le noeud est sature
        c'est a dire si le noeud a incoming_edges >= limit_capacity
        """
        return len(self.incoming_edges) >= self.limit_capacity
