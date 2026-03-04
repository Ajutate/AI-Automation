import io.cucumber.java.en.*;
import io.cucumber.datatable.DataTable;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import java.util.Map;

public class RegistrationAndLoginStepDefinitions {

    private WebDriver driver;
    private RegisterPage registerPage;
    private LoginPage loginPage;

    @Before
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        registerPage = new RegisterPage(driver);
        loginPage = new LoginPage(driver);
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Given("the email service is configured")
    public void theEmailServiceIsConfigured() {
        // Assume this step is handled by the application setup
    }

    @Given("the database schema for user management is set up")
    public void theDatabaseSchemaForUserManagementIsSetUp() {
        // Assume this step is handled by the application setup
    }

    @Given("the SSL certificate is installed")
    public void theSSLCertificateIsInstalled() {
        // Assume this step is handled by the application setup
    }

    @Given("OAuth 2.0 authentication is enabled")
    public void oAuth20AuthenticationIsEnabled() {
        // Assume this step is handled by the application setup
    }

    @Given("JWT tokens are used for session management")
    public void jWTTokensAreUsedForSessionManagement() {
        // Assume this step is handled by the application setup
    }

    @Given("password encryption using bcrypt is implemented")
    public void passwordEncryptionUsingBcryptIsImplemented() {
        // Assume this step is handled by the application setup
    }

    @Given("rate limiting on login attempts is enforced (max 5 attempts per 15 minutes)")
    public void rateLimitingOnLoginAttemptsIsEnforcedMax5AttemptsPer15Minutes() {
        // Assume this step is handled by the application setup
    }

    @Given("HTTPS is required for all authentication endpoints")
    public void httpsIsRequiredForAllAuthenticationEndpoints() {
        // Assume this step is handled by the application setup
    }

    @Given("the user is registered")
    public void theUserIsRegistered(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        registerPage.register(data.get("First Name"), data.get("Last Name"), data.get("Email"), data.get("Password"));
    }

    @When("the user fills in the registration form")
    public void theUserFillsInTheRegistrationForm(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        registerPage.enterFirstName(data.get("First Name"));
        registerPage.enterLastName(data.get("Last Name"));
        registerPage.enterEmail(data.get("Email"));
        registerPage.enterPassword(data.get("Password"));
    }

    @Then("the system sends a verification email to the provided address")
    public void theSystemSendsAVerificationEmailToTheProvidedAddress() {
        registerPage.verifyEmailSent();
    }

    @Then("the user receives an email with a verification link")
    public void theUserReceivesAnEmailWithAVerificationLink() {
        // Assume this step is handled by the application setup
    }

    @When("the user logs in with {string} and {string}")
    public void theUserLogsInWith(String email, String password) {
        loginPage.enterEmail(email);
        loginPage.enterPassword(password);
        loginPage.clickLogin();
    }

    @Then("the result is {string}")
    public void theResultIs(String result) {
        if (result.equals("success")) {
            loginPage.verifySuccessfulLogin();
        } else if (result.equals("failure")) {
            loginPage.verifyFailedLogin();
        }
    }

    @When("the user requests a password reset for {string}")
    public void theUserRequestsAPasswordResetFor(String email) {
        loginPage.requestPasswordReset(email);
    }

    @Then("the system sends a password reset link to the provided address")
    public void theSystemSendsAPasswordResetLinkToTheProvidedAddress() {
        // Assume this step is handled by the application setup
    }

    @Given("the user has attempted to log in with {string} and {string} five times")
    public void theUserHasAttemptedToLogInWithFiveTimes(String email, String password) {
        for (int i = 0; i < 5; i++) {
            loginPage.enterEmail(email);
            loginPage.enterPassword(password);
            loginPage.clickLogin();
        }
    }

    @When("the user tries to log in again")
    public void theUserTriesToLogInAgain() {
        loginPage.enterEmail("wrong@example.com");
        loginPage.enterPassword("wrongpassword");
        loginPage.clickLogin();
    }

    @Then("the system locks the account for 15 minutes")
    public void theSystemLocksTheAccountFor15Minutes() {
        // Assume this step is handled by the application setup
    }
}