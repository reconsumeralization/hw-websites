import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
from pathlib import Path
import threading
import queue
import time
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from typing import Dict, Any

class DeploymentVisualizer:
    def __init__(self, frame):
        self.frame = frame
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Store node data for interaction
        self.node_positions = {}
        self.node_details = {}
        self.current_animation = None

        # Connect click event
        self.canvas.mpl_connect('button_press_event', self.on_click)

        # Create details panel
        self.create_details_panel()

    def create_details_panel(self):
        """Create panel for displaying node details"""
        self.details_frame = ttk.LabelFrame(self.frame, text="Component Details", padding=10)
        self.details_frame.pack(fill=tk.X, pady=5)

        self.details_text = scrolledtext.ScrolledText(self.details_frame, height=4)
        self.details_text.pack(fill=tk.X)

    def on_click(self, event):
        """Handle click events on nodes"""
        if event.inaxes != self.ax:
            return

        # Find closest node to click
        click_pos = (event.xdata, event.ydata)
        closest_node = None
        min_dist = float('inf')

        for node, pos in self.node_positions.items():
            dist = ((pos[0] - click_pos[0])**2 + (pos[1] - click_pos[1])**2)**0.5
            if dist < min_dist and dist < 0.1:  # Threshold for clicking
                min_dist = dist
                closest_node = node

        if closest_node:
            self.show_node_details(closest_node)

    def show_node_details(self, node: str):
        """Display details for selected node"""
        details = self.node_details.get(node, {})

        # Format details text
        text = f"Component: {node}\n"
        text += f"Status: {details.get('status', 'Unknown')}\n"
        text += f"Last Updated: {details.get('last_updated', 'Unknown')}\n"

        if 'metrics' in details:
            text += "\nMetrics:\n"
            for key, value in details['metrics'].items():
                text += f"  {key}: {value}\n"

        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, text)

    def animate_deployment(self, node: str):
        """Animate deployment progress for a node"""
        if self.current_animation:
            self.current_animation.event_source.stop()

        circle = Circle((0, 0), 0.1, color='blue', alpha=0.3)
        self.ax.add_patch(circle)

        def update(frame):
            circle.set_radius(0.1 + frame * 0.02)
            circle.set_alpha(0.3 - frame * 0.02)
            return circle,

        self.current_animation = FuncAnimation(
            self.fig, update, frames=15, interval=50, blit=True
        )
        self.canvas.draw()

    def update_visualization(self, deployment_data: Dict[str, Any]):
        """Update the deployment visualization"""
        self.ax.clear()
        G = nx.Graph()

        colors = []
        sizes = []
        labels = {}
        status_indicators = []

        # Add nodes and collect their data
        for site, data in deployment_data.items():
            # Site nodes
            G.add_node(site, type='site')
            status = data.get('status', 'unknown')
            colors.append(self.get_status_color(status))
            sizes.append(3000)
            labels[site] = site
            self.node_details[site] = {
                'status': status,
                'last_updated': data.get('last_updated', 'Unknown'),
                'metrics': {
                    'uptime': data.get('uptime', 'Unknown'),
                    'response_time': data.get('response_time', 'Unknown')
                }
            }

            # City nodes
            for city in data['cities']:
                city_node = f"{city}_{site}"
                G.add_node(city_node, type='city')
                G.add_edge(site, city_node)
                city_status = data.get('city_status', {}).get(city, 'unknown')
                colors.append(self.get_status_color(city_status))
                sizes.append(2000)
                labels[city_node] = city
                self.node_details[city_node] = {
                    'status': city_status,
                    'last_updated': data.get('last_updated', 'Unknown'),
                    'metrics': {
                        'pages_deployed': data.get('pages_deployed', {}).get(city, 0),
                        'total_pages': data.get('total_pages', {}).get(city, 0)
                    }
                }

        # Draw the graph
        pos = nx.spring_layout(G)
        self.node_positions = pos

        # Draw nodes with status indicators
        nx.draw(G, pos,
                node_color=colors,
                node_size=sizes,
                labels=labels,
                font_size=8,
                font_weight='bold',
                ax=self.ax)

        # Add resource usage indicators
        for node, (x, y) in pos.items():
            if node in self.node_details:
                metrics = self.node_details[node].get('metrics', {})
                if 'cpu_usage' in metrics:
                    self.add_resource_indicator(x, y, metrics['cpu_usage'], 'CPU')
                if 'memory_usage' in metrics:
                    self.add_resource_indicator(x, y - 0.1, metrics['memory_usage'], 'MEM')

        # Add legend
        self.add_legend()

        self.canvas.draw()

    def get_status_color(self, status: str) -> str:
        """Get color based on status"""
        colors = {
            'active': 'lightgreen',
            'deploying': 'yellow',
            'error': 'red',
            'inactive': 'gray',
            'unknown': 'lightgray'
        }
        return colors.get(status, 'lightgray')

    def add_resource_indicator(self, x: float, y: float, value: float, label: str):
        """Add resource usage indicator"""
        width = 0.1
        height = value / 100 * 0.1
        self.ax.add_patch(plt.Rectangle(
            (x - width/2, y - height/2),
            width, height,
            color=self.get_resource_color(value)
        ))
        self.ax.text(x, y, f"{label}: {value}%",
                    horizontalalignment='center',
                    verticalalignment='bottom',
                    fontsize=6)

    def get_resource_color(self, value: float) -> str:
        """Get color based on resource usage value"""
        if value < 60:
            return 'green'
        elif value < 80:
            return 'yellow'
        else:
            return 'red'

    def add_legend(self):
        """Add legend with status and resource indicators"""
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w',
                      markerfacecolor=color, markersize=10,
                      label=status)
            for status, color in [
                ('Active', 'lightgreen'),
                ('Deploying', 'yellow'),
                ('Error', 'red'),
                ('Inactive', 'gray')
            ]
        ]
        self.ax.legend(handles=legend_elements, loc='upper left')

class ProjectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HW Websites Manager")
        self.root.geometry("1200x800")

        # Create queue for log messages
        self.log_queue = queue.Queue()

        # Create main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and pack components
        self.create_control_panel()
        self.create_monitor_panel()
        self.create_log_panel()
        self.create_deployment_panel()

        # Start monitoring thread
        self.monitoring = False
        self.monitor_thread = None

        # Configure styles
        self.configure_styles()

        # Start log queue processing
        self.process_log_queue()

        # Start periodic updates
        self.update_deployment_status()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('Action.TButton', padding=10, font=('Helvetica', 10, 'bold'))
        style.configure('Monitor.TFrame', relief='solid', borderwidth=1)
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))

    def create_control_panel(self):
        # Control Panel
        control_frame = ttk.LabelFrame(self.main_container, text="Control Panel", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        # Project Controls
        project_controls = ttk.Frame(control_frame)
        project_controls.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(project_controls, text="Initialize Project",
                  command=lambda: self.run_command('init'),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(project_controls, text="Clean Project",
                  command=lambda: self.run_command('clean'),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(project_controls, text="Reset Project",
                  command=lambda: self.run_command('reset'),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        # Backup Controls
        backup_controls = ttk.Frame(control_frame)
        backup_controls.pack(fill=tk.X, pady=(0, 10))

        self.backup_name = ttk.Entry(backup_controls)
        self.backup_name.pack(side=tk.LEFT, padx=5)

        ttk.Button(backup_controls, text="Create Backup",
                  command=self.create_backup,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(backup_controls, text="Restore Backup",
                  command=self.restore_backup,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(backup_controls, text="List Backups",
                  command=lambda: self.run_command('list'),
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

        # Deployment Controls
        deploy_controls = ttk.Frame(control_frame)
        deploy_controls.pack(fill=tk.X)

        self.environment_var = tk.StringVar(value='staging')
        ttk.Radiobutton(deploy_controls, text="Staging",
                       variable=self.environment_var,
                       value='staging').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(deploy_controls, text="Production",
                       variable=self.environment_var,
                       value='production').pack(side=tk.LEFT, padx=5)

        ttk.Button(deploy_controls, text="Deploy",
                  command=self.deploy,
                  style='Action.TButton').pack(side=tk.LEFT, padx=5)

    def create_monitor_panel(self):
        # Monitor Panel
        monitor_frame = ttk.LabelFrame(self.main_container, text="System Monitor", padding=10)
        monitor_frame.pack(fill=tk.X, pady=(0, 10))

        # CPU and Memory Meters
        meters_frame = ttk.Frame(monitor_frame)
        meters_frame.pack(fill=tk.X)

        # CPU Meter
        cpu_frame = ttk.Frame(meters_frame)
        cpu_frame.pack(side=tk.LEFT, expand=True, padx=10)

        ttk.Label(cpu_frame, text="CPU Usage", style='Header.TLabel').pack()
        self.cpu_meter = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_meter.pack()
        self.cpu_label = ttk.Label(cpu_frame, text="0%")
        self.cpu_label.pack()

        # Memory Meter
        mem_frame = ttk.Frame(meters_frame)
        mem_frame.pack(side=tk.LEFT, expand=True, padx=10)

        ttk.Label(mem_frame, text="Memory Usage", style='Header.TLabel').pack()
        self.mem_meter = ttk.Progressbar(mem_frame, length=200, mode='determinate')
        self.mem_meter.pack()
        self.mem_label = ttk.Label(mem_frame, text="0%")
        self.mem_label.pack()

        # Monitor Controls
        control_frame = ttk.Frame(monitor_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))

        self.monitor_button = ttk.Button(control_frame,
                                       text="Start Monitoring",
                                       command=self.toggle_monitoring,
                                       style='Action.TButton')
        self.monitor_button.pack(side=tk.LEFT, padx=5)

    def create_log_panel(self):
        # Log Panel
        log_frame = ttk.LabelFrame(self.main_container, text="Log Output", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)

        # Log Text Area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Clear Log Button
        ttk.Button(log_frame, text="Clear Log",
                  command=self.clear_log,
                  style='Action.TButton').pack(pady=(10, 0))

    def create_deployment_panel(self):
        """Create deployment visualization panel"""
        deployment_frame = ttk.LabelFrame(self.main_container, text="Deployment Status", padding=10)
        deployment_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.deployment_viz = DeploymentVisualizer(deployment_frame)

    def run_command(self, command, *args):
        def run():
            try:
                result = subprocess.run(['python', 'scripts/control.py', command, *args],
                                     capture_output=True, text=True)
                self.log_queue.put(result.stdout)
                if result.stderr:
                    self.log_queue.put(f"Error: {result.stderr}")
            except Exception as e:
                self.log_queue.put(f"Error executing command: {str(e)}")

        thread = threading.Thread(target=run)
        thread.start()

    def create_backup(self):
        name = self.backup_name.get()
        if name:
            self.run_command('backup', '--name', name)
        else:
            messagebox.showwarning("Warning", "Please enter a backup name")

    def restore_backup(self):
        name = self.backup_name.get()
        if name:
            if messagebox.askyesno("Confirm Restore",
                                 f"Are you sure you want to restore backup '{name}'?"):
                self.run_command('restore', '--name', name)
        else:
            messagebox.showwarning("Warning", "Please enter a backup name")

    def deploy(self):
        env = self.environment_var.get()
        if messagebox.askyesno("Confirm Deploy",
                             f"Are you sure you want to deploy to {env}?"):
            self.run_command('deploy', '--env', env)

    def toggle_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.monitor_button.configure(text="Stop Monitoring")
            self.monitor_thread = threading.Thread(target=self.monitor_resources)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
        else:
            self.monitoring = False
            self.monitor_button.configure(text="Start Monitoring")

    def monitor_resources(self):
        import psutil
        while self.monitoring:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent

            self.cpu_meter['value'] = cpu
            self.cpu_label['text'] = f"{cpu}%"

            self.mem_meter['value'] = mem
            self.mem_label['text'] = f"{mem}%"

            time.sleep(1)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def process_log_queue(self):
        while True:
            try:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
            except queue.Empty:
                break

        self.root.after(100, self.process_log_queue)

    def update_deployment_status(self):
        """Update deployment status visualization"""
        try:
            # Read current deployment status
            with open('data/deployment_status.json', 'r') as f:
                deployment_data = json.load(f)
        except FileNotFoundError:
            deployment_data = {
                'hwroads.com': {
                    'cities': ['Miami', 'Fort Lauderdale', 'West Palm Beach'],
                    'status': 'active'
                },
                'hwasphaltfl.com': {
                    'cities': ['Orlando', 'Tampa', 'Jacksonville'],
                    'status': 'active'
                }
            }

        # Update visualization
        self.deployment_viz.update_visualization(deployment_data)

        # Schedule next update
        self.root.after(5000, self.update_deployment_status)  # Update every 5 seconds

def main():
    root = tk.Tk()
    app = ProjectGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
