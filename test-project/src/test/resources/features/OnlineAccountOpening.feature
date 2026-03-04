Feature: Online Account Opening (Retail Banking)

  Background:
    Given a customer named John who is 20 years old
    And the bank's KYC service is available
    And the core banking system is operational

  Scenario: Valid account opening process
    When John starts the account opening process via the web channel
    Then he provides his personal detai
    ls (name, DOB, address, phone, email)
    And he uploads his ID proof and address proof
    When the KYC verification is successful
    Then he selects a savings account type and submits the application
    And the system creates the account in the core banking system
    And John receives an account number
    And John receives a confirmation email and SMS

  Scenario: Invalid KYC due to OTP mismatch
    Given John has started the account opening process via the web channel
    When he provides his personal details (name, DOB, address, phone, email)
    And he uploads his ID proof and address proof
    And the OTP for his phone number is sent but not verified correctly
    Then an error message is shown asking to verify the OTP again
    And upon re-entering a correct OTP, the KYC verification fails
    And John's application is rejected

  Scenario: Failed KYC on second attempt
    Given John has started the account opening process via the web channel
    When he provides his personal details (name, DOB, address, phone, email)
    And he uploads his ID proof and address proof
    And the OTP for his phone number is sent but not verified correctly
    Then an error message is shown asking to verify the OTP again
    And upon re-entering a correct OTP, the KYC verification fails
    And John's application is rejected due to failed second attempt

  Scenario: Duplicate application for same ID
    Given a customer with ID already exists in the system
    When another customer attempts to open an account using the same ID
    Then an error message is shown indicating that the ID is already in use
    And the application process is terminated

  Scenario: KYC service timeout during verification
    Given John has started the account opening process via the web channel
    When he provides his personal details (name, DOB, address, phone, email)
    And he uploads his ID proof and address proof
    When the KYC service times out during verification
    Then an error message is shown indicating that the KYC service has timed out
    And John's application process is terminated

  Scenario: Missing personal detail - Email (Invalid account opening process)
    Given a customer named Sarah who is 21 years old and does not provide her email
    When she starts the account opening process via the web channel
    Then an error message is shown asking to provide an email address
    And Sarah's application is rejected