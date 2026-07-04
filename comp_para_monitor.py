import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk
import psutil

class SystemResourceDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("System Core: Hardware Telemetry Matrix")
        self.root.geometry("600x420")
        self.root.configure(bg="#1e1e2e")
        
        self.is_monitoring = True

        # --- Sleek UI Styling Grid ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TProgressbar", thickness=18, troughcolor="#313244", borderwidth=0)
        self.style.map("TProgressbar", background=[("active", "#89b4fa")])
        
        # 👤 Header Status Panel
        header_frame = tk.Frame(self.root, bg="#313244", height=50)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        lbl_title = tk.Label(header_frame, text="⚡ LIVE HARDWARE KERNEL METRICS", font=("Arial", 11, "bold"), fg="#a6e3a1", bg="#313244")
        lbl_title.pack(side=tk.LEFT, padx=15, pady=12)
        
        self.lbl_status = tk.Label(header_frame, text="OS Kernel Linked", font=("Arial", 9, "italic"), fg="#bac2de", bg="#313244")
        self.lbl_status.pack(side=tk.RIGHT, padx=15, pady=12)

        # 📊 Main Resource Metric Display Container
        main_container = tk.Frame(self.root, bg="#1e1e2e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # --- Metric 1: CPU Utilization ---
        cpu_frame = tk.Frame(main_container, bg="#1e1e2e")
        cpu_frame.pack(fill=tk.X, pady=10)
        
        self.lbl_cpu_title = tk.Label(cpu_frame, text="🧠 CPU Core Utilization: Checking...", font=("Arial", 10, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        self.lbl_cpu_title.pack(anchor="w", pady=(0, 2))
        
        self.progress_cpu = ttk.Progressbar(cpu_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_cpu.pack(fill=tk.X)

        # --- Metric 2: Virtual RAM Allocation ---
        ram_frame = tk.Frame(main_container, bg="#1e1e2e")
        ram_frame.pack(fill=tk.X, pady=10)
        
        self.lbl_ram_title = tk.Label(ram_frame, text="💾 Virtual RAM Footprint: Checking...", font=("Arial", 10, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        self.lbl_ram_title.pack(anchor="w", pady=(0, 2))
        
        self.progress_ram = ttk.Progressbar(ram_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_ram.pack(fill=tk.X)

        # --- Metric 3: Disk Partition Capacity ---
        disk_frame = tk.Frame(main_container, bg="#1e1e2e")
        disk_frame.pack(fill=tk.X, pady=10)
        
        self.lbl_disk_title = tk.Label(disk_frame, text="🗄️ Primary Storage (C:): Checking...", font=("Arial", 10, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        self.lbl_disk_title.pack(anchor="w", pady=(0, 2))
        
        self.progress_disk = ttk.Progressbar(disk_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_disk.pack(fill=tk.X)

        # Close Window Gracefully handling thread cleanup strings
        self.root.protocol("WM_DELETE_WINDOW", self._on_close_event)

        # 🚀 Spin up asynchronous background hardware worker thread
        self.worker_thread = threading.Thread(target=self._hardware_scanner_worker, daemon=True)
        self.worker_thread.start()

    def _hardware_scanner_worker(self):
        """Queries hardware usage configurations directly from the system kernel matrix."""
        while self.is_monitoring:
            # 1. Capture fractional CPU changes over a 0.5s interval window
            cpu_usage = psutil.cpu_percent(interval=0.5)
            
            # 2. Extract memory metrics map data
            ram_metrics = psutil.virtual_memory()
            ram_usage = ram_metrics.percent
            ram_used_gb = ram_metrics.used / (1024 ** 3)
            ram_total_gb = ram_metrics.total / (1024 ** 3)
            
            # 3. Read physical drive arrays partition storage sectors
            disk_metrics = psutil.disk_usage('/')
            disk_usage = disk_metrics.percent
            disk_used_gb = disk_metrics.used / (1024 ** 3)
            disk_total_gb = disk_metrics.total / (1024 ** 3)

            # Safely push update commands back to the main UI window frame objects
            self.root.after(0, self._update_dashboard_display, cpu_usage, ram_usage, ram_used_gb, ram_total_gb, disk_usage, disk_used_gb, disk_total_gb)
            
            # Throttle collection pacing loop slightly to balance background context switching
            time.sleep(0.5)

    def _update_dashboard_display(self, cpu, ram_p, ram_u, ram_t, disk_p, disk_u, disk_t):
        """Updates UI elements and text formats dynamically."""
        # Update CPU Elements
        self.lbl_cpu_title.config(text=f"🧠 CPU Core Utilization: {cpu}%")
        self.progress_cpu['value'] = cpu
        
        # Update RAM Elements
        self.lbl_ram_title.config(text=f"💾 Virtual RAM Footprint: {ram_p}% ({ram_u:.1f} GB / {ram_t:.1f} GB)")
        self.progress_ram['value'] = ram_p
        
        # Update Disk Elements
        self.lbl_disk_title.config(text=f"🗄️ Primary Storage (C:): {disk_p}% ({disk_u:.0f} GB / {disk_t:.0f} GB)")
        self.progress_disk['value'] = disk_p
        
        # Dynamically change status bar text to reflect loading strain states
        if cpu > 80 or ram_p > 85:
            self.lbl_status.config(text="⚠️ Heavy System Strain", fg="#f38ba8")
        else:
            self.lbl_status.config(text="🟢 Performance Optimal", fg="#a6e3a1")

    def _on_close_event(self):
        self.is_monitoring = False
        self.root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemResourceDashboard(root)
    root.mainloop()
