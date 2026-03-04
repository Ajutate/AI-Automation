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
        // Assume this step is handled by system configuration or setup script
    }

    @Given("the database schema for user management is set up")
    public void theDatabaseSchemaForUserManagementIsSetUp() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("the SSL certificate is installed")
    public void theSSLCertificateIsInstalled() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("OAuth 2.0 authentication is enabled")
    public void oAuth20AuthenticationIsEnabled() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("JWT tokens are used for session management")
    public void jWTTokensAreUsedForSessionManagement() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("password encryption using bcrypt is implemented")
    public void passwordEncryptionUsingBcryptIsImplemented() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("rate limiting on login attempts is enforced (max 5 attempts per 15 minutes)")
    public void rateLimitingOnLoginAttemptsIsEnforcedMax5AttemptsPer15Minutes() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("HTTPS is required for all authentication endpoints")
    public void httpsIsRequiredForAllAuthenticationEndpoints() {
        // Assume this step is handled by system configuration or setup script
    }

    @Given("the user has registered and verified their account")
    public void theUserHasRegisteredAndVerifiedTheirAccount() {
        // Assume this step is handled by system configuration or setup script
    }

    @When("the user fills in the registration form")
    public void theUserFillsInTheRegistrationForm(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        registerPage.enterFirstName(data.get("First Name"));
        registerPage.enterLastName(data.get("Last Name"));
        registerPage.enterEmail(data.get("Email"));
        registerPage.enterPassword(data.get("Password"));
    }

    @Then("the system validates the email format and uniqueness")
    public void theSystemValidatesTheEmailFormatAndUniqueness() {
        registerPage.validateRegistration();
    }

    @Then("the system generates a verification token for the user's email")
    public void theSystemGeneratesAVerificationTokenForTheUsersEmail() {
        registerPage.verifyEmailGeneration();
    }

    @Then("the system sends a verification email to the user")
    public void theSystemSendsAVerificationEmailToTheUser() {
        registerPage.sendVerificationEmail();
    }

    @When("the user logs in with {string} and {string}")
    public void theUserLogsInWith(String email, String password) {
        loginPage.enterEmail(email);
        loginPage.enterPassword(password);
        loginPage.clickLoginButton();
    }

    @Then("the result is success")
    public void theResultIsSuccess() {
        loginPage.verifyLoginSuccess();
    }

    @Then("the result is failure and appropriate error message is displayed")
    public void theResultIsFailureAndAppropriateErrorMessageIsDisplayed() {
        loginPage.verifyLoginFailure();
    }

    @Given("the user has registered and verified their account")
    public void theUserHasRegisteredAndVerifiedTheirAccount(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        registerPage.enterFirstName(data.get("First Name"));
        registerPage.enterLastName(data.get("Last Name"));
        registerPage.enterEmail(data.get("Email"));
        registerPage.enterPassword(data.get("Password"));
    }

    @When("the user clicks on Forgot Password")
    public void theUserClicksOnForgotPassword() {
        loginPage.clickForgotPassword();
    }

    @And("the user enters {string}")
    public void theUserEnters(String email) {
        loginPage.enterEmail(email);
    }

    @Then("the system sends a password reset link to the user's email")
    public void theSystemSendsAPasswordResetLinkToTheUsersEmail() {
        loginPage.sendPasswordResetLink();
    }

    @When("the user attempts to change password to {string}")
    public void theUserAttemptsToChangePasswordTo(String newPassword) {
        registerPage.enterNewPassword(newPassword);
    }

    @Then("the system rejects the password change due to reuse of last 3 passwords")
    public void theSystemRejectsThePasswordChangeDueToReuseOfLast3Passwords() {
        registerPage.verifyPasswordReuseError();
    }
}