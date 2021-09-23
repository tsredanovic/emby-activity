class InvalidActivityError(Exception):
    """Exception raised when activity is not supported.

    Attributes:
        activity -- unsupported activity
    """

    def __init__(self, activity):
        self.activity = activity
        self.message = 'Unsupported activity'
        super().__init__(self.message)

    def __str__(self):
        return '{} -> {}'.format(self.activity, self.message)
