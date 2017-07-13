class CannotReadSpectraError(RuntimeError):
    """Exception to be used by plugins to indicate that a spectra could not be
    read, even though it should be a valid index.
    """
    pass
