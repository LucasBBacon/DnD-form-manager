Feature: Item Attunement
    As a player, I want ot attune to magical items so that I can gain their magical benefits,
    while the system ensures I respect the 3-item limit and attunement rules.

    Background:
        Given a new character session is started

    Scenario: Successfully attuning to an item
        Given the user has a "Ring of Protection" in their inventory
        And the item "Ring of Protection" requires attunement
        When the user attunes to "Ring of Protection"
        Then the item "Ring of Protection" should be attuned
        And the user should have 1 attuned item
        And the user should have 2 attunement slots remaining

    Scenario: Attempting to attune to a mundane item
        Given the user has a "Longsword" in their inventory
        And the item "Longsword" does not require attunement
        When the user attempts to attune to "Longsword"
        Then the action should fail
        And the item "Longsword" should not be attuned
        And the user should have 0 attuned items

    Scenario: Attunement limit is strictly enforced
        Given the user has attuned to 3 items
        And the user has a "Cloak of Displacement" in their inventory
        And the item "Cloak of Displacement" requires attunement
        When the user attempts to attune to "Cloak of Displacement"
        Then the action should fail
        And the item "Cloak of Displacement" should not be attuned
        And the user should have 0 attunement slots remaining

    Scenario: Attempting to attune to duplicate items
        Given the user has a "Ring of Protection" in their inventory
        And the item "Ring of Protection" requires attunement
        And the user attunes to "Ring of Protection"
        And the user has another "Ring of Protection" in their inventory
        When the user attempts to attune to the second "Ring of Protection"
        Then the action should fail
        And the user should have 1 attuned item

    Scenario: Unattuning from an item
        Given the user has a "Ring of Protection" in their inventory
        And the item "Ring of Protection" requires attunement
        And the user attunes to "Ring of Protection"
        When the user unattunes from "Ring of Protection"
        Then the item "Ring of Protection" should not be attuned
        And the user should have 3 attunement slots remaining