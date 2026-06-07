import numpy as np
import matplotlib.pyplot as plt

class RocketSimulator:
    def __init__(self):
        # Rocket parameters - tweak these for your Artemis 2 model!
        self.mass = 5.0  # kg (initial mass, including fuel)
        self.fuel_mass = 2.5  # kg
        self.thrust = 100.0  # Newtons
        self.burn_time = 10.0  # seconds
        self.drag_coeff = 0.5
        self.area = 0.05  # m²
        self.g = 9.81  # m/s²
        
    def simulate(self, dt=0.1):
        t = 0
        height = 0
        velocity = 0
        mass = self.mass
        times = []
        heights = []
        velocities = []
        
        while height >= 0 or t < self.burn_time + 20:
            times.append(t)
            heights.append(height)
            velocities.append(velocity)
            
            # Thrust phase
            if t < self.burn_time and mass > self.mass - self.fuel_mass:
                thrust = self.thrust
                mass -= (self.fuel_mass / self.burn_time) * dt
            else:
                thrust = 0
            
            # Forces
            drag = 0.5 * self.drag_coeff * 1.225 * self.area * velocity**2  # air density approx
            net_force = thrust - mass * self.g - drag * (1 if velocity > 0 else -1)
            accel = net_force / mass if mass > 0 else 0
            
            velocity += accel * dt
            height += velocity * dt
            t += dt
            
            if height < 0 and t > 5:
                break
        
        return times, heights, velocities

# Run sim
sim = RocketSimulator()
times, heights, vels = sim.simulate()

print("Max height:", max(heights), "meters")
print("Max velocity:", max(vels), "m/s")

# Plot
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(times, heights)
plt.ylabel('Height (m)')
plt.title('Rocket Trajectory Simulation')
plt.subplot(2,1,2)
plt.plot(times, vels)
plt.ylabel('Velocity (m/s)')
plt.xlabel('Time (s)')
plt.grid(True)
plt.show()