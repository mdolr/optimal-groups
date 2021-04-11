def get_weight(index, method='decreasing'):
    if method == 'fibonacci':
        return fibo(index)
    else:
        return index


def get_max_weight(group_file_path, method='decreasing'):
    # avoid circular reference
    from src.common.data import load_data

    group_rows, groups_data = load_data(group_file_path)

    # group_rows != array
    for row in group_rows:
        if method == 'fibonacci':
            return fibo(len(row) - 1)
        else:
            return len(row) - 1


def fibo(n):
    if(n <= 2):
        return n
    else:
        return (fibo(n-1) + fibo(n-2))
