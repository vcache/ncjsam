def flatten_list(input):
    return [i for nested in flatten_list for i in nested]
