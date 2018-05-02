
class {{ class_name }}Error(Exception):
    """Generic errors."""

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg

    def __repr__(self):
        return "<{{ class_name }}Error - %s>" % self.msg
