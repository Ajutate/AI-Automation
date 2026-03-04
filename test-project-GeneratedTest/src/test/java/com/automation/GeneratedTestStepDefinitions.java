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
        // Assume this step is handled by an external system or configuration
    }

    @Given("the database schema for user management is set up")
    public void theDatabaseSchemaForUserManagementIsSetUp() {
        // Assume this step is handled by an external system or configuration
    }

    @Given("OAuth 2.0 and JWT tokens are implemented")
    public void oAuth20AndJwtTokensAreImplemented() {
        // Assume this step is handled by an external system or configuration
    }

    @Given("HTTPS is enabled for all authentication endpoints")
    public void httpsIsEnabledForAllAuthenticationEndpoints() {
        // Assume this step is handled by an external system or configuration
    }

    @Given("rate limiting on login attempts is in place (max 5 attempts per 15 minutes)")
    public void rateLimitingOnLoginAttemptsIsInPlace() {
        // Assume this step is handled by anexternal system or configuration
    }

    @Given("the user has registered with {string}")
    public void theUserHasRegisteredWith(String email) {
        registerPage.register(email, "P@ssw0rd123", "John", "Doe");
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
        registerPage.verifyEmailSent();
    }

    @Then("the system sends an email to the user with the verification link")
    public void theSystemSendsAnEmailToTheUserWithTheVerificationLink() {
        registerPage.checkVerificationEmailSent();
    }

    @When("the user logs in with {string} and {string}")
    public void theUserLogsInWith(String email, String password) {
        loginPage.enterEmail(email);
        loginPage.enterPassword(password);
        loginPage.clickLoginButton();
    }

    @Then("the result is {string}")
    public void theResultIs(String expectedResult) {
        String actualResult = loginPage.getLoginResult();
        assert expectedResult.equals(actualResult) : "Expected: " + expectedResult + ", Actual: " + actualResult;
    }

    @When("the user requests a password reset via email")
    public void theUserRequestsAPasswordResetViaEmail() {
        loginPage.requestPasswordReset();
    }

    @Then("an email with a reset link is sent to {string}")
    public void anEmailWithAResetLinkIsSentTo(String email) {
        // Check if an email was sent and contains the correct reset link
    }

    @When("the user does not log out within 24 hours")
    public void theUserDoesNotLogOutWithin24Hours() {
        loginPage.waitTillSessionExpires();
    }

    @Then("the system recognizes the user as logged in")
    public void theSystemRecognizesTheUserAsLoggedIn() {
        assert loginPage.isUserLoggedIn();
    }

    @When("the user fills in the registration form with invalid email format")
    public void theUserFillsInTheRegistrationFormWithInvalidEmailFormat(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        registerPage.enterFirstName(data.get("First Name"));
        registerPage.enterLastName(data.get("Last Name"));
        registerPage.enterEmail(data.get("Email"));
        registerPage.enterPassword(data.get("Password"));
    }

    @Then("the system shows an error message {string}")
    public void theSystemShowsAnErrorMessage(String errorMessage) {
        assert registerPage.getErrorMessages().contains(errorMessage);
    }

    @Given("the user has registered with {string} and password {string}")
    public void theUserHasRegisteredWithAndPassword(String email, String password1) {
        registerPage.register(email, password1, "John", "Doe");
    }

    @When("the user changes their password to {string}")
    public void theUserChangesTheirPasswordTo(String password2) {
        loginPage.changePassword(password2);
    }

    @Then("the system shows an error message {string}")
    public void theSystemShowsAnErrorMessage1(String errorMessage) {
        assert loginPage.getErrorMessages().contains(errorMessage);
    }
}