import sys
import getopt
import json
from src.common.data import create_graph
from src.implementations.hungarian import Hungarian

# Options par defaut
DEFAULT_OPTIONS = {
    # chemin vers le fichier d'entree contenant
    # la liste des groupes et les preferences
    'g': './test_groups.csv',

    # chemin vers le fichier d'entree contenant
    # la liste des projets et leur capacite
    'p': './test_projects.csv',

    # chemin vers le fichier de sortie contenant
    # les resultats
    'o': './outputs.txt',

    # implementation a utiliser
    'i': 'hungarian',

    'debug': False
}

options = {}

# si le programme est lance
# depuis la ligne de commande
# a l'aide de python main.py
if __name__ == '__main__':
    # on commence par recuperer les arguments
    # -g <chemin_fichier_entree>
    # -p <chemin_fichier_entree>
    # -o <chemin_fichier_sortie>
    # -i <algorithme>

    try:
        # on enleve le nom du fichier des args
        opts, args = getopt.getopt(
            sys.argv[1:], 'g:p:o:i:', longopts=['debug'])

    # au cas ou des options avec arguments manquent d'un argument
    # on redonne la syntaxe de la commande
    except getopt.GetoptError:
        print('Correct syntax: main.py -g <groups_data_file> -p <projects_data_file> -o <outputs_file> -i <algorithm>')
        sys.exit(2)

    for opt, arg in opts:
        # on veut traiter les arguments sans le -
        opt = opt.replace('--', '').replace('-', '')
        options[opt] = arg

        if opt == 'debug':
            options['debug'] = True

    # on remplace les valeurs par defauts pour les arguments precises
    DEFAULT_OPTIONS.update(options)

    graph = create_graph(DEFAULT_OPTIONS['g'], DEFAULT_OPTIONS['p'])

    algorithm = Hungarian(graph=graph, debug=DEFAULT_OPTIONS['debug'])
    matching = algorithm.solve()

    # if DEFAULT_OPTIONS['debug']:
    print(json.dumps(matching['outputs'],  indent=4))
    matching['graph'].draw(bipartite=False, title='Graph final')

    # lancer la recuperation des donnees
    # creer le graph
    # une fois le graph creer traiter le graph avec l'algo
    # une fois le graph traite retranscrire les resultats dans un fichier
