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

1. Use [pip](https://pypi.org/project/pip/) to install the required python packages

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

Location: CPSC525PROJECT/src/budget_hacker/database/services/finances/accounts.py

TLDR; An account capacity check intended for the recipient's security leaks the recipient's private balance information to the sender when a transfer fails.

Explanation:
The core issue lies within the send_money() function, which transfers funds between two users. It relies on two private functions _add_expense() (to deduct money from the sender) and _add_income() (adds money to the recipient).

The vulnerability is specifically in _add_income().

Vulnerability

    1. _add_income(): Is used for a user to deposit money into their own account. It includes a security check to ensure the new balance doesn't exceed a predetermined maximum account balance ($99999999.99).

    2. The Flaw: send_money() uses _add_income() so if the recipient's account balance plus the incoming amount would exceed 99999999.99 _add_income() will raise an exception with sensitive information.

    3. Information Leak: When this exception is raised, it prints an error message "Amount ${amount} plus current balance ${starting_balance} exceeds the maximum allowed account balance of $99999999.99." (line 156).

    4. Security Impact: This error message inadvertently displays to the sender the recipient's account balance as the{starting_balance}

## How to Exploit the Application

Goal: As the user Bob (bob@gmail.com) we will access another user Alice's (alice@gmail.com) account balance unauthorized

Approach: 
    - Add income to Bob's account to maximize his account to capacity and send all the money to Alice's account
    - This will raise an exception that this amouont goes beyond the account capacity

Result: 
    - prints erorr: "Error sending money: Amount $99999999.99 plus current balance $12345.00 exceeds the maximum allowed account balance of $99999999.99."
    Alice's account balance is leaked as $12345.00 from the error message

** <x> = enter x in command line without <>

1. Follow "How to Run the Application" section to start app

2. Select [0] to login in the welcoming page
    - Choice: <0>

3. Login as [bob]
    - Email: <bob@gmail.com>
    - Password: <password>

4. Select [0] to Add Income
    - Choice: <0>

5. Enter max account capacity as income
    - Amount: $<99999999.99>
    - Description: <the exploit>
    - Add more income? (y or n): <n>

6. Send money to Alice
    - Choice: <2>

7. Enter information to send money to Alice
    - Recipient email: <alice@gmail.com>
    - Amount to send: $<99999999.99>
    - Description: <Expose alice's balance>
    - Send $99999999.99 to alice@gmail.com with description: Expose alice's balance? (y or n): <y>

8. Check exploit was successful
    - Success if prints: "Error sending money: Amount $99999999.99 plus current balance $12345.00 exceeds the maximum allowed account balance of $99999999.99."


## Default Users

|      Email      | Password | Starting Balance | Budget Name | Budget Balance |    Goal    |
| --------------- + -------- + ---------------- + ----------- + -------------- + ---------- |
|   bob@gmail.com | password | $           0.00 |     New Car | $         0.00 | $ 10000.00 |
| alice@gmail.com | password | $       12345.00 |     New Car | $         0.00 | $ 10000.00 |
