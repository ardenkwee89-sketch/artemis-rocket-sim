import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon, Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

class SFSStyleRocketSim:
    def __init__(self):
        # Easy to tweak for your real Artemis 2 soda can model!
        self.dry_mass = 2.5      # kg without fuel
        self.fuel_mass = 2.5     # kg
        self.thrust = 120.0      # Newtons (adjust for your engine)
        self.burn_time = 8.0     # seconds
        self.drag_coeff = 0.6
        self.cross_section = 0.04  # m²
        self.g = 9.81
        self.dt = 0.05           # simulation timestep
        
        # For SFS-like feel
        self.rocket_height = 1.2  # visual scale (meters in sim, but visual)
        self.rocket_width = 0.25
        
    def run_simulation(self):
        """Precompute the flight data like SFS physics"""
        mass = self.dry_mass + self.fuel_mass
        height = 0.0
        velocity = 0.0
        time = 0.0
        fuel_left = self.fuel_mass
        
        times = []
        heights = []
        velocities = []
        thrusts = []
        stages = []  # 1 = burning, 2 = coasting
        
        stage = 1
        while time < 60:  # max sim time
            times.append(time)
            heights.append(height)
            velocities.append(velocity)
            stages.append(stage)
            
            if stage == 1 and fuel_left > 0:
                thrust = self.thrust
                fuel_burn_rate = self.fuel_mass / self.burn_time
                fuel_left -= fuel_burn_rate * self.dt
                if fuel_left <= 0:
                    stage = 2  # staging / coast
                    thrust = 0
            else:
                thrust = 0
                stage = 2
            
            thrusts.append(thrust)
            
            # Realistic forces (SFS style)
            rho = 1.225  # air density
            drag = 0.5 * self.drag_coeff * rho * self.cross_section * velocity**2
            if velocity < 0:
                drag = -drag  # drag opposes velocity
            
            weight = mass * self.g
            net_force = thrust - weight - drag
            accel = net_force / mass if mass > 0 else 0
            
            velocity += accel * self.dt
            height += velocity * self.dt
            time += self.dt
            
            if height < 0 and time > 3:
                break  # hit ground
        
        self.data = {
            'times': np.array(times),
            'heights': np.array(heights),
            'velocities': np.array(velocities),
            'thrusts': np.array(thrusts),
            'stages': np.array(stages)
        }
        return self.data
    
    def create_sfs_style_animation(self):
        """Make it look like Spaceflight Simulator - 2D side view flight"""
        data = self.run_simulation()
        
        fig, ax = plt.subplots(figsize=(8, 10))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-0.5, max(data['heights']) * 1.1 + 5)
        ax.set_aspect('equal')
        ax.set_facecolor('#0a1628')  # dark space/sky like SFS
        fig.patch.set_facecolor('#0a1628')
        
        # Ground
        ground = Rectangle((-2, -0.5), 4, 0.5, color='#2d5a27', zorder=1)
        ax.add_patch(ground)
        
        # Simple stars
        np.random.seed(42)
        stars_x = np.random.uniform(-2, 2, 50)
        stars_y = np.random.uniform(5, max(data['heights'])*1.1, 50)
        ax.scatter(stars_x, stars_y, c='white', s=1, alpha=0.6, zorder=0)
        
        # Rocket parts (will be updated)
        rocket_body = FancyBboxPatch((0, 0), self.rocket_width, self.rocket_height, 
                                     boxstyle="round,pad=0.02", 
                                     facecolor='#e0e0e0', edgecolor='#333333', linewidth=2, zorder=5)
        ax.add_patch(rocket_body)
        
        # Nose cone
        nose = Polygon([[0, self.rocket_height], 
                        [self.rocket_width/2, self.rocket_height + 0.35], 
                        [self.rocket_width, self.rocket_height]], 
                       closed=True, facecolor='#c0c0c0', edgecolor='#333', linewidth=1.5, zorder=6)
        ax.add_patch(nose)
        
        # Fins (simple)
        fin_left = Polygon([[-0.05, 0.1], [-0.25, 0.1], [-0.05, 0.4]], 
                           closed=True, facecolor='#555555', zorder=4)
        fin_right = Polygon([[self.rocket_width+0.05, 0.1], 
                             [self.rocket_width+0.25, 0.1], 
                             [self.rocket_width+0.05, 0.4]], 
                            closed=True, facecolor='#555555', zorder=4)
        ax.add_patch(fin_left)
        ax.add_patch(fin_right)
        
        # Flame (multiple lines for SFS engine fire look)
        flame_lines = []
        for i in range(5):
            line, = ax.plot([], [], color='#ffaa00', linewidth=3, alpha=0.8, zorder=3)
            flame_lines.append(line)
        
        # Trajectory trail (SFS style path)
        trail, = ax.plot([], [], color='#00ffcc', linewidth=1.5, alpha=0.7, zorder=2)
        
        # Info text box (like SFS HUD)
        info_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                            fontsize=11, color='white', 
                            verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='#112244', alpha=0.85),
                            family='monospace')
        
        ax.set_title('🚀 Artemis-Style Rocket • SFS Inspired Physics Sim', color='white', fontsize=14, pad=10)
        ax.set_xlabel('Horizontal (m)', color='white')
        ax.set_ylabel('Altitude (m)', color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        
        def update(frame):
            if frame >= len(data['heights']):
                return
            
            h = data['heights'][frame]
            v = data['velocities'][frame]
            t = data['times'][frame]
            thrust = data['thrusts'][frame]
            stage = data['stages'][frame]
            
            # Update rocket position (centered horizontally)
            x_center = 0
            y_bottom = h
            
            # Move rocket body
            rocket_body.set_xy((x_center - self.rocket_width/2, y_bottom))
            
            # Move nose
            nose.set_xy([[x_center - self.rocket_width/2, y_bottom + self.rocket_height],
                         [x_center, y_bottom + self.rocket_height + 0.35],
                         [x_center + self.rocket_width/2, y_bottom + self.rocket_height]])
            
            # Move fins
            fin_left.set_xy([[x_center - self.rocket_width/2 - 0.05, y_bottom + 0.1],
                             [x_center - self.rocket_width/2 - 0.25, y_bottom + 0.1],
                             [x_center - self.rocket_width/2 - 0.05, y_bottom + 0.4]])
            fin_right.set_xy([[x_center + self.rocket_width/2 + 0.05, y_bottom + 0.1],
                              [x_center + self.rocket_width/2 + 0.25, y_bottom + 0.1],
                              [x_center + self.rocket_width/2 + 0.05, y_bottom + 0.4]])
            
            # Flame effect (only when thrusting, SFS style)
            if thrust > 0:
                flame_length = 0.4 + 0.3 * np.sin(frame * 0.8)  # flicker
                for i, line in enumerate(flame_lines):
                    offset = (i - 2) * 0.04
                    x_flame = [x_center + offset, x_center + offset]
                    y_flame = [y_bottom, y_bottom - flame_length * (0.7 + 0.3*np.random.random())]
                    line.set_data(x_flame, y_flame)
                    line.set_alpha(0.7 + 0.3*np.random.random())
            else:
                for line in flame_lines:
                    line.set_data([], [])
            
            # Update trail (SFS path)
            trail.set_data(data['heights'][:frame+1]*0 + 0, data['heights'][:frame+1])  # vertical line at x=0 for simplicity, or make curved if wanted
            
            # HUD text like SFS
            stage_name = "BOOSTER BURN" if stage == 1 else "COASTING"
            info_str = (f"Time: {t:.1f}s\n"
                       f"Altitude: {h:.1f} m\n"
                       f"Velocity: {v:.1f} m/s\n"
                       f"Stage: {stage_name}\n"
                       f"Thrust: {thrust:.0f} N")
            info_text.set_text(info_str)
            
            return [rocket_body, nose, fin_left, fin_right, trail] + flame_lines + [info_text]
        
        ani = FuncAnimation(fig, update, frames=len(data['heights']), 
                            interval=50, blit=False, repeat=False)
        
        plt.tight_layout()
        plt.show()
        
        print("🚀 SFS-style animation ready!")
        print(f"Max altitude: {max(data['heights']):.1f} m")
        print(f"Max speed: {max(data['velocities']):.1f} m/s")
        print("\nTweak the numbers in __init__ to match your real rocket model!")

# Run it
if __name__ == "__main__":
    sim = SFSStyleRocketSim()
    sim.create_sfs_style_animation()