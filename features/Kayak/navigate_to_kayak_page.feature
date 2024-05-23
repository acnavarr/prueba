@regression_tests

Feature: Validate element created dropdown column

#  Scenario: Navigate to the Kayak home page and validate principal elements
#    Given I navigate to the kayak main page
#    Then I should be in the "home" page
#    And The page "should" contain the next elements
#      | name                   | type   |
#      | name_tag               | input  |
##      | name_dropdown_column   | input  |
##      | search_tag             | input  |
##      | cancel                 | button |
##      | create_column_disabled | button |
#
  @18 @regression
  Scenario: Validate URL of Home page
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    And The url page should be contain to the next "https://www.kayak.com" url

  @19 @regression
  Scenario Outline: Navigate between countries and validate the URL
      Given I navigate to the kayak main page
      Then I should be in the "home" page
      When I navigate to the "<url>" URL
      Then The url page should be equal to the next "<url>" url

    Examples:
      | url                       |
      | https://www.kayak.com.my/ |
      | https://www.kayak.com.pr/ |
      | https://www.kayak.com.br/ |
#
  @20 @regression
  Scenario Outline: Navigate by menu options
      Given I navigate to the kayak main page
      Then I should be in the "home" page
      When I enter to "<submenu>" option
      Then The url page should be equal to the next "<url>" url
      And The page title should "contain" the "<title>" text

    Examples:
     |submenu | url                       |title|
     |Vuelos | https://www.kayak.com.co/flights |Vuelos y tiquetes baratos|
     |Alojamientos | https://www.kayak.com.co/stays |Dónde alojarse: busca ofertas y descuentos de alojamiento - KAYAK|
     |Carros | https://www.kayak.com.co/cars |Encuentra ofertas de renta de autos                                     |
     |Paquetes | https://www.kayak.com.co/citybreaks |Paquetes turísticos baratos, vuelos y más                       |
     |Explore | https://www.kayak.com.co/explore |KAYAK Explore'                                                      |
     |Blog | https://www.kayak.com.co/news/ |Noticias y consejos expertos                                             |
     |Vuelos directos | https://www.kayak.com.co/direct |Vuelos directos                                              |
     |El mejor momento | https://www.kayak.com.co/el-mejor-momento-para-viajar |El mejor momento para viajar'         |
     |KAYAK for Business | https://www.kayak.com.co/business |KAYAK for Business: Gestión de viajes de negocios con KAYAK|


