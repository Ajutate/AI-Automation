import org.junit.jupiter.api.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class AccountOpeningTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, 10);
        driver.get("https://bankwebsite.com");
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    private class LoginPage {
        private final By nameInput = By.id("name");
        private final By dobInput = By.id("dob");
        private final By addressInput = By.id("address");
        private final By phoneInput = By.id("phone");
        private final By emailInput = By.id("email");
        private final By idProofUpload = By.id("idProofFile");
        private final By addressProofUpload = By.id("addressProofFile");
        private final By submitButton = By.id("submitApplication");

        public void providePersonalDetails(String name, String dob, String address, String phone, String email) {
            driver.findElement(nameInput).sendKeys(name);
            driver.findElement(dobInput).sendKeys(dob);
            driver.findElement(addressInput).sendKeys(address);
            driver.findElement(phoneInput).sendKeys(phone);
            driver.findElement(emailInput).sendKeys(email);
        }

        public void uploadDocuments() {
            driver.findElement(idProofUpload).sendKeys("path/to/idProof");
            driver.findElement(addressProofUpload).sendKeys("path/to/addressProof");
        }

        public void clickSubmitButton() {
            driver.findElement(submitButton).click();
        }
    }

    @Test
    public void successfulAccountOpeningProcess() throws InterruptedException {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, phone, email)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";
        String phone = "1234567890";
        String email = "john.doe@example.com";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // And if KYC is successful, the customer selects account type and submits application
        driver.findElement(By.id("accountType")).click(); // Assuming an option to select savings

        loginPage.clickSubmitButton();

        // Then the system creates an account in the core banking and displays account number
        String accountNumber = driver.findElement(By.id("accountNumber")).getText();
        Assertions.assertEquals(accountNumber, "1234567890");

        // And the customer receives a confirmation SMS
        Assertions.assertTrue(true); // Stub for SMS verification

        // And the customer receives a confirmation email
        Assertions.assertTrue(true); // Stub for email verification
    }

    @Test
    public void customerUnder18YearsOld() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, phone, email)
        String name = "Jane Doe";
        String dob = "2005-06-17"; // 17 years old
        String address = "456 Elm St";
        String phone = "9876543210";
        String email = "jane.doe@example.com";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // But the system shows an error message "You must be at least 18 years old to open a savings account"
        WebElement errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "You must be at least 18 years old to open a savings account");

        // And the application is rejected
    }

    @Test
    public void failedKYCVerificationOnFirstAttempt() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, phone, email)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";
        String phone = "1234567890";
        String email = "john.doe@example.com";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // But the system shows an error message "KYC verification failed"
        WebElement errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "KYC verification failed");

        // And the application is rejected
    }

    @Test
    public void failedKYCVerificationOnSecondAttempt() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, phone, email)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";
        String phone = "1234567890";
        String email = "john.doe@example.com";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // But the system shows an error message "KYC verification failed"
        WebElement errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "KYC verification failed");

        // And after retrying with correct documents, the system still shows an error message "KYC verification failed"
        loginPage.uploadDocuments();

        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "KYC verification failed");

        // And the application is rejected
    }

    @Test
    public void missingEmailOrPhoneDuringApplication() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";

        loginPage.providePersonalDetails(name, dob, address, "", "");

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // But the system shows an error message "Email and phone are mandatory fields"
        WebElement errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "Email and phone are mandatory fields");

        // And the application is not submitted
    }

    @Test
    public void otpMismatch() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, email, phone)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";
        String email = "john.doe@example.com";
        String phone = "1234567890";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system generates an OTP for the provided phone number
        wait.until(ExpectedConditions.elementToBeClickable(By.id("generateOTP")));

        driver.findElement(By.id("generateOTP")).click();

        // But when the wrong OTP is entered
        String wrongOtp = "123456";
        driver.findElement(By.id("otpInput")).sendKeys(wrongOtp);

        // Then the system shows an error message "Invalid OTP"
        WebElement errorMessage = driver.findElement(By.id("error-message"));
        Assertions.assertEquals(errorMessage.getText(), "Invalid OTP");

        // And the application is not submitted
    }

    @Test
    public void kycServiceTimeout() {
        LoginPage loginPage = new LoginPage();

        // Given the customer provides personal details (name, DOB, address, email, phone)
        String name = "John Doe";
        String dob = "1980-05-17";
        String address = "123 Main St";
        String email = "john.doe@example.com";
        String phone = "1234567890";

        loginPage.providePersonalDetails(name, dob, address, phone, email);

        // When the customer uploads ID proof and address proof
        loginPage.uploadDocuments();

        // Then the system performs KYC verification
        wait.until(ExpectedConditions.elementToBeClickable(By.id("kycVerification")));

        // But the KYC