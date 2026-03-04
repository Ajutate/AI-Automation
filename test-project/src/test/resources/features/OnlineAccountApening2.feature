Feature: Online Account Opening (Retail Banking)

    Background:
        Given a customer is on the bank's web portal
        And the customer has access to internet and required documents

    Scenario: Successful Account Opening by New-to-Bank Customer
        Given the customer provides valid personal details (name, DOB, address, phone, email)
        When the customer uploads ID proof and address proof
        Then the system performs KYC verification
        And if KYC is successful, the system prompts the customer to select account type
        When the customer selects a savings account type and submits application
        Then the system creates an account in core banking
        And the system displays the account number
        And the customer receives a confirmation email and SMS

    Scenario: Failed KYC Verification with Retry Attempt
        Given the customer provides valid personal details (name, DOB, address, phone, email)
        When the customer uploads ID proof and address proof
        Then the system performs KYC verification
        And if the first attempt of KYC fails due to invalid documents
        When the customer resubmits valid documents
        Then the system re-verifies the KYC
        And if the second attempt of KYC is successful, the system prompts the customer to select account type
        When the customer selects a savings account type and submits application
        Then the system creates an account in core banking
        And the system displays the account number
        And the customer receives a confirmation email and SMS

    Scenario: Failed KYC Verification with Rejection
        Given the customer provides valid personal details (name, DOB, address, phone, email)
        When the customer uploads ID proof and address proof
        Then the system performs KYC verification
        And if both attempts of KYC fail due to invalid documents
        Then the application is rejected

    Scenario: OTP Mismatch for Phone Verification
        Given the customer provides valid personal details (name, DOB, address, phone, email)
        When the customer uploads ID proof and address proof
        Then the system performs KYC verification
        And if KYC is successful, the sys99tem sends an OTP to the customer's registered phone number
        When the customer enters a wrong OTP
        Then the system displays an error message and allows retry once

    Scenario: Duplicate Application for Same ID
        Given the customer has already opened an account with the same ID proof
        When the customer attempts to open another account using the same ID proof
        Then the system displays an error message indicating that a duplicate application is not allowed