def isNumber(string: str):
    numberable: bool = False
    try:
        int(string)
        numberable = True
    except ValueError:
        pass
    try:
        float(string)
        numberable = True
    except ValueError:
        pass
    try:
        complex(string)
    except ValueError:
        pass

    return numberable


def isWhiteSpace(string: str):
    return string.isspace() or len(string) == 0
