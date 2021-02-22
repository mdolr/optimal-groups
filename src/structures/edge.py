class Edge:
    """
    Represente une connexion entre 2 nodes sur le graph
    """

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)

        self.graph = kwargs.pop('graph', None)

        self.weigh = kwargs.pop('weigh', 0)

        #self.current_capacity = kwargs.pop('current_capacity', 0)
        #self.limit_capacity = kwargs.pop('limit_capacity', 0)

        self.parent_node = kwargs.pop('parent_node', None)
        self.child_node = kwargs.pop('child_node', None)
