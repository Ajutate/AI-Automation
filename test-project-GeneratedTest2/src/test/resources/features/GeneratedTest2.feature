Feature: Shopping Cart Management System

  Scenario: User adds a single item to an empty cart
    Given the user is logged in and on the product listing page
    When the user clicks "Add to Cart" on a product
    Then the cart icon displays with count "1"
    And the cart contains the added product with correct quantity
    And the subtotal, tax, shipping estimate, and total are displayed

  Scenario: User adds multiple items with different quantities
    Given the user is logged in and on the product listing page
    When the user clicks "Add to Cart" for three products with quantities 1, 2, and 3 respectively
    Then the cart icon displays with count "6"
    And the cart contains all added products with correct quantities
    And the subtotal, tax, shipping estimate, and total are updated

  Scenario: User updates product quantity in cart to maximum stock level
    Given the user is logged in and has an item in their cart with a quantity of 2
    When the user increases the quantity to the maximum available (5)
    Then the cart contains the item with the new quantity "5"
    And the subtotal, tax, shipping estimate, and total are updated

  Scenario: User removes individual items from cart
    Given the user is logged in and has multiple items in their cart
    When the user clicks "Remove" on one of the items
    Then the item is removed from the cart
    And the cart icon displays with a reduced count
    And the subtotal, tax, shipping estimate, and total are updated

  Scenario: User applies valid discount code to cart
    Given the user is logged in and has multiple items in their cart
    When the user enters "SUMMER20" as the discount code
    Then the cart displays the applied discount
    And the subtotal, tax, shipping estimate, and total are updated

  Scenario: User applies invalid discount code to cart
    Given the user is logged in and has multiple items in their cart
    When the user enters "INVALIDCODE123" as the discount code
    Then the cart does not apply any discount
    And the subtotal, tax, shipping estimate, and total remain unchanged

  Scenario Outline: User adds products to cart from product listing or detail page
    Given the user is logged in
    When the user clicks "Add to Cart" on "<product>" from the product listing/detail page
    Then the cart contains "<product>" with quantity "1"
    And the subtotal, tax, shipping estimate, and total are updated

    Examples:
      | product         |
      | T-Shirt         |
      | Hoodie           |
      | Laptop Bag       |

  Scenario: User sees out-of-stock warning when adding to cart
    Given the user is logged in and a product with quantity "0" is available
    When the user clicks "Add to Cart"
    Then the system displays a warning message "This item is currently out of stock. It will be removed from your cart."
    And the item is not added to the cart

  Scenario: User's cart persists for 30 days after login
    Given the user has an existing guest cart with items
    When the user logs in and their saved cart is merged
    Then the user sees all items from both the guest and saved carts
    And the subtotal, tax, shipping estimate, and total are updated

  Scenario: User's cart shows real-time price calculations
    Given the user has an item in their cart with a dynamic price
    When the product price changes due to inventory updates
    Then the cart displays the updated price for that item
    And the subtotal, tax, shipping estimate, and total are recalculated

  Scenario: User's cart removes out-of-stock items after 7 days
    Given the user has an out-of-stock item in their cart
    When 7 days pass without any action from the user
    Then the system automatically removes the out-of-stock item from the cart with a notification

  Scenario Outline: Guest cart merge with user cart on login
    Given the guest cart contains "<items>"
    And the user logs in and their saved cart is merged
    Then the user sees all items from both the guest and saved carts
    And the subtotal, tax, shipping estimate, and total are updated

    Examples:
      | items          |
      | T-Shirt        |
      | Hoodie         |

  Scenario: User's cart displays "Your cart is empty" with CTA to browse products
    Given the user has an empty cart
    When the user views their cart page
    Then the system displays a message "Your cart is empty. Start browsing our products now!"
    And there is a call-to-action link to browse products

  Scenario: User's cart handles session expiration and prompts login
    Given the user has items in their cart
    When the user's session expires and they navigate away from the cart page
    Then the system displays a message "Your session has expired. Please log in again."
    And the saved cart is restored upon successful login

  Scenario Outline: User's cart handles network errors gracefully
    Given the user has items in their cart
    When there is a network error while updating the cart
    Then the system displays a retry option and does not lose any cart data

    Examples:
      | errorType     |
      | Timeout       |
      | Server Error  |

  Scenario: User's cart supports mobile responsiveness
    Given the user has items in their cart on a mobile device
    When the user navigates to the cart page
    Then the system displays a responsive layout suitable for mobile devices

  Scenario Outline: User's cart handles out-of-stock during checkout
    Given the user is logged in and has an item with quantity "0" in their cart
    When the user attempts to proceed to checkout
    Then the system displays a warning message "This item is currently out of stock. It will be removed from your cart."
    And the item is not included in the order

  Scenario: User's cart handles session timeout and prompts login
    Given the user has items in their cart
    When the user's session times out after 24 hours
    Then the system displays a message "Your session has expired. Please log in again."
    And the saved cart is restored upon successful login

  Scenario: User's cart handles network errors during checkout
    Given the user has items in their cart and attempts to proceed to checkout
    When there is a network error while processing the order
    Then the system displays a retry option and does not lose any cart data