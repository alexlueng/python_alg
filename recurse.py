

import os


def factorial(n):
    if n == 0:
        return 1
    else:
        return factorial(n-1) * n

def binary_search(data, target, low, high):
    """
        Return true if target is found in indicated portion of a Python list
        The search only considers the portion from data[low] to data[high] inclusive
    """
    
    if low > high:
        return False
    else:
        mid = (low + high) // 2
        print(data[mid])
        if target == data[mid]:
            return True
        elif target < data[mid]:
            return binary_search(data, target, low, mid-1)
        else:
            return binary_search(data, target, mid+1, high)

def disk_usage(path):
    """ Return the number of bytes used by a file/folder and any descendents """
    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            childpath = os.path.join(path, filename)
            total += disk_usage(childpath)
    
    print('{0:<7}'.format(total), path)
    return total


def linear_sum(S, n):
    """ Return the sum of the first n numbers of sequence S. """
    if n == 0:
        return 0
    else:
        return linear_sum(S, n-1) + S[n-1]


def reverse(S, start, stop):
    """ Reverse elements in implicit slice[start:stop] """
    if start < stop-1:
        S[start], S[stop-1] = S[stop-1], S[start]
        print(S)
        reverse(S, start+1, stop-1)

def power(x, n):
    if n == 0:
        return 1
    return x * power(x, n-1)

# R4-1 递归查找序列 S 的最大值
def recurse_max(S, n):
    if n == 1:
        return S[0]
    m = recurse_max(S, n-1)
    if m > S[n-1]:
        return m
    else:
        return S[n-1]

# R4-10 只使用加法和整数除法，求n以2为底的对数的整数部分
def log2(n):
    if n < 2:
        return 0
    return 1 + log2(n / 2)

if __name__ == '__main__':
    # print(factorial(5))

    # data = [2,4,5,7,8,9,12,14,17,19,22,25,27,28,33,37]
    # result = binary_search(data, 23, 0, len(data)-1)
    # print(result)

    # disk_usage('D:\courses')
    # print(reverse(data, 0, len(data)))

    # s = [1,5,4, 10,7,8,2]
    # m = recurse_max(s, 6)
    m = log2(1024)
    print(m)
    