class InvalidCertificatePath(Exception):
    """Raised when trying to create a file bound certificate object and
    pfx file was not found or invalid"""

    def __init__(self) -> None:
        super().__init__(
            "Invalid certificate. Make sure you are passing a valid pfx file path."
        )


class InvalidCertificatePassword(Exception):
    """Raised when trying to create a file bound certificate object and
    the password is invalid"""

    def __init__(self) -> None:
        super().__init__("Invalid password. Try again with the correct password.")


class InvalidStoreLocation(Exception):
    """Raised when trying to install certificate with invalid value to
    store_location parameter"""

    def __init__(self) -> None:
        super().__init__(
            "Invalid value for store_location. The value must be the string 'user' or 'machine'."
        )
