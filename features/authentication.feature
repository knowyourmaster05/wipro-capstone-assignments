@auth
Feature: Authentication API - Verify Login
  As a QA engineer
  I want to validate login endpoints across positive and negative paths
  So that I can trust authentication behaviour before shipping

  Background:
    Given the "automation_exercise" API client is ready

  @smoke @auth @negative
  Scenario Outline: Verify login with invalid credentials variants
    When I attempt to verify login with the "<case>" payload
    Then the response body code should be <status>
    And the response body should contain "<message>"

    Examples:
      | case          | status | message        |
      | missing email | 404    | User not found |
      | missing pass  | 404    | User not found |
      | invalid email | 404    | User not found |
      | wrong creds   | 404    | User not found |

  @regression @auth
  Scenario: Verify login with valid credentials after account creation
    Given I have created a user with a randomly generated payload
    When I verify login using the last created user's credentials
    Then the response status code should be 200
    And the response body should contain "User exists!"

  @regression @negative @auth
  Scenario: DELETE method on verifyLogin is not supported
    When I send a DELETE request to the verify login endpoint
    Then the response status code should be 200
    And the response body should contain "not supported"