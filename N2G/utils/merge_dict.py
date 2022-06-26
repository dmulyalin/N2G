from copy import deepcopy


def merge_dict(a: dict, b: dict, use_deepcopy: bool = False) -> dict:
    """
    Helper function to recursively merge two dictionaries. This function only
    merges lists and dictionaries, if "a" dictionary value is not a dictionary or
    a list, then this value left unchanged, even if same key exists in dictionary "b"


    :param a: first dictionary to merge
    :param b: second dictionary to merge
    :param use_deepcopy: if True merges deepcopies of a and b dictionaries
    """
    result = deepcopy(a) if use_deepcopy else a
    for bk, bv in b.items():
        av = result.get(bk)
        if isinstance(av, dict) and isinstance(bv, dict):
            result[bk] = merge_dict(av, bv)
        elif isinstance(av, list) and isinstance(bv, list):
            result[bk] = deepcopy(av) + deepcopy(bv) if use_deepcopy else av + bv
        elif isinstance(av, list) and isinstance(bv, dict):
            result[bk] = deepcopy(av) if use_deepcopy else av
            result[bk].append(deepcopy(bv) if use_deepcopy else bv)
        elif isinstance(av, dict) and isinstance(bv, list):
            result[bk] = deepcopy(bv) if use_deepcopy else bv
            result[bk].append(deepcopy(av) if use_deepcopy else av)
        elif bk not in result:
            result[bk] = deepcopy(bv) if use_deepcopy else bv
    return result
