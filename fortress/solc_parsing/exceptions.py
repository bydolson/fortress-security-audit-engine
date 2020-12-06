from fortress.exceptions import FortressException


class ParsingError(FortressException):
    pass


class VariableNotFound(FortressException):
    pass
