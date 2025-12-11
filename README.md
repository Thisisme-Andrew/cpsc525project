# Budget Hacker - CPSC 525 Fall 2025 - Group Project

## CWE Topic

CWE-200: Exposure of Sensitive Information to an Unauthorized Actor

## Group Members

-   Eugene Lee (30137489)
-   Hunter Halvorson (30145930)
-   Braedon Haensel (30144363)
-   Kevin Tran (30146900)
-   Andy Tang (10139121)

## Application Description

Budget Hacker is a text-based finance and budget management application. Each user gets one financial account, which they can use to track their income and expenses. Users can create budgets and allocate funds from their financial account. Funds can be transferred to another user's account, which can be exploited to reveal the other user's account balance.

## How to Run the Application

1. Use [pip](https://pypi.org/project/pip/) to install the required python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Navigate into the source directory:

    ```bash
    cd src
    ```

3. Run the Python application:
    ```
    python app.py
    ```

## Exploit Explanation

Location: [/src/budget_hacker/database/services/finances/accounts.py](/src/budget_hacker/database/services/finances/accounts.py)

Summary: When sending money, an account capacity check on the recipient's account can expose their private account balance to the sender. This occurs if the amount to be sent would exceed the recipient's maximum account capacity.

Explanation: The core issue lies within the send_money() function, which transfers funds between two users. It relies on two private functions: \_add_expense() (to deduct money from the sender) and \_add_income() (to add money to the recipient).

The vulnerability is specifically in \_add_income().

Vulnerability:

1. \_add_income(): This function is used to deposit money into a user's account. It includes a security check to ensure the new balance doesn't exceed a predetermined maximum account balance of $99999999.99.

2. The Flaw: send_money() uses \_add_income(), so if the recipient's account balance plus the incoming amount would exceed $99999999.99, then \_add_income() will raise an exception containing sensitive information.

3. Information Leak: When this exception is raised, it prints an error message "Amount ${amount} plus current balance ${starting_balance} exceeds the maximum allowed account balance of ${MAX_BALANCE}." (line 165).

4. Security Impact: This error message inadvertently displays to the sender the recipient's account balance as the {starting_balance}. This is a major vulnerability, as it allows the sender to view the recipient's account balance, constituting an unauthorized exposure of sensitive information.

## How to Exploit the Application

### Overview

Goal:

-   As the user Bob (bob@gmail.com) we will access another user Alice's (alice@gmail.com) account balance without authorization.

Approach:

-   We will add income to Bob's account to reach the maximum capacity, then we will try to send all of the money to Alice's account.

-   The sent amount would push Alice's account balance over the maximum capacity, so an exception will be raised. The resulting exception message will expose Alice's account balance.

Result:

-   The error message "Error sending money: Amount $99999999.99 plus current balance $12345.00 exceeds the maximum allowed account balance of $99999999.99." will be printed.

-   Alice's account balance will be leaked in this message as "$12345.00".

### Steps to Perform the Exploit:

1. Follow the [How to Run the Application](#How-to-Run-the-Application) section to start application

2. Select "Log In":

    - Choice: <0>

        - Note: Do not include the < or > characters

3. Log in as Bob:

    - Email: <bob@gmail.com>
    - Password: \<password>

4. Select "Add Income":

    - Choice: <0>

5. Enter the maximum account capacity for Bob's income:

    - Amount: $<99999999.99>
    - Description: \<Maximize bob's account for the exploit.>
    - Add more income? (y or n): \<n>

6. Select "Send Money":

    - Choice: <2>

7. Enter the required information to send money to Alice:

    - Recipient email: <alice@gmail.com>
    - Amount to send: $<99999999.99>
    - Description: \<Send money to expose Alice's account balance.>
    - Send $99999999.99 to alice@gmail.com with description: Send money to expose Alice's account balance.? (y or n): \<y>

8. View Alice's exposed account balance:

    - In the error message "Error sending money: Amount $99999999.99 plus current balance $12345.00 exceeds the maximum allowed account balance of $99999999.99." Alice's account balance is revealed as "$12345.00"

## Default Users

| Email           | Password | Starting Balance | Budget Name | Budget Balance | Goal       |
| --------------- | -------- | ---------------- | ----------- | -------------- | ---------- |
| bob@gmail.com   | password | $ 0.00           | New Car     | $ 0.00         | $ 10000.00 |
| alice@gmail.com | password | $ 12345.00       | New Car     | $ 0.00         | $ 10000.00 |
