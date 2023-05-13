class ParseStatusException(Exception):
    """Post is not find."""

    pass


class PostException(Exception):
    """An error occurred while publishing post."""

    pass


class TextConvertException(Exception):
    """An error occurred while converting text.."""

    pass


class PostGettingException(Exception):
    """An error occurred while receiving post."""

    pass
