class UserNotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TNoMoreAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TNoBeforeAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UNoMoreAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UNoBeforeAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NoBeforeAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        # <3
class NoMoreAccesses(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TrackingError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)