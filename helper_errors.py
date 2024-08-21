class MissingUserDataError(Exception):
    """ """

    def __init__(self):
        msg = "No user data associated with this context!?!"
        super().__init__(msg)


class MissingMessageDataError(Exception):
    """ """

    def __init__(self):
        msg = "No message associated with this update!?!"
        super().__init__(msg)


class MissingMessageFromUserError(Exception):
    """ """

    def __init__(self):
        msg = "No from user was associated with this update!?!"
        super().__init__(msg)
