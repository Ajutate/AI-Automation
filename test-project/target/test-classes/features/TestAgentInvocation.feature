Feature: Online Account Opening - Retail Savings

As a Customer,
I want to open a savings account online,
So that I can start managing my finances with the bank.

Background:
Given the customer is on the bank's website and has not started any application process yet
And the KYC service is available
And the core banking system is operational
And the email and phone numbers are masked in logs

Scenario: Successful Account Opening Process
Given the customer provides personal details (name, DOB, address, phone, email)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
And if KYC is successful, the customer selects account type and submits application
Then the system creates an account in the core banking and displays account number
And the customer receives a confirmation SMS
And the customer receives a confirmation email

Scenario: Customer Under 18 Years Old
Given the customer provides personal details (name, DOB, address, phone, email)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
But the system shows an error message "You must be at least 18 years old to open a savings account"
And the application is rejected

Scenario: Failed KYC Verification on First Attempt
Given the customer provides personal details (name, DOB, address, phone, email)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
But the system shows an error message "KYC verification failed"
And the application is rejected

Scenario: Failed KYC Verification on Second Attempt
Given the customer provides personal details (name, DOB, address, phone, email)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
But the system shows an error message "KYC verification failed"
And after retrying with correct documents, the system still shows an error message "KYC verification failed"
And the application is rejected

Scenario: Missing Email or Phone During Application
Given the customer provides personal details (name, DOB, address)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
But the system shows an error message "Email and phone are mandatory fields"
And the application is not submitted

Scenario: OTP Mismatch
Given the customer provides personal details (name, DOB, address, email, phone)
When the customer uploads ID proof and address proof
Then the system generates an OTP for the provided phone number
But when the wrong OTP is entered
Then the system shows an error message "Invalid OTP"
And the application is not submitted

Scenario: KYC Service Timeout
Given the customer provides personal details (name, DOB, address, email, phone)
When the customer uploads ID proof and address proof
Then the system performs KYC verification
But the KYC service times out
Then the system shows an error message "KYC service timed out"
And the application is not submitted

Scenario: Duplicate Application for Same ID
Given a duplicate customer with similar personal details (name, DOB, address, email, phone)
When this customer attempts to upload ID proof and address proof
Then the system detects a duplicate account attempt
Then the system shows an error message "Duplicate application detected"
And the application is rejected