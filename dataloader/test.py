def reverse_list(input_list):
    """
    Reverse the elements in a given list.

    Parameters:
    input_list (list): The list to be reversed.

    Returns:
    list: A new list containing the elements of the input list in reverse order.

    Example:
    >>> reverse_list([1, 2, 3, 4, 5])
    [5, 4, 3, 2, 1]
    """

    # Use Python's built-in `reversed()` function to obtain an iterator over the reversed input list.
    # Then, convert the iterator to a list using the `list()` constructor and return it.
    return list(reversed(input_list))
