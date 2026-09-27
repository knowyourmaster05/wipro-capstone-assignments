@catalog
Feature: Product Catalog API - AutomationExercise
  As a QA engineer
  I want to validate the catalog endpoints
  So that I can verify read-only and error-path behaviour

  Background:
    Given the "automation_exercise" API client is ready

  @smoke @catalog
  Scenario: Fetch all products and validate schema
    When I fetch all products
    Then the response status code should be 200
    And the response body should conform to the "product" schema

  @regression @catalog
  Scenario: Fetch all brands
    When I fetch all brands
    Then the response status code should be 200

  @regression @catalog
  Scenario Outline: Search for products by term
    When I search for products with term "<term>"
    Then the response status code should be 200
    And the response body should contain at least <min_results> product(s)

    Examples:
      | term   | min_results |
      | top    | 1           |
      | tshirt | 1           |
      | jean   | 1           |
      | dress  | 1           |

  @regression @negative @catalog
  Scenario: Search without required parameter returns 400
    When I search for products without the required parameter
    Then the response status code should be 200
    And the response body should contain "Bad request"

  @regression @negative @catalog
  Scenario: POST to productsList is not supported
    When I send a POST request to the products list endpoint
    Then the response status code should be 200
    And the response body should contain "not supported"

  @regression @negative @catalog
  Scenario: PUT to brandsList is not supported
    When I send a PUT request to the brands list endpoint
    Then the response status code should be 200
    And the response body should contain "not supported"
