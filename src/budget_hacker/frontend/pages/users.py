from email_validator import EmailNotValidError, validate_email
from getpass import getpass
from time import sleep

from .page_templates import Page
from .. import state
from ..utils.utils import clear_screen
from ...database.services.users.users import (
    create_user,
    login,
    change_password,
    remove_user,
)


class LoginPage(Page):
    """Login page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import MainDashboardPage, WelcomePage

        clear_screen()
        print("--Log In--\n")

        while True:
            print("Please enter your login credentials or press Enter to go back:\n")

            # Get the user's credentials
            email = input("Email: ")
            if not email:
                return WelcomePage()

            # Get and hash the password
            password = getpass("Password: ")
            if not password:
                return WelcomePage()

            db_response = login(email, password)
            if not db_response["success"]:
                print(db_response["error"] + "\n")
                continue

            # Success, update global state and redirect to the dashboard
            state.email = email
            print("\nSuccess. Redirecting to the Budget Hacker Dashboard...")
            sleep(1)
            return MainDashboardPage()


class LogoutPage(Page):
    """Logout page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import WelcomePage

        print("Logging out...")
        state.clear()
        sleep(1)
        return WelcomePage()


class CreateUserPage(Page):
    """Create user page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import WelcomePage

        clear_screen()
        print("--Create User Account--\n")

        while True:
            print("Create an account or press Enter to go back:\n")

            # Get the user's email
            email = input("Email: ")
            if not email:
                return WelcomePage()

            try:
                validate_email(email)
            except EmailNotValidError:
                print("Invalid email format. Please try again.\n")
                continue

            # Get the user's password
            password = getpass("Password: ")
            if len(password) < 8:
                print("Password must be at least 8 characters. Please try again.\n")
                continue
            if " " in password:
                print("Password must not contain spaces. Please try again.\n")
                continue

            confirm_password = getpass("Confirm password: ")

            # Confirm the passwords match
            if password != confirm_password:
                print("Passwords do not match. Please try again.\n")
                continue

            db_response = create_user(email, password)
            if not db_response["success"]:
                print(db_response["error"] + "\n")
                continue

            # Success, require the user to log into their login info
            print()
            print("Please log in to continue. Redirecting to the Log In page...")
            sleep(1.5)
            return LoginPage()


class ChangePasswordPage(Page):
    """Change password page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import SettingsPage

        clear_screen()
        print("--Change Password--\n")

        print(f"Changing password for user: {state.email}\n")

        while True:
            old_pass = getpass("Old password: ")
            if not old_pass:
                return SettingsPage()

            # Get the user's new password
            new_pass = getpass("New password: ")
            if len(new_pass) < 8:
                print("Password must be at least 8 characters. Please try again.\n")
                continue
            if " " in new_pass:
                print("Password must not contain spaces. Please try again.\n")
                continue

            confirm_new_pass = getpass("Confirm new password: ")

            # Confirm the passwords match
            if new_pass != confirm_new_pass:
                print("Passwords do not match. Try again or press Enter to go back.\n")
                continue

            db_response = change_password(state.email, old_pass, new_pass)
            if not db_response["success"]:
                print(db_response["error"] + "\n")
                continue

            # Success, return to the previous page
            print()
            print("Password changed successfully. Returning to the previous page...")
            sleep(1.5)
            return SettingsPage()


class DeleteUserPage(Page):
    """Delete user page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .main_dashboard import SettingsPage, WelcomePage

        clear_screen()
        print("--Delete User Account--\n")

        print(f"Deleting user: {state.email}\n")

        while True:
            confirm = input("Confirm your email: ")
            if not confirm:
                # Return to the settings page
                print()
                return SettingsPage()
            if confirm != state.email:
                print("Incorrect email. Please try again.\n")
                continue

            confirm = input("Are you sure you want to delete your account? (y or n): ")
            if not confirm.lower() in ["y", "yes"]:
                # Return to the settings page
                print("Aborting...")
                sleep(1)
                return SettingsPage()

            db_response = remove_user(state.email)
            # Perform the user deletion
            if not db_response["success"]:
                print(db_response["error"] + "\n")
                continue

            # Success, clear state and return to the welcome page
            state.clear()
            print()
            print("Account deleted. Redirecting to the Welcome page")
            sleep(1.5)
            return WelcomePage()
