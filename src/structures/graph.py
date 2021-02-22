class Graph:
    """
    Represente un graph contenant des nodes et des edges
    """

    def __init__(self, **kwargs):
        self.starting_node = kwargs.pop('starting_node', None)
        self.ending_node = kwargs.pop('ending_node', None)

        self.nodes = kwargs.pop('nodes', [])
        self.edges = kwargs.pop('edges', [])

    def add_node(self, node):
        """
        Rajoute une node
        """

    def remove_node(self, node):
        """
        Supprime une node et ses edges du reseau
        """

    def get_node_by_id(self, node):
        """
        Renvoi une node par rapport a son id
        """
