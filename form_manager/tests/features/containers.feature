Feature: Containers and Storage
    As a player, I want to organize my items into containers (like backpacks and pouches) so that I can manage my inventory capacity and organization.

    Background:
        Given a new character session is started
        And the user has a "Backpack" in their inventory
        And the item "Backpack" is a container with capacity 30.0 lbs and base weight 5.0 lbs

    Scenario: Adding Items to a Container
        Given the user has a "Torch" weighing 1.0 lbs in their inventory
        When the user moves "Torch" into "Backpack"
        Then the inventory should not contain "Torch" at the top level
        And the "Backpack" should contain "Torch"
        And the "Backpack" total weight should be 6.0 lbs

    Scenario: Calculating Character Weight with Nested Items
        Given the user has 2 "Rations" weighing 2.0 lbs in their inventory
        And the user moves 2 "Rations" into "Backpack"
        When the user checks their total inventory weight
        Then the total weight should be 9.0 lbs

    Scenario: Container Capacity Limits
        Given the "Backpack" contains items weighing 29.0 lbs
        And the use has a "Greatsword" weighing 6.0 lbs
        When the user attempts to move "Greatsword" into "Backpack"
        Then the action should fail
        And the "Backpack" should not contain "Greatsword"

    Scenario: Retrieving Items from a Container
        Given the "Backpack" contains "Rope"
        When the user retrieves "Rope" from "Backpack"
        Then the inventory should contain "Rope" at the top level
        And the "Backpack" should not contain "Rope"

    Scenario: Dropping a Container
        Given the user has a "Backpack" weighing 35.0 lbs total
        And the user total weight is 150.0 lbs
        When the user drops the "Backpack"
        Then The user total weight should be 115.0 lbs
        And the inventory should not contain "Backpack"