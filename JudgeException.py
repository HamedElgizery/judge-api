class JudgeException(Exception):
    pass


class CompilationError(JudgeException):
    pass


class RuntimeError(JudgeException):
    pass


class TLE(JudgeException):
    pass


class MLE(JudgeException):
    pass
