Feature: Shop and Transactions
    As a player, I want to buy and sell items using my purse so that I can acquire new gear and convert loot into wealth.
    
    Background:
        Given a new character session is started
        And the user has 100 "Gold Pieces" in their purse

    Scenario: Buying an affordable item
        # Dagger costs 2 gp
        When the user buys a "Dagger"
        Then the inventory should contain 1 "Dagger"
        And the character funds should show 98 gp and 0 sp

    Scenario: Buying multiple items
        When the user buys 10 "Rations"
        Then the inventory should contain 10 "Rations"
        # Rations = 5 sp. 10 * 5 sp = 5 gp
        And the character funds should show 95 gp and 0 sp
        
    Scenario: Attempting to buy with insufficient funds
        When the user attempts to buy "Plate Armor"
        Then the transaction should fail
        And the inventory should not contain "Plate Armor"
        And the character funds should show 100 gp and 0 sp

    Scenario: Selling an item for half value
        Given the user has a "Light Hammer" in their inventory
        When the user sells the "Light Hammer"
        Then the inventory should not contain "Light Hammer"
        # Light hammer = 2 gp
        And the character funds should show 101 gp and 0 sp

    Scenario: Selling an item with complex cost conversion
        Given the user has a "Chain Shirt" in their inventory
        When the user sells the "Chain Shirt"
        Then the character funds should show 125 gp and 0 sp

    Scenario: Selling items for specific value
        Given the user has a "Gem" worth "50 gp" in their inventory
        When the user sells the "Gem" for "50 gp"
        Then the inventory should not contain "Gem"
        And the character funds should show 150 gp and 0 sp
