import math

def rocket_simulator(initial_mass, fuel_mass, thrust, burn_time, stages=1):
    '''Simple rocket simulator using basic physics.'''
    g = 9.81  # gravity m/s²
    velocity = 0
    altitude = 0
    mass = initial_mass
    
    print(f'Simulating {stages}-stage rocket...')
    for stage in range(1, stages + 1):
        print(f'Stage {stage} burning...')
        dt = 0.1  # time step
        for t in range(int(burn_time / dt)):
            thrust_force = thrust
            weight = mass * g
            net_force = thrust_force - weight
            acceleration = net_force / mass
            velocity += acceleration * dt
            altitude += velocity * dt
            mass -= fuel_mass / burn_time * dt  # fuel consumption
            if mass <= 0:
                break
        if stage < stages:
            print('Stage separation!')
    
    print(f'Final altitude: {altitude:.2f} m')
    print(f'Final velocity: {velocity:.2f} m/s')
    return altitude, velocity

# Example for Artemis-like rocket
if __name__ == '__main__':
    # Rough Artemis 2 params (simplified)
    result = rocket_simulator(
        initial_mass=100000,  # kg
        fuel_mass=50000,
        thrust=2000000,  # Newtons
        burn_time=120,   # seconds
        stages=2
    )
    print('Simulation complete!')