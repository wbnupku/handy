def _find_value(data, value, path=[], output=[]):

    if not isinstance(data, (dict, list)):
        if type(data) == type(value):
            if (data == value) or (isinstance(data, str) and value in data):
                # print(path)
                output.append(path[:])
        return
    if isinstance(data, list):
        for i in range(len(data)):
            n_path = path[:]
            n_path.append(i)
            _find_value(data[i], value, n_path, output)
    else:
        for k, v in data.items():
            n_path = path[:]
            n_path.append(k)
            _find_value(data[k], value, n_path, output)
            
            
def find_value(data, value):
    output = []
    path = []
    _find_value(data, value, path, output)
    return ['.'.join(map(str, p)) for p in output]


def get_value(data, path):
    key_chain = path.split('.')
    pointer = data
    for k in key_chain:
        if isinstance(pointer, list):
            pointer = pointer[int(k)]
        elif isinstance(pointer, dict):
            pointer = pointer[k]
        else:
            raise Exception('Not found')
    return pointer

def get_values(data, paths):
    return [get_value(data, p) for p in paths]

def test_find_value():

    d = {'a': [1, 2, '1234'], 'b': {'haha': ['c', '1234']}}
    find_value(d, '1234')
    
if __name__ == '__main__':
    test_find_value()
