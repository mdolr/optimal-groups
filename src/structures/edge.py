class Edge:
    """
    Represente une connexion entre 2 nodes sur le graph
    """

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.name = kwargs.get('name', None)

        self.position = kwargs.pop('position', None)

        self.current_capacity = kwargs.pop('current_capacity', 0)
        self.limit_capacity = kwargs.pop('limit_capacity', 0)

        self.parent = kwargs.pop('parent', None)
        self.child = kwargs.pop('child', None)
