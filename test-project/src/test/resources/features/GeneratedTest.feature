Feature: User Registration and Login for E-Commerce Platform
  As a new customer,
  I want to register an account and login to the e-commerce platform
  So that I can save my shopping preferences and track my orders

  Background:
    Given the email service is configured
    And the database schema for user management is set up
    And the SSL certificate is installed
    And OAuth 2.0 authentication is enabled
    And JWT tokens are used for session management
    And password encryption using bcrypt is implemented
    And rate limiting on login attempts is enforced (max 5 attempts per 15 minutes)
    And HTTPS is required for all authentication endpoints

  Scenario: User registers with valid credentials
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | P@ssw0rd123      |
    Then the system validates the email format and uniqueness
    And the system generates a verification token for the user's email
    And the system sends a verification email to the user

  Scenario: User registers with invalid credentials (duplicate email)
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | P@ssw0rd123      |
    Then the system rejects the registration due to duplicate email

  Scenario Outline: User logs in with valid credentials
    When the user logs in with "<email>" and "<password>"
    Then the result is "success"
    Examples:
      | email            | password    |
      | john@example.com | P@ssw0rd123 |

  Scenario Outline: User logs in with invalid credentials (wrong password)
    When the user logs in with "<email>" and "<password>"
    Then the result is "failure" and appropriate error message is displayed
    Examples:
      | email            | password    |
      | john@example.com | wrongpass   |

  Scenario: User requests password reset via email
    Given the user has registered and verified their account
    When the user clicks on "Forgot Password"
    And the user enters "<email>"
    Then the system sends a password reset link to the user's email

  Scenario Outline: User attempts login with too many failed attempts
    When the user logs in with "<email>" and "<password>"
    Then the result is "failure" and account is locked for 15 minutes
    Examples:
      | email            | password    |
      | john@example.com | wrongpass   |

  Scenario: User session persists for 24 hours or until logout
    Given the user has logged in successfully
    When the user does not log out within 24 hours
    Then the system maintains the user's session

  Scenario Outline: User registers with a password that is too weak
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | pass123          |
    Then the system rejects the registration due to weak password
    Examples:
      | email            | password    |
      | john@example.com | pass123     |

  Scenario: User registers with a password that is same as last 3 passwords
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | P@ssw0rd123      |
    And the user attempts to change password to "P@ssw0rd123"
    Then the system rejects the password change due to reuse of last 3 passwords