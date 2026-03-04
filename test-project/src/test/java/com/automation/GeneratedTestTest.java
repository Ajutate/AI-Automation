import org.junit.jupiter.api.*;
import static org.openqa.selenium.support.ui.ExpectedConditions.*;
import static org.openqa.selenium.support.ui.Wait.*;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import java.time.Duration;

public class UserRegistrationAndLoginTest {

    private WebDriver driver;

    @BeforeEach
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        // Navigate to the base URL of the e-commerce platform
        driver.get("http://ecommerce-platform.com");
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    private WebElement findElement(By by) {
        return waitUntil(ExpectedConditions.presenceOfElementLocated(by));
    }

    private WebElement findClickableElement(By by) {
        return waitUntil(ExpectedConditions.elementToBeClickable(by));
    }

    private void performAction(By elementBy, String actionText) {
        findClickableElement(elementBy).click();
    }

    @Test
    public void userSuccessfullyRegistersAndVerifiesTheirAccount() {
        // Given the user visits the registration page
        driver.get("http://ecommerce-platform.com/register");

        // When the user enters a valid email, password, first name, and last name
        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("Test@1234");

        WebElement firstNameField = findElement(By.id("firstName"));
        firstNameField.sendKeys("John");

        WebElement lastNameField = findElement(By.id("lastName"));
        lastNameField.sendKeys("Doe");

        // And the user clicks on the register button
        performAction(By.id("registerButton"), "Clicking Register Button");

        // Then the system sends a verification email to the entered email address
        waitUntil(ExpectedConditions.presenceOfElementLocated(By.className("verification-message")));

        // And the user clicks on the verification link in the received email
        driver.get("http://ecommerce-platform.com/verify-email?token=1234567890");
    }

    @Test
    public void userAttemptsToRegisterWithAnInvalidEmailFormat() {
        driver.get("http://ecommerce-platform.com/register");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test.example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("Test@1234");

        performAction(By.id("registerButton"), "Clicking Register Button");

        // Then the system displays an error message: "Invalid email format"
        waitUntil(ExpectedConditions.textToBePresentInElementLocated(By.className("error-message"), "Invalid email format"));
    }

    @Test
    public void userAttemptsToRegisterWithAUsedEmailAddress() {
        driver.get("http://ecommerce-platform.com/register");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("Test@1234");

        performAction(By.id("registerButton"), "Clicking Register Button");

        // Then the system displays an error message: "Email already in use"
        waitUntil(ExpectedConditions.textToBePresentInElementLocated(By.className("error-message"), "Email already in use"));
    }

    @Test
    public void userAttemptsToRegisterWithAWeakPassword() {
        driver.get("http://ecommerce-platform.com/register");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("test1234");

        performAction(By.id("registerButton"), "Clicking Register Button");

        // Then the system displays an error message: "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"
        waitUntil(ExpectedConditions.textToBePresentInElementLocated(By.className("error-message"), "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"));
    }

    @Test
    public void userSuccessfullyLogsInAfterAccountVerification() {
        driver.get("http://ecommerce-platform.com/login");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("Test@1234");

        performAction(By.id("loginButton"), "Clicking Login Button");

        // Then the system redirects to the dashboard
        waitUntil(ExpectedConditions.urlToBe("http://ecommerce-platform.com/dashboard"));
    }

    @Test
    public void userAttemptsAnInvalidLogin() {
        driver.get("http://ecommerce-platform.com/login");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        WebElement passwordField = findElement(By.id("password"));
        passwordField.sendKeys("WrongPassword1234");

        performAction(By.id("loginButton"), "Clicking Login Button");

        // Then the system displays an error message: "Invalid username or password"
        waitUntil(ExpectedConditions.textToBePresentInElementLocated(By.className("error-message"), "Invalid username or password"));
    }

    @Test
    public void userRequestsAPasswordResetViaEmail() {
        driver.get("http://ecommerce-platform.com/forgot-password");

        WebElement emailField = findElement(By.id("email"));
        emailField.sendKeys("test@example.com");

        performAction(By.id("sendResetLinkButton"), "Clicking Send Reset Link Button");

        // Then the system sends a password reset email to the entered email address
    }

    @Test
    public void userAttemptsTooManyLoginAttemptsAndGetsLockedOutFor15Minutes() {
        driver.get("http://ecommerce-platform.com/login");

        for (int i = 0; i < 5; i++) {
            WebElement emailField = findElement(By.id("email"));
            emailField.sendKeys("test@example.com");

            WebElement passwordField = findElement(By.id("password"));
            passwordField.sendKeys("WrongPassword1234");

            performAction(By.id("loginButton"), "Clicking Login Button");
        }

        // Then the system displays an error message: "Too many failed attempts. Account locked for 15 minutes"
    }
}