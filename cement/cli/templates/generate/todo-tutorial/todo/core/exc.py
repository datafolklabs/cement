
class TodoError(Exception):
    """Generic errors."""

    def __init__(self, msg: str) -> None:
        Exception.__init__(self, msg)
        self.msg = msg

    def __str__(self) -> str:
        return self.msg

    def __repr__(self) -> str:
        return f"<TodoError - {self.msg}>"
