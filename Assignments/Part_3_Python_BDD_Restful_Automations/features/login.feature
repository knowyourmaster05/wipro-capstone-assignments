Feature: SauceDemo Login

  Scenario: Successful Login
    Given I open the SauceDemo login page
    When I enter valid credentials
    Then the URL should contain inventory.html

  Scenario: Invalid Login
    Given I open the SauceDemo login page
    When I enter invalid credentials
    Then I should see an error message