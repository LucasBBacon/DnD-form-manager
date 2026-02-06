Feature: Racial Modifiers
    As a player, I want to select my Race so that my base statistics and features are correctly populated according to the Player's Handbook (PHB)

    Scenario: Applying Fixed Racial Ability Bonuses and Features
        Given a new character session is started with default stats
        When the user selects "Dwarf" as their race
        Then the user "Constitution" score should increase by 2
        And the user size should be set to "Medium"
        And the user speed should be set to 25 ft
        And "Darkvision" should be added to the user feature list
        And "Dwarven Resilience" should be added to the user feature list
        And "Dwarven Combat Training" should be added to the user feature list
        And "Tool Proficiency" should be added to the user pending choices
        And "Stonecutting" should be added to the user feature list
        And "Common" should be added to the user languages
        And "Dwarvish" should be added to the user languages


    Scenario: Applying Fixed Sub Race Racial Ability Bonuses and Features
        Given a new character session is started with default stats
        When the user selects "Dwarf" as their race
        And the user selects "Mountain Dwarf" as their subrace
        Then the user "Constitution" score should increase by 2
        Then the user "Strength" score should increase by 2
        And the user size should be set to "Medium"
        And the user speed should be set to 25 ft
        And "Darkvision" should be added to the user feature list
        And "Dwarven Resilience" should be added to the user feature list
        And "Dwarven Combat Training" should be added to the user feature list
        And "Tool Proficiency" should be added to the user pending choices
        And "Stonecutting" should be added to the user feature list
        And "Common" should be added to the user languages
        And "Dwarvish" should be added to the user languages
        And "Dwarven Armor Training" should be added to the user feature list
        