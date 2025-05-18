Feature: Emergency Braking for Pedestrian Detection

  Scenario: Pedestrian crosses suddenly on urban road - Day
    Given the weather is Clear
    And the road type is Urban during Day time
    And the ego vehicle is moving at 50 km/h in lane 1
    And the driver reaction time is late
    And a pedestrian crosses unexpectedly from the roadside at 20 meters ahead
    When the ego vehicle detects the pedestrian
    Then it must apply emergency braking and stop before collision

  Scenario: Pedestrian runs across highway - Night
    Given the weather is Clear
    And the road type is Highway during Night time
    And the ego vehicle is moving at 100 km/h in lane 1
    And the driver does not react
    And a pedestrian runs across from the median at 30 meters ahead
    When the ego vehicle detects the pedestrian
    Then it must trigger emergency braking immediately

  Scenario: Pedestrian walks slowly across road in rain
    Given the weather is Rainy
    And the road type is Urban during Evening time
    And the ego vehicle is moving at 40 km/h in lane 1
    And the driver reaction time is delayed
    And a pedestrian walks slowly across a crosswalk at 15 meters ahead
    When the ego vehicle detects the pedestrian
    Then it must apply emergency braking and stop before reaching the pedestrian
