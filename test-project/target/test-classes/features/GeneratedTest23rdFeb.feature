Feature: User Registration and Login for E-Commerce Platform
  As a new customer,
  I want to register an account and login to the e-commerce platform
  So that I can save my shopping preferences and track my orders

  Background:
    Given the email service is configured
    And the database schema for user management is set up
    And the SSL certificate is installed

  Scenario: User registers with valid credentials
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | P@ssw0rd123      |
    Then the system sends a verification email to "john@example.com"
    And the user receives an email with a verification link
    When the user clicks on the verification link
    Then the account is marked as verified

  Scenario Outline: User logs in with valid credentials
    Given the user has registered and verified their account
    When the user logs in with "<email>" and "<password>"
    Then the result is "success"
    
    Examples:
      | email            | password    |
      | john@example.com | P@ssw0rd123 |

  Scenario Outline: User logs in with invalid credentials
    Given the user has registered but not verified their account
    When the user logs in with "<email>" and "<password>"
    Then the result is "failure"
    
    Examples:
      | email            | password    |
      | john@example.com | wrongpass   |

  Scenario: User attempts to login after failed attempts lockout
    Given the user has registered and verified their account
    When the user logs in with "<email>" and "<password>"
    Then the result is "failure"
    And the system locks the account for 15 minutes
    
    Examples:
      | email            | password    |
      | john@example.com | wrongpass   |

  Scenario: User requests password reset via email
    Given the user has registered but not verified their account
    When the user clicks on "Forgot Password" link
    Then a password reset email is sent to "john@example.com"
    And the user receives an email with a reset link

  Scenario Outline: User logs in with remembered session
    Given the user has registered and verified their account
    When the user checks the "Remember Me" checkbox during login
    And the user closes the browser or navigates away
    Then the system maintains the user's session for 24 hours
    
    Examples:
      | email            | password    |
      | john@example.com | P@ssw0rd123 |

  Scenario: User logs in with invalid email format
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | invalidemail     |
      | Password     | P@ssw0rd123      |
    Then the system shows an error message "Invalid email format"
    And the account is not created

  Scenario: User logs in with weak password
    When the user fills in the registration form
      | First Name   | John             |
      | Last Name    | Doe              |
      | Email        | john@example.com |
      | Password     | pass123          |
    Then the system shows an error message "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"
    And the account is not created