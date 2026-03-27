Feature: Shopping Cart Management System

Background: The user is logged in and on the product catalog page with a valid session

Scenario: Add single item to empty cart
  When the user adds a product to the cart
    | Product Name | Price | Quantity |
    | Laptop       | 999.99 | 1        |
  Then the cart icon displays "1" item
  And the cart shows product thumbnail, name, price, and quantity

Scenario: Add multiple items with different quantities
  When the user adds products to the cart
    | Product Name | Price | Quantity |
    | Laptop       | 999.99 | 1        |
    | Smartphone   | 699.99 | 2        |
  Then the cart icon displays "3" items
  And the cart displays subtotal, tax, shipping estimate, and total

Scenario Outline: Update product quantity to max stock level
  When the user updates the quantity of "<product>" to "<quantity>"
    | product | quantity |
    | Laptop  | 5        |
    | Smartphone | 3      |
  Then the quantity is set to "<quantity>" and the system checks stock availability
  And the cart shows updated subtotal and total

Scenario: Remove item from cart with multiple items
  When the user removes the "<product>" from the cart
    | product |
    | Laptop  |
  Then the cart icon displays "2" items
  And the cart shows updated subtotal and total

Scenario Outline: Apply valid/invalid discount codes
  When the user applies the discount code "<code>"
    | code         | result |
    | DISCOUNT10  | success |
    | INVALIDCODE | failure |
  Then the total is adjusted accordingly
  And the system validates discount codes before application

Scenario: Guest cart merge with user cart on login
  When the user logs in and merges the guest cart
  Then the merged cart contains all items from both carts
  And the cart persists for 30 days

Scenario: Cart persistence across browser sessions
  When the user closes the browser and returns
  Then the cart items are still present
  And the cart data is stored in Redis cache

Scenario: Handle out-of-stock during checkout
  When the user tries to checkout an out-of-stock item
  Then a warning is displayed and checkout is disabled
  And the system auto-removes out-of-stock items after 7 days

Scenario: Cart recovery after session timeout
  When the user's session times out
  Then the cart is restored upon login
  And the system sends a cart abandonment email after 24 hours

Scenario Outline: Quantity exceeds stock
  When the user tries to add "<quantity>" of "<product>" which has "<stock>" in stock
    | product | quantity | stock |
    | Laptop  | 10       | 5     |
  Then the quantity is adjusted to "<stock>" and a warning is shown
  And the system enforces maximum stock quantity limits

Scenario Outline: Out-of-stock item warning
  When the user adds an item with "<stock>" quantity
    | stock |
    | 0     |
  Then a warning is displayed
  And the item is prevented from checkout

Scenario Outline: Minimum order value validation
  When the user proceeds to checkout with "<subtotal>"
    | subtotal |
    | 5        |
    | 15       |
  Then the system checks minimum order value of $10
  And displays appropriate message for orders below $10

Scenario Outline: Free shipping eligibility
  When the user proceeds to checkout with "<subtotal>"
    | subtotal |
    | 40       |
    | 60       |
  Then the system applies free shipping for orders over $50
  And displays updated shipping estimate

Scenario Outline: Tax calculation based on shipping address
  When the user selects a shipping address in "<location>"
    | location |
    | California |
    | New York  |
  Then the system calculates tax based on the selected location
  And displays updated total with tax applied

Scenario Outline: Cart abandonment email
  When the user abandons the cart after "<hours>" hours
    | hours |
    | 24    |
    | 48    |
  Then a cart abandonment email is sent
  And the email includes cart details and a CTA to complete purchase

Scenario Outline: Mobile responsive cart interface
  When the user accesses the cart on a "<device>" device
    | device |
    | mobile |
    | tablet |
  Then the cart is displayed in a responsive layout
  And the interface is optimized for touch interactions