"""Global user state that persists between pages."""

# Email of the currently logged-in user
email = None


def clear():
    """Clears the user state."""
    global email
    email = None
