class Node:
    """
    Represente un point dans le graph
    """

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)

        self.graph = kwargs.pop('graph', None)

        self.edges = kwargs.pop('edges', [])
        
        self.current_capacity = kwargs.pop('current_capacity', 0)
        self.limit_capacity = kwargs.pop('limit_capacity', 0)
