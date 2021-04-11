def get_weight(index, method='decreasing'):
    if method == 'fibo':
        return fibo(index)
    else:
        return index


def fibo(n):
    if(n <= 2):
        return n
    else:
        return (fibo(n-1) + fibo(n-2))
