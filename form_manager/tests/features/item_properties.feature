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
    