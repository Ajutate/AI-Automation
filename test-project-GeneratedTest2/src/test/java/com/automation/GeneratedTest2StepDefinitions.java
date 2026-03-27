import io.cucumber.java.en.*;
import io.cucumber.datatable.DataTable;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import java.util.Map;

public class ShoppingCartStepDefinitions {

    private WebDriver driver;
    private LoginPage loginPage;
    private ProductListingPage productListingPage;
    private CartPage cartPage;

    @Before
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        loginPage = new LoginPage(driver);
        productListingPage = new ProductListingPage(driver);
        cartPage = new CartPage(driver);
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Given("the user is logged in and on the product listing page")
    public void theUserIsLoggedInAndOnTheProductListingPage(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        loginPage.login(data.get("email"), data.get("password"));
        productListingPage.navigateTo();
    }

    @When("the user clicks \"Add to Cart\" on a product")
    public void theUserClicksAddToCartOnAProduct() {
        cartPage.addItemToCart();
    }

    @Then("the cart icon displays with count {int}")
    public void theCartIconDisplaysWithCount(int expectedCount) {
        int actualCount = cartPage.getCartItemCount();
        assert actualCount == expectedCount : "Expected cart item count is not matching";
    }

    @And("the cart contains the added product with correct quantity")
    public void theCartContainsTheAddedProductWithCorrectQuantity(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        cartPage.verifyCartItem(data.get("product"), Integer.parseInt(data.get("quantity")));
    }

    @And("the subtotal, tax, shipping estimate, and total are displayed")
    public void theSubtotalTaxShippingEstimateAndTotalAreDisplayed() {
        cartPage.verifyPriceDetails();
    }

    // Scenario: User adds multiple items with different quantities
    @When("the user clicks \"Add to Cart\" for three products with quantities {int}, {int} and {int} respectively")
    public void theUserClicksAddToCartForThreeProductsWithQuantities(int quantity1, int quantity2, int quantity3) {
        productListingPage.clickAddToCart(quantity1);
        productListingPage.clickAddToCart(quantity2);
        productListingPage.clickAddToCart(quantity3);
    }

    // Scenario: User updates product quantity in cart to maximum stock level
    @When("the user increases the quantity to the maximum available (5)")
    public void theUserIncreasesTheQuantityToTheMaximumAvailable() {
        cartPage.increaseItemQuantity(2, 5); // Assuming initial quantity is 2 and max is 5
    }

    // Scenario: User removes individual items from cart
    @When("the user clicks \"Remove\" on one of the items")
    public void theUserClicksRemoveOnOneOfTheItems() {
        cartPage.removeItemFromCart();
    }

    // Scenario: User applies valid discount code to cart
    @When("the user enters {string} as the discount code")
    public void theUserEntersAsTheDiscountCode(String discountCode) {
        cartPage.applyDiscountCode(discountCode);
    }

    // Scenario: User applies invalid discount code to cart
    @Then("the cart does not apply any discount")
    public void theCartDoesNotApplyAnyDiscount() {
        assert !cartPage.isDiscountApplied() : "Discount should not be applied";
    }

    // Scenario Outline: User adds products to cart from product listing or detail page
    @When("the user clicks \"Add to Cart\" on \"{product}\" from the product listing/detail page")
    public void theUserClicksAddToCartOnProductFromTheProductListingDetailPage(String product) {
        productListingPage.clickAddToCart(product);
    }

    // Scenario: User sees out-of-stock warning when adding to cart
    @When("the user clicks \"Add to Cart\"")
    public void theUserClicksAddToCart() {
        cartPage.addItemToCart();
    }

    @Then("the system displays a warning message {string}")
    public void theSystemDisplaysAWarningMessage(String expectedMessage) {
        assert cartPage.getWarningMessage().contains(expectedMessage) : "Expected warning message is not matching";
    }

    // Scenario: User's cart persists for 30 days after login
    @Given("the user has an existing guest cart with items")
    public void theUserHasAnExistingGuestCartWithItems(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productListingPage.addProductsToCart(data.get("products"));
    }

    // Scenario: User's cart shows real-time price calculations
    @When("the product price changes due to inventory updates")
    public void theProductPriceChangesDueToInventoryUpdates() {
        // Simulate price change for testing purposes
        cartPage.updateItemPrice();
    }

    // Scenario: User's cart removes out-of-stock items after 7 days
    @Given("the user has an out-of-stock item in their cart")
    public void theUserHasAnOutOfStockItemInTheirCart(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productListingPage.addProductsToCart(data.get("products"));
    }

    // Scenario: User's cart merge with user cart on login
    @Given("the guest cart contains \"{items}\"")
    public void theGuestCartContainsItems(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productListingPage.addProductsToCart(data.get("items"));
    }

    // Scenario: User's cart displays "Your cart is empty" with CTA to browse products
    @Given("the user has an empty cart")
    public void theUserHasAnEmptyCart() {
        productListingPage.navigateTo();
    }

    // Scenario: User's cart handles session expiration and prompts login
    @Given("the user has items in their cart")
    public void theUserHasItemsInTheirCart(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productListingPage.addProductsToCart(data.get("products"));
    }

    // Scenario: User's cart handles network errors gracefully
    @When("there is a {errorType} error while updating the cart")
    public void thereIsANetworkErrorWhileUpdatingTheCart(String errorType) {
        // Simulate network error for testing purposes
        cartPage.simulateNetworkError(errorType);
    }

    // Scenario: User's cart supports mobile responsiveness
    @Given("the user has items in their cart on a mobile device")
    public void theUserHasItemsInTheirCartOnAMobileDevice() {
        productListingPage.navigateTo();
    }

    // Scenario: User's cart handles out-of-stock during checkout
    @When("the user attempts to proceed to checkout")
    public void theUserAttemptsToProceedToCheckout() {
        cartPage.proceedToCheckout();
    }

    // Scenario: User's cart handles session timeout and prompts login
    @Given("the user has items in their cart")
    public void theUserHasItemsInTheirCart(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productListingPage.addProductsToCart(data.get("products"));
    }

    // Scenario: User's cart handles network errors during checkout
    @When("there is a {errorType} error while processing the order")
    public void thereIsANetworkErrorWhileProcessingTheOrder(String errorType) {
        // Simulate network error for testing purposes
        cartPage.simulateNetworkError(errorType);
    }
}