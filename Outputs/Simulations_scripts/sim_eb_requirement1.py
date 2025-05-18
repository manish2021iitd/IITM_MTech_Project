import carla
import time
import random

def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)
    world = client.load_world('Town03')

    blueprint_library = world.get_blueprint_library()

    # Vehicle and pedestrian blueprints
    vehicle_bp = blueprint_library.filter('vehicle.tesla.model3')[0]
    pedestrian_bp = random.choice(blueprint_library.filter('walker.pedestrian.*'))

    spawn_points = world.get_map().get_spawn_points()
    ego_transform = spawn_points[0]
    pedestrian_transform = carla.Transform(
        location=ego_transform.location + carla.Location(x=20, y=2),
        rotation=carla.Rotation()
    )

    # Spawn ego vehicle
    ego_vehicle = world.spawn_actor(vehicle_bp, ego_transform)
    ego_vehicle.set_autopilot(True)

    # Spawn pedestrian
    pedestrian = world.spawn_actor(pedestrian_bp, pedestrian_transform)

    # Let the simulation stabilize
    time.sleep(2)

    # Move the pedestrian across the road
    walker_controller_bp = blueprint_library.find('controller.ai.walker')
    walker_controller = world.spawn_actor(walker_controller_bp, carla.Transform(), attach_to=pedestrian)
    walker_controller.start()
    walker_controller.go_to_location(ego_transform.location + carla.Location(x=-10, y=-2))
    walker_controller.set_max_speed(1.4)  # meters per second

    # Run simulation for a while to observe emergency braking
    time.sleep(15)

    # Cleanup
    walker_controller.destroy()
    pedestrian.destroy()
    ego_vehicle.destroy()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Simulation interrupted')
