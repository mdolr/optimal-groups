from src.common.data import load_data


def get_weight(index, method='decreasing'):
    if method == 'fibonacci':
        return fibo(index)
    else:
        return index


def get_max_weight(group_path, method='decreasing'):
    group_rows, groups_data = load_data(group_path)
    return fibo(len(group_rows[0]) - 1) if method == 'fibonacci' else len(group_rows[0]) - 1


def fibo(n):
    if(n <= 2):
        return n
    else:
        return (fibo(n-1) + fibo(n-2))
