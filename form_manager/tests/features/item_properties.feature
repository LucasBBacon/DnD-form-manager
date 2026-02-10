Feature: Item Properties and Usage
    As a player, I want my items to have detailed mechanics so that I can use them in combat and exploration.

    Scenario: Defining a Weapon with Properties
        Given a new character session is started
        When the user creates a custom item named "Dagger"
        And the user sets the item category to "Weapon"
        And the user adds the property "Finesse" to the item
        And the user adds the property "Light" to the item
        And the user adds the property "Thrown" to the item
        Then the item "Dagger" should have properties "Finesse, Light, Thrown"

    Scenario: Equipping an Item
        Given a new character session is started
        And the user has a "Longsword" in their inventory
        And the item "Longsword" is currently unequipped
        When the user equips the "Longsword"
        Then the item "Longsword" should be marked as equipped

    Scenario: Unequipping an Item
        Given a new character session is started
        And the user has a "Shield" in their inventory
        And the item "Shield" is currently equipped
        When the user unequips the "Shield"
        Then the item "Shield" should be marked as unequipped

    Scenario: Defining Item Weight and Calculation
        Given a new character session is started
        And the user has 1 "Chain Mail" weighing 55.0 lbs in their inventory
        And the user has 2 "Shortsword" weighing 2.0 lbs in their inventory
        When the user checks their total inventory weight
        Then the total weight should be 59.0 lbs

    Scenario: Defining Damage Dice for a Weapon
        Given a new character session is started
        And the user has a "Greataxe" in their inventory
        When the user sets the damage die of "Greataxe" to "1d12"
        And the user sets the damage type of "Greataxe" to "Slashing"
        Then the item "Greataxe" should have a damage die of "1d12"
        And the item "Greataxe" should have the damage type of "Slashing"

    Scenario: Using an object as a generic Improvised Weapon
        Given a new character session is started
        And the user has a "Heavy Tome" in their inventory
        When the user treats "Heavy Tome" as an improvised weapon
        Then the item "Heavy Tome" should have a damage die of "1d4"
        And the item "Heavy Tome" should have a range of "20/60"

    Scenario: Using an object similar to an actual weapon
        Given a new character session is started
        And the user has a "Table Leg" in their inventory
        # The DM decides it's like a Club
        When the user treats "Table Leg" as a "Club"
        Then the item "Table Leg" should have a damage die of "1d4"
        And the item "Table Leg" should have the damage type of "Bludgeoning"
        And the item "Table Leg" should have properties "Light"

    Scenario: Throwing a melee weapon that is not designed for throwing
        Given a new character session is started
        And the user has a "Longsword" in their inventory
        And the item "Longsword" does not have the property "Thrown"
        When the user uses the "Longsword" as an improvised thrown weapon
        Then the item "Longsword" should have a damage die of "1d4"
        And the item "Longsword" should have a range of "20/60"

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
    