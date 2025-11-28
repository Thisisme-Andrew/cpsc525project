from email_validator import EmailNotValidError, validate_email
from getpass import getpass
import hashlib
from time import sleep

from .page_templates import Page
from .. import state
from ..utils.utils import clear_screen
from ...database.services.users.users_services import add_user, login, change_password

# Password salt
SALT = "CPSC525SecurePasswordSalt123!"


class LoginPage(Page):
    """Login page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import DashboardPage, WelcomePage

        clear_screen()
        print("Please enter your login credentals:\n")

        while True:
            # Get the user's credentials
            email = input("Email: ")
            if not email:
                # Return to the welcome page
                print()
                return WelcomePage()

            # Get and hash the password
            password = getpass("Password: ")
            hashed_pw = hashlib.sha256((password + SALT).encode()).hexdigest()

            if not login(email, hashed_pw):
                # TODO proper error handling between frontend/backend
                print("Invalid credentials! Try again or press Enter to go back.\n")
                continue

            # Success, update global state and redirect to the dashboard
            state.email = email
            print("Success. Redirecting to the dashboard...")
            sleep(1.5)
            return DashboardPage()


class CreateAccountPage(Page):
    """Create account page."""

    def run(self) -> Page:
        """Runs the page.

        :return: The next page for the app to run.
        :rtype: Page
        """
        # Deferred imports to avoid circular dependencies
        from .dashboard import WelcomePage

        clear_screen()
        print("Create an account:\n")

        while True:
            # Get the user's email
            email = input("Email: ")
            if not email:
                # Return to the welcome page
                print()
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
                print("Passwords do not match. Try again or press Enter to go back.\n")
                continue

            # Hash the password
            hashed_pw = hashlib.sha256((password + SALT).encode()).hexdigest()

            if not add_user(email, hashed_pw):
                # TODO error handling between backend/frontend
                print()
                continue

            # Success, require the user to log into their new account
            print()
            print("Please log in to continue. Redirecting...")
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
        from .dashboard import SettingsPage

        clear_screen()
        print(f"Changing password for user: {state.email}\n")

        while True:
            old_pass = getpass("Old password: ")
            if not old_pass:
                # Return to the settings page
                print()
                return SettingsPage

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

            # Hash the passwords
            old_hashed_pw = hashlib.sha256((old_pass + SALT).encode()).hexdigest()
            new_hashed_pw = hashlib.sha256((new_pass + SALT).encode()).hexdigest()

            if not change_password(state.email, old_hashed_pw, new_hashed_pw):
                # TODO error handling between backend/frontend
                print()
                continue

            # Success, return to the settings page
            print()
            print("Password successfully changed. Redirecting...")
            sleep(1.5)
            return SettingsPage()
