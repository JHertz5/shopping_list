def input_is_valid_int(input_str, max=0, min=0):

    assert isinstance(input_str, str)
    return_bool = False
    try:
        return_int = int(input_str)
        return_bool = (min <= return_int <= max)
    except ValueError:
        print('Error: grouping selection must be int')
    except AssertionError:
        print('Error: input must be in range [{},{}]'.format(min, max))

    return return_bool
