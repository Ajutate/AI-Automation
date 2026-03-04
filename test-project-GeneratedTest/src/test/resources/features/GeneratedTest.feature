Feature: User Registration and Login for E-Commerce Platform
  As a new customer,
  I want to register an account and login to the e-commerce platform
  So that I can save my shopping preferences and track my orders

  Background:
    Given the email service is configured
    And the database schema for user management is set up
    And OAuth 2.0 and JWT tokens are implemented
    And HTTPS is enabled for all authentication endpoints
    And rate limiting on login attempts is in place (max 5 attempts per 15 minutes)

  Scenario: User registers with valid credentials
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | P@ssw0rd123      |
    Then the system validates the email format and uniqueness
    And the system generates a verification token for the user's email
    And the system sends an email to the user with the verification link

  Scenario: User logs in with verified credentials
    When the user logs in with "john@example.com" and "P@ssw0rd123"
    Then the result is "success"

  Scenario Outline: Login with different credentials
    When the user logs in with "<email>" and "<password>"
    Then the result is "<result>"

    Examples:
      | email            | password    | result  |
      | john@example.com | P@ssw0rd123 | success |
      | wrong@test.com   | wrongpass   | failure |

  Scenario: User logs in with invalid credentials
    When the user logs in with "invalid@example.com" and "wrongpassword"
    Then the result is "failure"

  Scenario Outline: Password reset request
    Given the user has registered with "<email>"
    When the user requests a password reset via email
    Then an email with a reset link is sent to "<email>"

    Examples:
      | email            |
      | john@example.com |

  Scenario: User session persists for 24 hours or until logout
    Given the user logs in with "john@example.com" and "P@ssw0rd123"
    When the user does not log out within 24 hours
    Then the system recognizes the user as logged in

  Scenario Outline: User registration with invalid email format
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | johnexample.com  |
      | Password     | P@ssw0rd123      |
    Then the system shows an error message "Invalid email format"

  Scenario: User session is locked after multiple failed login attempts
    Given the user has registered with "john@example.com"
    When the user logs in with "john@example.com" and "wrongpassword" five times within 15 minutes
    Then the account is locked for 15 minutes

  Scenario Outline: Password cannot be same as last 3 passwords
    Given the user has registered with "<email>" and password "<password1>"
    And the user changes their password to "<password2>"
    When the user tries to change their password back to "<password1>"
    Then the system shows an error message "Password cannot be same as last 3 passwords"

    Examples:
      | email            | password1       | password2        |
      | john@example.com | P@ssw0rd123     | P@ssw0rd456      |