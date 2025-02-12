class NoTableOfContentFound(Exception):
    def __init__(self, message="No Table of Contents found in the document"):
        super().__init__(message)


class NoReferenceMarkFound(Exception):
    def __init__(self, message="Could not find any bibliography references"):
        super().__init__(message)
