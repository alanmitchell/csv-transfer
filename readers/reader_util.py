"""Utility functions useful for reading CSV files.
"""

def apply_field_map(field_map, names):
    """Returns an altered a list of field names, 'names'
    according to a 'field_map'.

    Parameters
    ----------
    field_map: This can be a dictionary or a string; if it is neither, the
        field names are not modified.  If it is a dictionary, any field name
        that appears as a key in the dictionary is replaced with the corresponding
        dictionary value.  Not all field names need to appear in the dictionary.
        If 'field_map' is a string, it is assumed to be a lambda function with one
        parameter.  That lambda function is applied to all the field names.
    names: A list of field names to alter.

    Returns
    -------
    Returns the altered list of field names.  Raises an error if application of
    the lambda function causes an error.
    """

    new_names = names[:]   # make a copy of names

    if isinstance(field_map, dict):
        # field map is a dictionary, mapping some/all old names to
        # new names
        new_names = [field_map.get(fld, fld) for fld in names]
    elif isinstance(field_map, str):
        # field map is a string, presumed to be a lambda function for
        # converting field names
        try:
            conv_func = eval(field_map)
            new_names = [conv_func(nm) for nm in names]
        except:
            raise ValueError('The field_map function "%s" is not valid.' % field_map)

    return new_names
