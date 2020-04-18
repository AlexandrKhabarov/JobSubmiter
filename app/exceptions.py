class UnrecognizedMode(Exception):
    MSG = "Passed unrecognized mode: {}. Available: DEVELOPMENT, PRODUCTION, TEST"

    def __init__(self, mode):
        msg = self.MSG.format(mode)
        super().__init__(msg)
