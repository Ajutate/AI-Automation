import io.cucumber.java.en.*;
import io.cucumber.java.Before;
import io.cucumber.java.After;
import io.cucumber.datatable.DataTable;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import java.util.Map;

public class CartManagementStepDefinitions {

    private WebDriver driver;
    private ProductCatalogPage productCatalogPage;
    private CartPage cartPage;
    private LoginPage loginPage;

    @Before
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        productCatalogPage = new ProductCatalogPage(driver);
        cartPage = new CartPage(driver);
        loginPage = new LoginPage(driver);
    }

    @After
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Given("the user is logged in and on the product catalog page")
    public void theUserIsLoggedInAndOnTheProductCatalogPage() {
        loginPage.login("validUser", "validPassword");
        productCatalogPage.navigateToProductCatalog();
    }

    @When("the user adds a product to the cart")
    public void theUserAddsAProductToTheCart(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productCatalogPage.addProductToCart(data.get("Product Name"), Integer.parseInt(data.get("Quantity")));
    }

    @When("the user adds products to the cart")
    public void theUserAddsProductsToTheCart(DataTable dataTable) {
        Map<String, String> data = dataTable.asMap(String.class, String.class);
        productCatalogPage.addProductsToCart(data.get("Product Name"), Integer.parseInt(data.get("Quantity")));
    }

    @When("the user updates the quantity of \"{product}\" to \"{quantity}\"")
    public void theUserUpdatesTheQuantityOfTo(String product, String quantity) {
        productCatalogPage.updateProductQuantity(product, Integer.parseInt(quantity));
    }

    @When("the user removes the \"{product}\" from the cart")
    public void theUserRemovesTheFromTheCart(String product) {
        cartPage.removeProductFromCart(product);
    }

    @When("the user applies the discount code \"{code}\"")
    public void theUserAppliesTheDiscountCode(String code) {
        cartPage.applyDiscountCode(code);
    }

    @When("the user logs in and merges the guest cart")
    public void theUserLogsInAndMergesTheGuestCart() {
        loginPage.login("validUser", "validPassword");
        cartPage.mergeGuestCart();
    }

    @When("the user closes the browser and returns")
    public void theUserClosesTheBrowserAndReturns() {
        driver.quit();
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        cartPage.navigateToCart();
    }

    @When("the user tries to checkout an out-of-stock item")
    public void theUserTriesToCheckoutAnOutOfStockItem() {
        cartPage.attemptCheckoutOutOfStockItem();
    }

    @When("the user's session times out")
    public void theUsersSessionTimesOut() {
        driver.quit();
        driver = new ChromeDriver();
        driver.manage().window().maximize();
        loginPage.login("validUser", "validPassword");
        cartPage.navigateToCart();
    }

    @When("the user tries to add \"{quantity}\" of \"{product}\" which has \"{stock}\" in stock")
    public void theUserTriesToAddOfWhichHasInStock(String quantity, String product, String stock) {
        cartPage.attemptAddProductWithStockLimit(Integer.parseInt(quantity), product, Integer.parseInt(stock));
    }

    @When("the user adds an item with \"{stock}\" quantity")
    public void theUserAddsAnItemWithQuantity(String stock) {
        cartPage.addProductWithStockLimit(Integer.parseInt(stock));
    }

    @When("the user proceeds to checkout with \"{subtotal}\"")
    public void theUserProceedsToCheckoutWith(String subtotal) {
        cartPage.proceedToCheckoutWithSubtotal(Double.parseDouble(subtotal));
    }

    @When("the user selects a shipping address in \"{location}\"")
    public void theUserSelectsAShippingAddressIn(String location) {
        cartPage.selectShippingLocation(location);
    }

    @When("the user abandons the cart after \"{hours}\" hours")
    public void theUserAbandonsTheCartAfterHours(String hours) {
        cartPage.abandonCartAfterHours(Integer.parseInt(hours));
    }

    @When("the user accesses the cart on a \"{device}\" device")
    public void theUserAccessesTheCartOnADevice(String device) {
        cartPage.accessCartOnDevice(device);
    }

    @Then("the cart icon displays \"{number}\" item")
    public void theCartIconDisplaysItem(String number) {
        cartPage.verifyCartItemCount(Integer.parseInt(number));
    }

    @Then("the cart icon displays \"{number}\" items")
    public void theCartIconDisplaysItems(String number) {
        cartPage.verifyCartItemCount(Integer.parseInt(number));
    }

    @Then("the cart shows product thumbnail, name, price, and quantity")
    public void theCartShowsProductDetails() {
        cartPage.verifyProductDetailsInCart();
    }

    @Then("the cart displays subtotal, tax, shipping estimate, and total")
    public void theCartDisplaysTotals() {
        cartPage.verifyCartTotals();
    }

    @Then("the quantity is set to \"{quantity}\" and the system checks stock availability")
    public void theQuantityIsSetToAndSystemChecksStockAvailability(String quantity) {
        cartPage.verifyQuantitySetTo(Integer.parseInt(quantity));
    }

    @Then("the cart shows updated subtotal and total")
    public void theCartShowsUpdatedTotals() {
        cartPage.verifyUpdatedCartTotals();
    }

    @Then("the total is adjusted accordingly")
    public void theTotalIsAdjustedAccordingly() {
        cartPage.verifyTotalAdjustment();
    }

    @Then("the system validates discount codes before application")
    public void theSystemValidatesDiscountCodesBeforeApplication() {
        cartPage.verifyDiscountCodeValidation();
    }

    @Then("the merged cart contains all items from both carts")
    public void theMergedCartContainsAllItems() {
        cartPage.verifyMergedCartItems();
    }

    @Then("the cart persists for 30 days")
    public void theCartPersistsFor30Days() {
        cartPage.verifyCartPersistence();
    }

    @Then("the cart items are still present")
    public void theCartItemsAreStillPresent() {
        cartPage.verifyCartItemsAfterSession();
    }

    @Then("the cart data is stored in Redis cache")
    public void theCartDataIsStoredInRedisCache() {
        cartPage.verifyRedisCacheStorage();
    }

    @Then("a warning is displayed and checkout is disabled")
    public void aWarningIsDisplayedAndCheckoutIsDisabled() {
        cartPage.verifyOutOfStockWarning();
    }

    @Then("the system auto-removes out-of-stock items after 7 days")
    public void theSystemAutoRemovesOutOfStockItems() {
        cartPage.verifyAutoRemovalOfOutOfStockItems();
    }

    @Then("the cart is restored upon login")
    public void theCartIsRestoredUponLogin() {
        cartPage.verifyCartRestoration();
    }

    @Then("the system sends a cart abandonment email after 24 hours")
    public void theSystemSendsCartAbandonmentEmail() {
        cartPage.verifyCartAbandonmentEmail();
    }

    @Then("the quantity is adjusted to \"{stock}\" and a warning is shown")
    public void theQuantityIsAdjustedToAndWarningIsShown(String stock) {
        cartPage.verifyQuantityAdjustmentToStock(Integer.parseInt(stock));
    }

    @Then("the system enforces maximum stock quantity limits")
    public void theSystemEnforcesMaximumStockQuantityLimits() {
        cartPage.verifyStockLimitEnforcement();
    }

    @Then("a warning is displayed")
    public void aWarningIsDisplayed() {
        cartPage.verifyOutOfStockWarning();
    }

    @Then("the item is prevented from checkout")
    public void theItemIsPreventedFromCheckout() {
        cartPage.verifyItemPreventionFromCheckout();
    }

    @Then("the system checks minimum order value of $10")
    public void theSystemChecksMinimumOrderValue() {
        cartPage.verifyMinimumOrderValueCheck();
    }

    @Then("displays appropriate message for orders below $10")
    public void displaysAppropriateMessageForOrdersBelow() {
        cartPage.verifyMinimumOrderMessage();
    }

    @Then("the system applies free shipping for orders over $50")
    public void theSystemAppliesFreeShippingForOrdersOver() {
        cartPage.verifyFreeShippingApplication();
    }

    @Then("displays updated shipping estimate")
    public void displaysUpdatedShippingEstimate() {
        cartPage.verifyUpdatedShippingEstimate();
    }

    @Then("the system calculates tax based on the selected location")
    public void theSystemCalculatesTaxBasedOnLocation() {
        cartPage.verifyTaxCalculationBasedOnLocation();
    }

    @Then("the email includes cart details and a CTA to complete purchase")
    public void theEmailIncludesCartDetailsAndCTA() {
        cartPage.verifyCartAbandonmentEmailContent();
    }

    @Then("the cart is displayed in a responsive layout")
    public void theCartIsDisplayedInResponsiveLayout() {
        cartPage.verifyResponsiveCartLayout();
    }

    @Then("the interface is optimized for touch interactions")
    public void theInterfaceIsOptimizedForTouchInteractions() {
        cartPage.verifyTouchOptimizedInterface();
    }
}