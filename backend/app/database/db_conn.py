class DBConnection:
    def __init__(self):
        pass

    def connect(self) -> bool | None:
        raise NotImplementedError("Not implement")

    def ping(self) -> bool | None:
        raise NotImplementedError("Not implement")

    def disconnect(self) -> bool | None:
        raise NotImplementedError("Not implement")
