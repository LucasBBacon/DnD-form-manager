Feature: Character Inventory Management
    As a player, I want to manage my inventory so that I can track what equipment and loot my character is carrying.

    Scenario: Adding a New Non-Stackable Item
        Given a new character session is started
        When the user adds a "Longsword" to their inventory
        Then the inventory should contain 1 "Longsword"
        And the item "Longsword" should not be stackable

    Scenario: Adding a Stackable Item to a New Slot
        Given a new character session is started
        And the user inventory is empty
        When the user adds 5 "Rations" to their inventory
        Then the inventory should contain 5 "Rations"
        And the "Rations" entry should be marked as stackable

    Scenario: Stacking Items on Existing Slots
        Given a new character session is started
        And the user has 5 "Torches" in their inventory
        When the user adds 5 "Torches" to their inventory
        Then the inventory should contain 10 "Torches"
        And the inventory should still have only 1 entry for "Torches"

    Scenario: Removing Items from a Stack
        Given a new character session is started
        And the user has 10 "Arrows" in their inventory
        When the user removes 3 "Arrows"
        Then the inventory should contain 7 "Arrows"

    Scenario: Removing the Last Item from a Stack
        Given a new character session is started
        And the user has 1 "Potion of Healing" in their inventory
        When the user removes 1 "Potion of Healing"
        Then "Potion of Healing" should be removed from the inventory list

    Scenario: Adding a Custom Item
        Given a new character session is started
        When the user creates a custom item named "Grandma's Pie"
        And the user sets the item as non-stackable
        Then the inventory should contain "Grandma's Pie"
