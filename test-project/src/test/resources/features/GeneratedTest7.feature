Feature: User Registration and Login for E-Commerce Platform
  As a new customer
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
    Then the system sends a verification email to the provided address
    And the user receives an email with a verification link

  Scenario: User registers with invalid credentials (email)
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@exmaple.com |
      | Password     | P@ssw0rd123      |
    Then the system shows an error message "Invalid email format"

  Scenario: User registers with invalid credentials (password)
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | pass123          |
    Then the system shows an error message "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"

  Scenario Outline: User logs in with different credentials
    When the user logs in with "<email>" and "<password>"
    Then the result is "<result>"

    Examples:
      | email            | password    | result  |
      | john@example.com | P@ssw0rd123 | success |
      | wrong@test.com   | wrongpass   | failure |

  Scenario: User logs in with invalid credentials
    When the user logs in with "wrong@example.com" and "wrongpassword"
    Then the system shows an error message "Invalid email or password"

  Scenario Outline: User requests password reset via email
    Given the user is registered
    When the user requests a password reset for "<email>"
    Then the system sends a password reset link to the provided address

    Examples:
      | email            |
      | john@example.com |

  Scenario: User session persists for 24 hours or until logout
    Given the user logs in with "john@example.com" and "P@ssw0rd123"
    When the user does not log out
    Then the system maintains the user's session for at least 24 hours

  Scenario: User session is terminated after multiple failed login attempts
    Given the user has attempted to log in with "wrong@example.com" and "wrongpassword" five times
    When the user tries to log in again
    Then the system locks the account for 15 minutes