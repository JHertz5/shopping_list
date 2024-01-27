import sys


def string_is_valid_int(input_str, max=0, min=0):
    '''
    Determine whether a string is can be converted to an int. Optional arguments to define the maximum and minimum valid
    values for the int.
    '''

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


def quit(exit_status=0):
    '''
    Gracefully exit the program.
    '''
    print('exiting')
    sys.exit(exit_status)
