#!/usr/bin/env python3
"""
System Monitoring Script - DevOps Example

This script demonstrates system monitoring techniques crucial for DevOps:
- CPU, memory, disk, and network monitoring
- Process monitoring and management
- System health checks and alerting
- Performance metrics collection
- Resource usage trending

Key Python concepts demonstrated:
- System calls and OS interaction
- Process management with subprocess
- Real-time data collection and monitoring
- Data serialization and storage
- Threading for concurrent monitoring
- Exception handling for system operations
"""

import os
import sys
import time
import json
import psutil
import platform
import subprocess
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import statistics
import signal


@dataclass
class SystemMetrics:
    """System performance metrics snapshot."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_usage: Dict[str, float]
    network_io: Dict[str, int]
    load_average: List[float]
    processes_count: int
    uptime: float


@dataclass
class ProcessInfo:
    """Process information."""
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    memory_rss: int
    status: str
    create_time: float
    cmdline: List[str]


@dataclass
class AlertRule:
    """Alert rule configuration."""
    metric: str
    threshold: float
    comparison: str  # 'gt', 'lt', 'eq'
    duration: int  # seconds
    message: str


class SystemMonitor:
    """Comprehensive system monitoring and alerting."""
    
    def __init__(self, alert_rules: List[AlertRule] = None):
        self.alert_rules = alert_rules or []
        self.metrics_history = []
        self.alert_states = {}
        self.monitoring = False
        self.monitor_thread = None
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\nReceived signal {signum}, shutting down...")
        self.stop_monitoring()
        sys.exit(0)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        try:
            return {
                'platform': platform.platform(),
                'architecture': platform.architecture(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'hostname': platform.node(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'cpu_count': psutil.cpu_count(),
                'cpu_count_logical': psutil.cpu_count(logical=False),
                'memory_total': psutil.virtual_memory().total,
                'disk_partitions': [
                    {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': psutil.disk_usage(partition.mountpoint).total
                    }
                    for partition in psutil.disk_partitions()
                ]
            }
        except Exception as e:
            return {'error': f"Failed to get system info: {e}"}
    
    def get_current_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk usage for all mounted filesystems
            disk_usage = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.mountpoint] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100
                    }
                except PermissionError:
                    # Skip partitions we can't access
                    continue
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Load average (Unix-like systems)
            try:
                load_avg = list(os.getloadavg())
            except (AttributeError, OSError):
                # Windows doesn't have getloadavg
                load_avg = [0.0, 0.0, 0.0]
            
            # Process count
            processes_count = len(psutil.pids())
            
            # System uptime
            uptime = time.time() - psutil.boot_time()
            
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_available=memory.available,
                disk_usage=disk_usage,
                network_io=network_io,
                load_average=load_avg,
                processes_count=processes_count,
                uptime=uptime
            )
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_available=0,
                disk_usage={},
                network_io={},
                load_average=[0.0, 0.0, 0.0],
                processes_count=0,
                uptime=0.0
            )
    
    def get_top_processes(self, count: int = 10, sort_by: str = 'cpu') -> List[ProcessInfo]:
        """Get top processes by CPU or memory usage."""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 
                                       'memory_info', 'status', 'create_time', 'cmdline']):
            try:
                proc_info = ProcessInfo(
                    pid=proc.info['pid'],
                    name=proc.info['name'],
                    cpu_percent=proc.info['cpu_percent'] or 0.0,
                    memory_percent=proc.info['memory_percent'] or 0.0,
                    memory_rss=proc.info['memory_info'].rss if proc.info['memory_info'] else 0,
                    status=proc.info['status'],
                    create_time=proc.info['create_time'],
                    cmdline=proc.info['cmdline'] or []
                )
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Process might have terminated or we don't have permission
                continue
        
        # Sort processes
        if sort_by == 'cpu':
            processes.sort(key=lambda p: p.cpu_percent, reverse=True)
        elif sort_by == 'memory':
            processes.sort(key=lambda p: p.memory_percent, reverse=True)
        
        return processes[:count]
    
    def check_disk_space(self, warning_threshold: float = 80.0, 
                        critical_threshold: float = 90.0) -> List[Dict[str, Any]]:
        """Check disk space usage and return alerts."""
        alerts = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (usage.used / usage.total) * 100
                
                if usage_percent >= critical_threshold:
                    level = 'CRITICAL'
                elif usage_percent >= warning_threshold:
                    level = 'WARNING'
                else:
                    continue
                
                alerts.append({
                    'level': level,
                    'type': 'disk_space',
                    'partition': partition.mountpoint,
                    'usage_percent': usage_percent,
                    'free_bytes': usage.free,
                    'message': f"Disk usage on {partition.mountpoint} is {usage_percent:.1f}%"
                })
                
            except PermissionError:
                continue
        
        return alerts
    
    def check_memory_usage(self, warning_threshold: float = 80.0,
                          critical_threshold: float = 90.0) -> Optional[Dict[str, Any]]:
        """Check memory usage and return alert if needed."""
        memory = psutil.virtual_memory()
        
        if memory.percent >= critical_threshold:
            level = 'CRITICAL'
        elif memory.percent >= warning_threshold:
            level = 'WARNING'
        else:
            return None
        
        return {
            'level': level,
            'type': 'memory_usage',
            'usage_percent': memory.percent,
            'available_bytes': memory.available,
            'message': f"Memory usage is {memory.percent:.1f}%"
        }
    
    def check_cpu_usage(self, warning_threshold: float = 80.0,
                       critical_threshold: float = 90.0, duration: int = 5) -> Optional[Dict[str, Any]]:
        """Check sustained CPU usage over a period."""
        cpu_readings = []
        
        for _ in range(duration):
            cpu_readings.append(psutil.cpu_percent(interval=1))
        
        avg_cpu = statistics.mean(cpu_readings)
        
        if avg_cpu >= critical_threshold:
            level = 'CRITICAL'
        elif avg_cpu >= warning_threshold:
            level = 'WARNING'
        else:
            return None
        
        return {
            'level': level,
            'type': 'cpu_usage',
            'usage_percent': avg_cpu,
            'duration': duration,
            'message': f"CPU usage averaged {avg_cpu:.1f}% over {duration} seconds"
        }
    
    def check_process_health(self, process_names: List[str]) -> List[Dict[str, Any]]:
        """Check if specified processes are running."""
        alerts = []
        running_processes = {proc.name() for proc in psutil.process_iter(['name'])}
        
        for proc_name in process_names:
            if proc_name not in running_processes:
                alerts.append({
                    'level': 'CRITICAL',
                    'type': 'process_down',
                    'process_name': proc_name,
                    'message': f"Process '{proc_name}' is not running"
                })
        
        return alerts
    
    def get_network_connections(self, kind: str = 'inet') -> List[Dict[str, Any]]:
        """Get active network connections."""
        connections = []
        
        try:
            for conn in psutil.net_connections(kind=kind):
                if conn.status == psutil.CONN_ESTABLISHED:
                    connections.append({
                        'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                        'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        'status': conn.status,
                        'pid': conn.pid,
                        'family': conn.family.name if hasattr(conn.family, 'name') else str(conn.family),
                        'type': conn.type.name if hasattr(conn.type, 'name') else str(conn.type)
                    })
        except psutil.AccessDenied:
            print("Access denied when retrieving network connections")
        
        return connections
    
    def run_health_checks(self) -> List[Dict[str, Any]]:
        """Run all health checks and return alerts."""
        alerts = []
        
        # Check disk space
        alerts.extend(self.check_disk_space())
        
        # Check memory usage
        memory_alert = self.check_memory_usage()
        if memory_alert:
            alerts.append(memory_alert)
        
        # Check load average (Unix-like systems)
        try:
            load_avg = os.getloadavg()
            cpu_count = psutil.cpu_count()
            
            if load_avg[0] > cpu_count * 2:  # Load average > 2x CPU count
                alerts.append({
                    'level': 'WARNING',
                    'type': 'high_load',
                    'load_average': load_avg[0],
                    'cpu_count': cpu_count,
                    'message': f"High load average: {load_avg[0]:.2f} (CPUs: {cpu_count})"
                })
        except (AttributeError, OSError):
            pass
        
        return alerts
    
    def save_metrics(self, metrics: SystemMetrics, filename: str = "system_metrics.jsonl"):
        """Save metrics to a JSON Lines file."""
        try:
            with open(filename, 'a') as f:
                json.dump(asdict(metrics), f)
                f.write('\n')
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def start_monitoring(self, interval: int = 60, save_to_file: bool = True):
        """Start continuous system monitoring."""
        if self.monitoring:
            print("Monitoring already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval, save_to_file),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"Started monitoring with {interval}s interval")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Monitoring stopped")
    
    def _monitor_loop(self, interval: int, save_to_file: bool):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                # Collect metrics
                metrics = self.get_current_metrics()
                self.metrics_history.append(metrics)
                
                # Keep only last 100 metrics in memory
                if len(self.metrics_history) > 100:
                    self.metrics_history.pop(0)
                
                # Save to file if requested
                if save_to_file:
                    self.save_metrics(metrics)
                
                # Run health checks
                alerts = self.run_health_checks()
                
                # Print alerts
                for alert in alerts:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"[{timestamp}] {alert['level']}: {alert['message']}")
                
                # Print current status
                print(f"[{metrics.timestamp[:19]}] "
                      f"CPU: {metrics.cpu_percent:.1f}% | "
                      f"Memory: {metrics.memory_percent:.1f}% | "
                      f"Processes: {metrics.processes_count}")
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def generate_report(self, hours: int = 24) -> str:
        """Generate a system performance report."""
        if not self.metrics_history:
            return "No metrics data available for report generation."
        
        # Filter metrics by time range
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            m for m in self.metrics_history
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return f"No metrics data available for the last {hours} hours."
        
        # Calculate statistics
        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        
        report = []
        report.append("=" * 60)
        report.append(f"SYSTEM PERFORMANCE REPORT (Last {hours} hours)")
        report.append("=" * 60)
        report.append("")
        
        report.append("CPU USAGE:")
        report.append(f"  Average: {statistics.mean(cpu_values):.1f}%")
        report.append(f"  Maximum: {max(cpu_values):.1f}%")
        report.append(f"  Minimum: {min(cpu_values):.1f}%")
        report.append("")
        
        report.append("MEMORY USAGE:")
        report.append(f"  Average: {statistics.mean(memory_values):.1f}%")
        report.append(f"  Maximum: {max(memory_values):.1f}%")
        report.append(f"  Minimum: {min(memory_values):.1f}%")
        report.append("")
        
        # Latest metrics
        latest = recent_metrics[-1]
        report.append("CURRENT STATUS:")
        report.append(f"  CPU: {latest.cpu_percent:.1f}%")
        report.append(f"  Memory: {latest.memory_percent:.1f}%")
        report.append(f"  Uptime: {latest.uptime/3600:.1f} hours")
        report.append(f"  Processes: {latest.processes_count}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def demo_system_monitor():
    """Demonstrate system monitoring functionality."""
    print("=== System Monitor Demo ===\n")
    
    monitor = SystemMonitor()
    
    # Show system information
    print("1. System Information:")
    sys_info = monitor.get_system_info()
    for key, value in sys_info.items():
        if key != 'disk_partitions':
            print(f"  {key}: {value}")
    
    print("\n2. Current Metrics:")
    metrics = monitor.get_current_metrics()
    print(f"  CPU Usage: {metrics.cpu_percent:.1f}%")
    print(f"  Memory Usage: {metrics.memory_percent:.1f}%")
    print(f"  Available Memory: {metrics.memory_available / (1024**3):.1f} GB")
    print(f"  Load Average: {metrics.load_average}")
    print(f"  Process Count: {metrics.processes_count}")
    
    print("\n3. Top Processes by CPU:")
    top_processes = monitor.get_top_processes(count=5, sort_by='cpu')
    for i, proc in enumerate(top_processes, 1):
        print(f"  {i}. {proc.name} (PID: {proc.pid}) - CPU: {proc.cpu_percent:.1f}%")
    
    print("\n4. Health Checks:")
    alerts = monitor.run_health_checks()
    if alerts:
        for alert in alerts:
            print(f"  {alert['level']}: {alert['message']}")
    else:
        print("  All systems healthy")
    
    print("\n5. Network Connections:")
    connections = monitor.get_network_connections()
    print(f"  Active connections: {len(connections)}")
    for conn in connections[:3]:  # Show first 3
        print(f"    {conn['local_address']} -> {conn['remote_address']} ({conn['status']})")
    
    print("\n=== Demo Complete ===")
    print("\nTo start continuous monitoring, run:")
    print("  python system_monitor.py --monitor --interval 30")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="System Monitor - Monitor system performance and health")
    parser.add_argument("--monitor", action="store_true", help="Start continuous monitoring")
    parser.add_argument("--interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--duration", type=int, help="Monitoring duration in minutes (default: infinite)")
    parser.add_argument("--report", action="store_true", help="Generate performance report")
    parser.add_argument("--top", action="store_true", help="Show top processes")
    parser.add_argument("--health", action="store_true", help="Run health checks")
    
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    
    if args.monitor:
        print(f"Starting system monitoring (interval: {args.interval}s)")
        monitor.start_monitoring(interval=args.interval)
        
        try:
            if args.duration:
                time.sleep(args.duration * 60)
                monitor.stop_monitoring()
            else:
                # Monitor indefinitely
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
    
    elif args.report:
        print(monitor.generate_report())
    
    elif args.top:
        print("Top processes by CPU usage:")
        processes = monitor.get_top_processes(count=10)
        for i, proc in enumerate(processes, 1):
            print(f"{i:2}. {proc.name:<20} PID: {proc.pid:<8} CPU: {proc.cpu_percent:>6.1f}% Memory: {proc.memory_percent:>6.1f}%")
    
    elif args.health:
        alerts = monitor.run_health_checks()
        if alerts:
            print("System health alerts:")
            for alert in alerts:
                print(f"  {alert['level']}: {alert['message']}")
        else:
            print("All systems healthy")
    
    else:
        # Run demo
        demo_system_monitor()