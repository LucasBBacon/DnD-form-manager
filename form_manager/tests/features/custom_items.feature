Feature: Custom Item Names and Templates
    As a player, I want to rename items or create unique items based on templates so that my character feels unique while following the rules.

    Scenario: Renaming an existing item
        Given a new character session is started
        And the user has a "Longsword" in their inventory
        When the user renames "Longsword" to "Goblin Cleaver"
        Then the inventory should contain "Goblin Cleaver"
        And the inventory should not contain "Longsword"
        # It should still retain the base properties
        And the item "Goblin Cleaver" should have damage die "1d8" 

    Scenario: Creating a new item from a Base Template
        Given a new character session is started
        # "Sting" is the name, "Shortsword" is the template/base
        When the user creates an item "Sting" using the "Shortsword" template
        Then the inventory should contain "Sting"
        And the item "Sting" should have the property "Finesse"
        And the item "Sting" should have the property "Light"
        And the item "Sting" should have a weight of 2.0 lbs

    Scenario: Overriding properties on a Custom Named item
        Given a new character session is started
        And the user creates an item "Mithral Chain Shirt" using the "Chain Shirt" template
        When the user sets the item weight to 10.0 lbs
        # Base Chain Shirt is 20 lbs, we check it didn't use the default
        Then the item "Mithral Chain Shirt" should have a weight of 10.0 lbs
        And the item "Mithral Chain Shirt" should be Category "Armor"