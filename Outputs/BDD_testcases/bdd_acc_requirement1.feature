Feature: Adaptive Cruise Control (ACC) Scenarios

  Scenario: ACC Following - Clear Day - Highway - Constant Speed
    Given the weather is Clear and the lighting is Daylight
    And the road type is Highway with Medium traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 25 m/s with an ACC gap of 1.0 second
    And there is a lead vehicle in the Center lane, 50 meters ahead, traveling at 25 m/s and maintaining constant speed
    When the lead vehicle maintains constant speed.
    Then the ego vehicle maintains a constant following distance corresponding to the selected ACC gap (1.0 second).

  Scenario: ACC Following - Clear Day - Highway - Lead Vehicle Slows Down
    Given the weather is Clear and the lighting is Daylight
    And the road type is Highway with Medium traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 25 m/s with an ACC gap of 1.0 second
    And there is a lead vehicle in the Center lane, 50 meters ahead, traveling at 25 m/s and decelerating to 15 m/s at a rate of 2 m/s^2
    When the lead vehicle decelerates.
    Then the ego vehicle decelerates smoothly to maintain the selected ACC gap (1.0 second) without exceeding a comfortable deceleration rate.

  Scenario: ACC Following - Clear Day - Highway - Lead Vehicle Accelerates
    Given the weather is Clear and the lighting is Daylight
    And the road type is Highway with Medium traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 20 m/s with an ACC gap of 1.5 seconds
    And there is a lead vehicle in the Center lane, 60 meters ahead, traveling at 20 m/s and accelerating to 30 m/s at a rate of 1 m/s^2
    When the lead vehicle accelerates.
    Then the ego vehicle accelerates smoothly to maintain the selected ACC gap (1.5 seconds) without exceeding a comfortable acceleration rate.

  Scenario: ACC Following - Rain - Highway - Lead Vehicle Slows Down Abruptly
    Given the weather is Rain and the lighting is Daylight
    And the road type is Highway with High traffic density and Wet road condition
    And the ego vehicle is a SUV in the Center lane, traveling at 30 m/s with an ACC gap of 2.0 seconds
    And there is a lead vehicle in the Center lane, 70 meters ahead, traveling at 30 m/s and decelerating to 5 m/s at a rate of 5 m/s^2
    When the lead vehicle decelerates abruptly.
    Then the ego vehicle decelerates rapidly to maintain the selected ACC gap (2.0 seconds), potentially engaging emergency braking if necessary to avoid a collision. The deceleration rate should be adjusted based on road conditions (wet).

  Scenario: ACC Following - Night - Highway - Lead Vehicle Changes Lane
    Given the weather is Clear and the lighting is Night
    And the road type is Highway with Low traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 28 m/s with an ACC gap of 1.2 seconds
    And there is a lead vehicle in the Center lane, 65 meters ahead, traveling at 28 m/s and changing lane to the right after 5 seconds.
    When the lead vehicle changes lane.
    Then the ego vehicle maintains its speed if no other vehicle is detected in the ego lane. If another vehicle is detected after the lane change of the lead vehicle, then the ego vehicle should adjust its speed to maintain the desired gap to the new lead vehicle.

  Scenario: ACC Following - Sunny - Highway - Cut-in Vehicle
    Given the weather is Sunny and the lighting is Daylight
    And the road type is Highway with Medium traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 22 m/s with an ACC gap of 1.5 seconds
    And there is a lead vehicle in the Center lane, 55 meters ahead, traveling at 22 m/s and maintaining constant speed
    And there is a cut-in vehicle in the Left lane, 70 meters ahead with a lateral offset of 3.7 meters, traveling at 25 m/s and changing lane to the center lane in front of the ego vehicle.
    When the cut-in vehicle merges into the ego vehicle's lane.
    Then the ego vehicle detects the cut-in vehicle and decelerates to maintain the selected ACC gap (1.5 seconds) from the cut-in vehicle.

  Scenario: ACC Following - Fog - Highway - Low Visibility - Lead Vehicle Decelerates
    Given the weather is Fog and the lighting is Daylight
    And the road type is Highway with Low traffic density and Low visibility
    And the ego vehicle is a Truck in the Center lane, traveling at 18 m/s with an ACC gap of 2.5 seconds
    And there is a lead vehicle in the Center lane, 45 meters ahead, traveling at 18 m/s and decelerating to 10 m/s at a rate of 1.5 m/s^2
    When the lead vehicle decelerates in low visibility conditions.
    Then the ego vehicle decelerates smoothly, taking into account the reduced visibility and increased ACC gap (2.5 seconds), to maintain a safe following distance.

  Scenario: ACC Following - Clear Day - Curved Road - Lead Vehicle Maintains Speed
    Given the weather is Clear and the lighting is Daylight
    And the road type is Highway with Medium traffic density and Curved road geometry with a curvature of 0.02
    And the ego vehicle is a Sedan in the Center lane, traveling at 27 m/s with an ACC gap of 1.0 second
    And there is a lead vehicle in the Center lane, 60 meters ahead, traveling at 27 m/s and maintaining constant speed along the curved road.
    When the lead vehicle maintains constant speed on a curved road.
    Then the ego vehicle maintains a constant following distance corresponding to the selected ACC gap (1.0 second) while navigating the curved road.

  Scenario: ACC Following - Varying ACC Gap - Lead Vehicle Maintains Speed
    Given the weather is Clear and the lighting is Daylight
    And the road type is Highway with Low traffic density
    And the ego vehicle is a Sedan in the Center lane, traveling at 25 m/s with an ACC gap of 1.0 second
    And there is a lead vehicle in the Center lane, 50 meters ahead, traveling at 25 m/s and maintaining constant speed
    When the ego vehicle ACC gap setting changes during scenario (1.0 -> 1.5 -> 0.8).
    Then the ego vehicle adjusts its following distance smoothly and safely according to the changes in the ACC gap setting.

  Scenario: ACC Following - Snow - Highway - Reduced Friction - Lead Vehicle Brakes Hard
    Given the weather is Snow and the lighting is Daylight
    And the road type is Highway with Low traffic density and Snowy road condition with a friction coefficient of 0.2
    And the ego vehicle is a SUV in the Center lane, traveling at 20 m/s with an ACC gap of 2.0 seconds
    And there is a lead vehicle in the Center lane, 40 meters ahead, traveling at 20 m/s and decelerating to 0 m/s at a rate of 4 m/s^2
    When the lead vehicle brakes hard on a snowy road.
    Then the ego vehicle decelerates, accounting for the reduced friction, to maintain the ACC gap. ABS and ESC systems may activate. Emergency braking may be triggered if a collision is imminent, but should avoid uncontrolled skidding.

