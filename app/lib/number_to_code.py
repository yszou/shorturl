# -*- coding: utf-8 -*-
 
CODE_MAP = [
    'a', 'b', 'c', 'd', 'e', 'f', 'h',
    'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o',
    'p', 'q', 'r', 's', 't', 'u',
    'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'H',
    'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O',
    'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z',
    '0', 
    '1', '2', '3', '4', '5', '6',
    '7', '8', '9',
]

def number_to_code(n):
    'convert a number to a string code as short as possible'

    if n <= 0:
        raise Exception('n must be greater than zero')

    size = len(CODE_MAP)
    result = []
    while True:
        result.append(CODE_MAP[n % size])
        if n < size:
            break
        n = n // size

    result.reverse()
    return ''.join(result)




if __name__ == '__main__':
    print(number_to_code(918359))

