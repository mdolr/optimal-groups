class Node:
    """
    Represente un point dans le graph
    """

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.name = kwargs.pop('name', None)

        self.position = kwargs.pop('position', None)

        self.children = kwargs.pop('children', [])
