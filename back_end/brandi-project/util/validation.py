def validation(data, lst, func_name):
    index = 0
    for key in data:
        if key not in lst:
            raise KeyError(f"invalid key '{key}' in '{func_name}'")
        index += 1

    if index != len(lst):
        raise KeyError(f"required key '{key}' in '{func_name}'")


class KeywordValidation:
    def signin(self, data):
        lst = [
            'account',
            'password'
        ]
        validation(data, lst, 'signin')
