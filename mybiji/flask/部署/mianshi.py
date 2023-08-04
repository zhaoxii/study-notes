versions = [1, 2, 3, 4, 5]

def isBadVersion(version):
    pass
from  collections import deque

def deque_push(deque,num):
    deque.appendleft(num)
    return deque

def deque_pop(deque):
    deque.pop()
    return deque

def get_deque_top(deque):
    d=deque.copy()
    top=d.pop()
    return top

def get_max(deque):
    max_val=max(deque)

    return max_val

if __name__ == '__main__':
    dl=deque(versions)
    print(dl)
    dl=deque_push(dl,11)
    print(dl)
    dl=deque_pop(dl)
    print(dl)
    top=get_deque_top(dl)
    print(top)
    print(dl)
    max_val=get_max(dl)
    print(max_val)
    print(dl)
