@user_mgmt
Feature: User Management API - AutomationExercise
  As an API consumer
  I want to create, retrieve, update and delete user accounts
  So that I can verify the User Management lifecycle end-to-end

  Background:
    Given the "automation_exercise" API client is ready

  @smoke @user_mgmt
  Scenario: Create a new user successfully
    When I create a user with a randomly generated payload
    Then the response status code should be 200
    And the response body should contain "User created!"
    And the response body should conform to the "login_response" schema

  @regression @user_mgmt @database
  Scenario: Created user is persisted in the database
    When I create a user with a randomly generated payload
    Then the response status code should be 200
    And the response body should contain "User created!"
    And the last created user should exist in the database

  @regression @user_mgmt
  Scenario: Retrieve a user by email after creation
    Given I have created a user with a randomly generated payload
    When I request user details for the last created user's email
    Then the response status code should be 200
    And the response should contain the last created user's email

  @regression @user_mgmt
  Scenario: Update an existing user's details
    Given I have created a user with a randomly generated payload
    When I update the last created user's company to "Updated Corp"
    Then the response status code should be 200
    And the response body should contain "User updated!"

  @regression @negative @user_mgmt @database
  Scenario: Delete a user and verify removal
    Given I have created a user with a randomly generated payload
    When I delete the last created user
    Then the response status code should be 200
    And the response body should contain "Account deleted!"
    And the last created user should NOT exist in the database

  @regression @contract @user_mgmt
  Scenario: Validate user object against JSON schema
    Given I have created a user with a randomly generated payload
    When I request user details for the last created user's email
    Then the response status code should be 200
    And the response body should conform to the "user" schema