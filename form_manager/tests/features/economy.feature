Feature: Economy and Wealth
    As a player, I want to track my coins and the value of my equipment so I know my total wealth.

    Scenario: Adding Coinage
        Given a new character session is started
        When the user adds 100 "gold pieces" to their purse
        And the user adds 50 "silver pieces" to their purse
        Then the character funds should show 100 gp and 50 sp

    Scenario: Calculating Item Value
        Given a new character session is started
        And the user adds a "Gem" worth "500 gp" to their inventory
        And the user adds a "Longsword" worth "15 gp" to their inventory
        When the user checks their total inventory value
        Then the total value should be "515 gp"

    Scenario: Removing Coinage
        Given the user has 10 "gold pieces" in their purse
        When the user removes 5 "gold pieces"
        Then the character funds should show 5 gp

    # Optional: Currency Conversion Scenario
    Scenario: Converting Currency for purchases
        Given the user has 1 "gold piece" in their purse
        And the user has 0 "silver pieces"
        When the user attempts to buy an item costing 5 "silver pieces"
        Then the purchase should be successful
        And the purse should contain 5 "silver pieces"
        And the purse should contain 0 "gold pieces"