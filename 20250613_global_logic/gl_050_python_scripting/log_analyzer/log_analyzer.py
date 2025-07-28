#!/usr/bin/env python3
"""
Log Analyzer with Regex Processing - DevOps Example

This script demonstrates log analysis techniques essential for DevOps:
- Parsing various log formats (Apache, Nginx, Application logs)
- Extracting metrics and patterns using regex
- Real-time log monitoring and alerting
- Statistical analysis of log data
- Error pattern detection and reporting

Key Python concepts demonstrated:
- Regular expressions (re module)
- Data processing with collections
- Statistical analysis with basic math
- File I/O with generators for large files
- Date/time parsing and manipulation
- Data structures (defaultdict, Counter)
"""

import re
import os
import json
import gzip
from datetime import datetime, timedelta
from collections import defaultdict, Counter, namedtuple
from typing import Dict, List, Iterator, Optional, Tuple, Any
from pathlib import Path
import statistics
from dataclasses import dataclass
import argparse


@dataclass
class LogEntry:
    """Structured representation of a log entry."""
    timestamp: datetime
    level: str
    message: str
    source: str
    ip_address: Optional[str] = None
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    user_agent: Optional[str] = None


@dataclass
class LogStats:
    """Statistics collected from log analysis."""
    total_entries: int
    error_count: int
    warning_count: int
    unique_ips: int
    avg_response_time: float
    top_errors: List[Tuple[str, int]]
    top_ips: List[Tuple[str, int]]
    time_range: Tuple[datetime, datetime]


class LogPatterns:
    """Common log format patterns using regex."""
    
    # Apache/Nginx Combined Log Format
    APACHE_COMBINED = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<path>[^\s]*) (?P<protocol>[^"]*)" '
        r'(?P<status>\d+) (?P<size>\d+|-) '
        r'"(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
    )
    
    # Application Log Pattern (common format: timestamp level message)
    APPLICATION_LOG = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[\.\d]*) '
        r'\[(?P<level>\w+)\] '
        r'(?P<message>.*)'
    )
    
    # Syslog Pattern
    SYSLOG = re.compile(
        r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) '
        r'(?P<hostname>\S+) '
        r'(?P<process>\S+): '
        r'(?P<message>.*)'
    )
    
    # Docker Log Pattern
    DOCKER_LOG = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z) '
        r'(?P<stream>stdout|stderr) F '
        r'(?P<message>.*)'
    )
    
    # Nginx Error Log
    NGINX_ERROR = re.compile(
        r'(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}) '
        r'\[(?P<level>\w+)\] '
        r'(?P<pid>\d+)#(?P<tid>\d+): '
        r'\*(?P<connection>\d+) '
        r'(?P<message>.*)'
    )
    
    # Error patterns for alerting
    ERROR_PATTERNS = [
        re.compile(r'(error|ERROR|Error)', re.IGNORECASE),
        re.compile(r'(exception|Exception|EXCEPTION)', re.IGNORECASE),
        re.compile(r'(failed|Failed|FAILED)', re.IGNORECASE),
        re.compile(r'(timeout|Timeout|TIMEOUT)', re.IGNORECASE),
        re.compile(r'(critical|Critical|CRITICAL)', re.IGNORECASE),
        re.compile(r'(fatal|Fatal|FATAL)', re.IGNORECASE),
    ]
    
    # Performance issue patterns
    PERFORMANCE_PATTERNS = [
        re.compile(r'slow\s+query', re.IGNORECASE),
        re.compile(r'high\s+memory', re.IGNORECASE),
        re.compile(r'cpu\s+usage', re.IGNORECASE),
        re.compile(r'response\s+time.*(\d+)ms', re.IGNORECASE),
    ]


class LogAnalyzer:
    """Comprehensive log analyzer with pattern matching and statistics."""
    
    def __init__(self):
        self.patterns = LogPatterns()
        self.stats = defaultdict(int)
        self.error_messages = Counter()
        self.ip_addresses = Counter()
        self.response_times = []
        self.log_entries = []
    
    def parse_timestamp(self, timestamp_str: str, format_patterns: List[str]) -> Optional[datetime]:
        """Parse timestamp string using multiple format patterns."""
        timestamp_formats = format_patterns or [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%d/%b/%Y:%H:%M:%S %z',
            '%b %d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y/%m/%d %H:%M:%S'
        ]
        
        for fmt in timestamp_formats:
            try:
                return datetime.strptime(timestamp_str.strip(), fmt)
            except ValueError:
                continue
        
        # Try parsing common variations
        try:
            # Remove timezone info if present
            clean_timestamp = re.sub(r'\s*[+-]\d{4}$', '', timestamp_str.strip())
            return datetime.strptime(clean_timestamp, '%d/%b/%Y:%H:%M:%S')
        except ValueError:
            pass
        
        return None
    
    def parse_log_line(self, line: str, log_format: str = 'auto') -> Optional[LogEntry]:
        """Parse a single log line based on detected or specified format."""
        line = line.strip()
        if not line:
            return None
        
        # Auto-detect format if not specified
        if log_format == 'auto':
            log_format = self.detect_log_format(line)
        
        if log_format == 'apache':
            return self._parse_apache_log(line)
        elif log_format == 'application':
            return self._parse_application_log(line)
        elif log_format == 'syslog':
            return self._parse_syslog(line)
        elif log_format == 'docker':
            return self._parse_docker_log(line)
        elif log_format == 'nginx_error':
            return self._parse_nginx_error_log(line)
        else:
            # Fallback: treat as plain text with basic parsing
            return self._parse_generic_log(line)
    
    def detect_log_format(self, line: str) -> str:
        """Auto-detect log format based on line structure."""
        if self.patterns.APACHE_COMBINED.match(line):
            return 'apache'
        elif self.patterns.APPLICATION_LOG.match(line):
            return 'application'
        elif self.patterns.SYSLOG.match(line):
            return 'syslog'
        elif self.patterns.DOCKER_LOG.match(line):
            return 'docker'
        elif self.patterns.NGINX_ERROR.match(line):
            return 'nginx_error'
        else:
            return 'generic'
    
    def _parse_apache_log(self, line: str) -> Optional[LogEntry]:
        """Parse Apache/Nginx combined log format."""
        match = self.patterns.APACHE_COMBINED.match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        timestamp = self.parse_timestamp(groups['timestamp'], ['%d/%b/%Y:%H:%M:%S %z'])
        
        return LogEntry(
            timestamp=timestamp or datetime.now(),
            level='INFO',
            message=f"{groups['method']} {groups['path']} {groups['protocol']}",
            source='apache',
            ip_address=groups['ip'],
            status_code=int(groups['status']),
            user_agent=groups['user_agent']
        )
    
    def _parse_application_log(self, line: str) -> Optional[LogEntry]:
        """Parse application log format."""
        match = self.patterns.APPLICATION_LOG.match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        timestamp = self.parse_timestamp(groups['timestamp'], None)
        
        return LogEntry(
            timestamp=timestamp or datetime.now(),
            level=groups['level'].upper(),
            message=groups['message'],
            source='application'
        )
    
    def _parse_syslog(self, line: str) -> Optional[LogEntry]:
        """Parse syslog format."""
        match = self.patterns.SYSLOG.match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        # Syslog typically doesn't include year, so we assume current year
        current_year = datetime.now().year
        timestamp_str = f"{current_year} {groups['timestamp']}"
        timestamp = self.parse_timestamp(timestamp_str, ['%Y %b %d %H:%M:%S'])
        
        return LogEntry(
            timestamp=timestamp or datetime.now(),
            level='INFO',
            message=groups['message'],
            source=groups['process']
        )
    
    def _parse_docker_log(self, line: str) -> Optional[LogEntry]:
        """Parse Docker log format."""
        match = self.patterns.DOCKER_LOG.match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        timestamp = self.parse_timestamp(groups['timestamp'], ['%Y-%m-%dT%H:%M:%S.%fZ'])
        
        level = 'ERROR' if groups['stream'] == 'stderr' else 'INFO'
        
        return LogEntry(
            timestamp=timestamp or datetime.now(),
            level=level,
            message=groups['message'],
            source='docker'
        )
    
    def _parse_nginx_error_log(self, line: str) -> Optional[LogEntry]:
        """Parse Nginx error log format."""
        match = self.patterns.NGINX_ERROR.match(line)
        if not match:
            return None
        
        groups = match.groupdict()
        timestamp = self.parse_timestamp(groups['timestamp'], ['%Y/%m/%d %H:%M:%S'])
        
        return LogEntry(
            timestamp=timestamp or datetime.now(),
            level=groups['level'].upper(),
            message=groups['message'],
            source='nginx'
        )
    
    def _parse_generic_log(self, line: str) -> LogEntry:
        """Fallback parser for unrecognized log formats."""
        # Try to extract timestamp from beginning of line
        timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})', line)
        
        if timestamp_match:
            timestamp = self.parse_timestamp(timestamp_match.group(1), None)
            message = line[len(timestamp_match.group(1)):].strip()
        else:
            timestamp = datetime.now()
            message = line
        
        # Detect log level in the message
        level = 'INFO'
        for pattern in ['ERROR', 'WARN', 'DEBUG', 'FATAL', 'TRACE']:
            if pattern in message.upper():
                level = pattern
                break
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            source='generic'
        )
    
    def read_log_file(self, file_path: str, max_lines: Optional[int] = None) -> Iterator[LogEntry]:
        """Read and parse log file, supporting gzipped files."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        
        # Determine if file is gzipped
        open_func = gzip.open if path.suffix == '.gz' else open
        mode = 'rt' if path.suffix == '.gz' else 'r'
        
        line_count = 0
        with open_func(file_path, mode, encoding='utf-8', errors='ignore') as f:
            for line in f:
                if max_lines and line_count >= max_lines:
                    break
                
                entry = self.parse_log_line(line)
                if entry:
                    yield entry
                    line_count += 1
    
    def analyze_logs(self, file_paths: List[str], max_lines_per_file: Optional[int] = None) -> LogStats:
        """Analyze multiple log files and generate comprehensive statistics."""
        all_entries = []
        timestamps = []
        
        for file_path in file_paths:
            print(f"Analyzing {file_path}...")
            
            try:
                for entry in self.read_log_file(file_path, max_lines_per_file):
                    all_entries.append(entry)
                    timestamps.append(entry.timestamp)
                    
                    # Collect statistics
                    self.stats['total_entries'] += 1
                    
                    if entry.level in ['ERROR', 'FATAL', 'CRITICAL']:
                        self.stats['error_count'] += 1
                        self.error_messages[entry.message] += 1
                    elif entry.level in ['WARN', 'WARNING']:
                        self.stats['warning_count'] += 1
                    
                    if entry.ip_address:
                        self.ip_addresses[entry.ip_address] += 1
                    
                    if entry.response_time:
                        self.response_times.append(entry.response_time)
            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        # Calculate final statistics
        avg_response_time = statistics.mean(self.response_times) if self.response_times else 0.0
        
        return LogStats(
            total_entries=self.stats['total_entries'],
            error_count=self.stats['error_count'],
            warning_count=self.stats['warning_count'],
            unique_ips=len(self.ip_addresses),
            avg_response_time=avg_response_time,
            top_errors=self.error_messages.most_common(10),
            top_ips=self.ip_addresses.most_common(10),
            time_range=(min(timestamps), max(timestamps)) if timestamps else (datetime.now(), datetime.now())
        )
    
    def find_error_patterns(self, entries: List[LogEntry]) -> Dict[str, List[LogEntry]]:
        """Find entries matching error patterns."""
        error_matches = defaultdict(list)
        
        for entry in entries:
            for i, pattern in enumerate(self.patterns.ERROR_PATTERNS):
                if pattern.search(entry.message):
                    pattern_name = f"error_pattern_{i+1}"
                    error_matches[pattern_name].append(entry)
        
        return dict(error_matches)
    
    def find_performance_issues(self, entries: List[LogEntry]) -> List[LogEntry]:
        """Find entries indicating performance issues."""
        performance_issues = []
        
        for entry in entries:
            for pattern in self.patterns.PERFORMANCE_PATTERNS:
                if pattern.search(entry.message):
                    performance_issues.append(entry)
                    break
        
        return performance_issues
    
    def generate_report(self, stats: LogStats, output_file: Optional[str] = None) -> str:
        """Generate a comprehensive analysis report."""
        report = []
        report.append("=" * 60)
        report.append("LOG ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic statistics
        report.append("BASIC STATISTICS:")
        report.append(f"  Total log entries: {stats.total_entries:,}")
        report.append(f"  Error entries: {stats.error_count:,}")
        report.append(f"  Warning entries: {stats.warning_count:,}")
        report.append(f"  Unique IP addresses: {stats.unique_ips:,}")
        report.append(f"  Average response time: {stats.avg_response_time:.2f}ms")
        report.append(f"  Time range: {stats.time_range[0]} to {stats.time_range[1]}")
        report.append("")
        
        # Top errors
        if stats.top_errors:
            report.append("TOP ERROR MESSAGES:")
            for i, (error, count) in enumerate(stats.top_errors[:5], 1):
                report.append(f"  {i}. {error[:80]}... ({count} times)")
            report.append("")
        
        # Top IP addresses
        if stats.top_ips:
            report.append("TOP IP ADDRESSES:")
            for i, (ip, count) in enumerate(stats.top_ips[:10], 1):
                report.append(f"  {i}. {ip}: {count} requests")
            report.append("")
        
        report.append("=" * 60)
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"Report saved to {output_file}")
        
        return report_text


def create_sample_logs():
    """Create sample log files for demonstration."""
    sample_logs_dir = Path("sample_logs")
    sample_logs_dir.mkdir(exist_ok=True)
    
    # Create sample Apache log
    apache_log = sample_logs_dir / "access.log"
    with open(apache_log, 'w') as f:
        f.write('192.168.1.1 - - [01/Dec/2023:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"\n')
        f.write('192.168.1.2 - - [01/Dec/2023:12:01:00 +0000] "POST /api/login HTTP/1.1" 401 567 "-" "curl/7.68.0"\n')
        f.write('192.168.1.1 - - [01/Dec/2023:12:02:00 +0000] "GET /dashboard HTTP/1.1" 500 890 "-" "Mozilla/5.0"\n')
        f.write('192.168.1.3 - - [01/Dec/2023:12:03:00 +0000] "GET /api/data HTTP/1.1" 200 2345 "-" "Python-requests/2.28.1"\n')
    
    # Create sample application log
    app_log = sample_logs_dir / "application.log"
    with open(app_log, 'w') as f:
        f.write('2023-12-01 12:00:00 [INFO] Application started successfully\n')
        f.write('2023-12-01 12:01:00 [ERROR] Database connection failed: timeout after 30s\n')
        f.write('2023-12-01 12:02:00 [WARN] High memory usage detected: 85%\n')
        f.write('2023-12-01 12:03:00 [INFO] User authentication successful\n')
        f.write('2023-12-01 12:04:00 [ERROR] Failed to process payment: invalid card number\n')
        f.write('2023-12-01 12:05:00 [FATAL] Critical system error: out of memory\n')
    
    print(f"Sample logs created in {sample_logs_dir}/")
    return [str(apache_log), str(app_log)]


def demo_log_analyzer():
    """Demonstrate the log analyzer functionality."""
    print("=== Log Analyzer Demo ===\n")
    
    # Create sample logs
    log_files = create_sample_logs()
    
    # Analyze logs
    analyzer = LogAnalyzer()
    stats = analyzer.analyze_logs(log_files)
    
    # Generate and display report
    report = analyzer.generate_report(stats, "log_analysis_report.txt")
    print(report)
    
    # Demonstrate pattern matching
    print("\n=== Pattern Analysis ===")
    
    # Read all entries for pattern analysis
    all_entries = []
    for file_path in log_files:
        all_entries.extend(list(analyzer.read_log_file(file_path)))
    
    # Find error patterns
    error_patterns = analyzer.find_error_patterns(all_entries)
    if error_patterns:
        print("\nError patterns found:")
        for pattern_name, entries in error_patterns.items():
            print(f"  {pattern_name}: {len(entries)} matches")
    
    # Find performance issues
    performance_issues = analyzer.find_performance_issues(all_entries)
    if performance_issues:
        print(f"\nPerformance issues found: {len(performance_issues)} entries")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Analyzer - Analyze log files for patterns and statistics")
    parser.add_argument("files", nargs="*", help="Log files to analyze")
    parser.add_argument("--format", choices=['auto', 'apache', 'application', 'syslog', 'docker', 'nginx_error'], 
                       default='auto', help="Log format (auto-detect by default)")
    parser.add_argument("--max-lines", type=int, help="Maximum lines to process per file")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    if args.files:
        # Analyze provided files
        analyzer = LogAnalyzer()
        stats = analyzer.analyze_logs(args.files, args.max_lines)
        report = analyzer.generate_report(stats, args.output)
        print(report)
    else:
        # Run demo with sample data
        demo_log_analyzer()