Feature: Encumbrance and Capacity
    As a player, I want to track my inventory weight against my Strength so that I know if I am slowed down.

    Background:
        Given a new character session is started
        And the user has a "Strength" score of 10
        # Base capacity = 10 * 15 = 150 lbs
        # Encumbered = 10 * 5 = 50 lbs
        # Heavily Encumbered = 10 * 10 = 100 lbs

    Scenario: Calculating Base Carrying Capacity
        Then the carrying capacity should be 150 lbs
        And the max push, drag, or lift capacity should be 300 lbs

    Scenario: Large Creatures have Double Capacity
        Given the user size is set to "Large"
        Then the carrying capacity should be 300 lbs

    Scenario: Unencumbered Status
        Given the variant encumbrance rule is enabled
        And the user has items weighing 45 lbs
        Then the encumbrance status should be "Unencumbered"
        And the speed penalty should be 0 ft

    Scenario: Encumbered Status (Variant)
        Given the variant encumbrance rule is enabled
        And the user has items weighing 55 lbs
        Then the encumbrance status should be "Encumbered"
        And the speed penalty should be 10 ft

    Scenario: Encumbered Status (Variant)
        Given the variant encumbrance rule is enabled
        And the user has items weighing 105 lbs
        Then the encumbrance status should be "Heavily Encumbered"
        And the speed penalty should be 20 ft

    Scenario: Exceeding Carrying Capacity
        Given the variant encumbrance rule is enabled
        And the user has items weighing 155 lbs
        Then the encumbrance status should be "Over Capacity"
        And the speed should be 5 ft
