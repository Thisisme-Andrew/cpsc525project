# Global user state that persists between pages

email = None


def clear():
    """Clears the user state."""
    global email
    email = None
