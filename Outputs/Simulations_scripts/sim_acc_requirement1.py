#!/usr/bin/env python

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time
import math

def run_scenario(scenario_number):
    """Runs a specific ACC scenario based on the provided number."""

    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    try:
        # Get the blueprint library and filter for the desired vehicle blueprint
        blueprint_library = world.get_blueprint_library()
        ego_vehicle_bp = blueprint_library.find('vehicle.tesla.model3')  # Changed to Tesla Model3 for better ACC simulation
        lead_vehicle_bp = blueprint_library.find('vehicle.audi.a2') # Changed to Audi A2 for better ACC simulation

        # Define helper function for spawning vehicles at specific locations with initial speed
        def spawn_vehicle(blueprint, initial_transform, initial_speed):
             vehicle = world.spawn_actor(blueprint, initial_transform)
             vehicle.set_simulate_physics(True)
             # Convert km/h to m/s
             initial_velocity = initial_speed * 1000 / 3600
             vehicle.set_target_velocity(carla.Vector3D(initial_velocity, 0, 0))
             return vehicle

        # Define weather presets
        weather_presets = {
            "Clear": carla.WeatherParameters.ClearNoon,
            "Rain": carla.WeatherParameters.WetNoon,
            "Night": carla.WeatherParameters.ClearNight
        }

        # Scenario-specific configurations
        if scenario_number == 1:
            # Scenario 01 - ACC maintains gap in clear weather
            weather = weather_presets["Clear"]
            ego_initial_speed = 65
            lead_initial_speed = 60
            acc_gap = 2.0
            lead_distance_ahead = 100
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)

        elif scenario_number == 2:
            # Scenario 02 - ACC adapts to rain
            weather = weather_presets["Rain"]
            ego_initial_speed = 65
            lead_initial_speed = 60
            acc_gap = 1.5
            lead_distance_ahead = 100
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)

        elif scenario_number == 3:
            # Scenario 03 - ACC adapts to night
            weather = weather_presets["Night"]
            ego_initial_speed = 70
            lead_initial_speed = 65
            acc_gap = 2.5
            lead_distance_ahead = 120
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)

        elif scenario_number == 4:
            # Scenario 04 - ACC in heavy traffic
            weather = weather_presets["Clear"]
            ego_initial_speed = 55
            lead_initial_speed = 50
            acc_gap = 1.0
            lead_distance_ahead = 80
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)

        elif scenario_number == 5:
            # Scenario 05 - Lead vehicle decelerates in clear weather
            weather = weather_presets["Clear"]
            ego_initial_speed = 65
            lead_initial_speed = 70
            acc_gap = 2.0
            lead_distance_ahead = 150
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)
            lead_deceleration = -0.2 * 9.81  # Deceleration at 0.2g in m/s^2

        elif scenario_number == 6:
            # Scenario 06 - Lead vehicle decelerates in rain
            weather = weather_presets["Rain"]
            ego_initial_speed = 65
            lead_initial_speed = 70
            acc_gap = 1.5
            lead_distance_ahead = 150
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)
            lead_deceleration = -0.3 * 9.81  # Deceleration at 0.3g in m/s^2

        elif scenario_number == 7:
            # Scenario 07 - Lead vehicle decelerates at night
            weather = weather_presets["Night"]
            ego_initial_speed = 70
            lead_initial_speed = 75
            acc_gap = 2.5
            lead_distance_ahead = 170
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)
            lead_deceleration = -0.15 * 9.81  # Deceleration at 0.15g in m/s^2

        elif scenario_number == 8:
            # Scenario 08 - Lead vehicle decelerates in heavy traffic
            weather = weather_presets["Clear"]
            ego_initial_speed = 55
            lead_initial_speed = 60
            acc_gap = 1.0
            lead_distance_ahead = 100
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=0, z=0.5)
            lead_deceleration = -0.4 * 9.81  # Deceleration at 0.4g in m/s^2

        elif scenario_number == 9:
            # Scenario 09 - Lead vehicle cuts in from left in clear weather
            weather = weather_presets["Clear"]
            ego_initial_speed = 65
            lead_initial_speed = 60
            acc_gap = 2.0
            lead_distance_ahead = 50
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=-3.5, z=0.5) # Left lane offset
            lane_change = True

        elif scenario_number == 10:
            # Scenario 10 - Lead vehicle cuts in from right in rain
            weather = weather_presets["Rain"]
            ego_initial_speed = 65
            lead_initial_speed = 60
            acc_gap = 1.5
            lead_distance_ahead = 40
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=3.5, z=0.5) # Right lane offset
            lane_change = True

        elif scenario_number == 11:
            # Scenario 11 - Lead vehicle cuts in from left at night
            weather = weather_presets["Night"]
            ego_initial_speed = 70
            lead_initial_speed = 65
            acc_gap = 2.5
            lead_distance_ahead = 60
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=-3.5, z=0.5) # Left lane offset
            lane_change = True

        elif scenario_number == 12:
            # Scenario 12 - Aggressive cut-in in heavy traffic
            weather = weather_presets["Clear"]
            ego_initial_speed = 55
            lead_initial_speed = 50
            acc_gap = 1.0
            lead_distance_ahead = 30
            ego_location = carla.Location(x=10, y=0, z=0.5)
            lead_location = carla.Location(x=ego_location.x + lead_distance_ahead, y=3.5, z=0.5) # Right lane offset
            lane_change = True

        else:
            print("Invalid scenario number")
            return

        # Set weather
        world.set_weather(weather)

        # Spawn vehicles
        ego_start_transform = carla.Transform(ego_location, carla.Rotation(yaw=0))
        lead_start_transform = carla.Transform(lead_location, carla.Rotation(yaw=0))

        ego_vehicle = spawn_vehicle(ego_vehicle_bp, ego_start_transform, ego_initial_speed)
        lead_vehicle = spawn_vehicle(lead_vehicle_bp, lead_start_transform, lead_initial_speed)

        print(f"Ego vehicle spawned at {ego_start_transform}")
        print(f"Lead vehicle spawned at {lead_start_transform}")

        # Add a camera sensor to the ego vehicle (optional)
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))  # Adjust the camera location
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=ego_vehicle)

        # Simulation loop
        simulation_time = 20 # seconds
        frame_rate = 20 # frames per second
        total_frames = simulation_time * frame_rate

        for frame in range(total_frames):
            time.sleep(1/frame_rate)

            # Lead vehicle deceleration scenarios
            if scenario_number in [5, 6, 7, 8]:
                if frame > 5 * frame_rate: # Start deceleration after 5 seconds
                    current_lead_velocity = lead_vehicle.get_velocity()
                    velocity_magnitude = math.sqrt(current_lead_velocity.x**2 + current_lead_velocity.y**2 + current_lead_velocity.z**2)
                    new_velocity = max(0, velocity_magnitude + lead_deceleration / frame_rate) # Ensure velocity doesn't go negative
                    lead_vehicle.set_target_velocity(carla.Vector3D(new_velocity, 0, 0))

            # Lead vehicle lane change scenarios
            if scenario_number in [9, 10, 11, 12]:
                if frame == 5 * frame_rate:  # Start lane change at 5 seconds
                    new_lead_location = lead_vehicle.get_location()
                    new_lead_location.y = 0  # Move to center lane
                    lead_vehicle.set_location(new_lead_location)

            world.tick()

            # Basic logging
            ego_velocity = ego_vehicle.get_velocity()
            lead_velocity = lead_vehicle.get_velocity()
            distance = ego_vehicle.get_location().distance(lead_vehicle.get_location())
            print(f"Frame {frame}: Ego speed = {3.6 * math.sqrt(ego_velocity.x**2 + ego_velocity.y**2 + ego_velocity.z**2):.2f} km/h, Lead speed = {3.6 * math.sqrt(lead_velocity.x**2 + lead_velocity.y**2 + lead_velocity.z**2):.2f} km/h, Distance = {distance:.2f} m")

        print("Scenario completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Cleaning up actors...")
        if 'ego_vehicle' in locals():
            ego_vehicle.destroy()
        if 'lead_vehicle' in locals():
            lead_vehicle.destroy()
        if 'camera' in locals():
            camera.destroy()

if __name__ == '__main__':
    scenario_number = int(input("Enter scenario number (1-12): "))
    run_scenario(scenario_number)
