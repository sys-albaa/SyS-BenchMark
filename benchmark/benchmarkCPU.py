import psutil
import time
import os
import threading
import multiprocessing
import tempfile
import platform
import socket
import math
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import statistics

class CPUBenchmark:
    def __init__(self):
        self.results = {}
        self.cpu_info = self._get_cpu_info()
        
    def _get_cpu_info(self):
        """gets detailed CPU information"""
        try:
            # Get CPU info with better error handling
            cpu_freq = psutil.cpu_freq()
            
            # Get processor name safely - try different methods
            processor_name = "Unknown"
            try:
                # Try to get CPU info from different sources
                import subprocess
                import platform
                
                # Method 1: Try platform module
                processor_name = platform.processor()
                if processor_name and processor_name != "":
                    pass
                else:
                    # Method 2: Try WMI on Windows
                    if platform.system() == "Windows":
                        try:
                            import wmi
                            c = wmi.WMI()
                            for processor in c.Win32_Processor():
                                processor_name = processor.Name
                                break
                        except:
                            # Method 3: Try subprocess
                            try:
                                result = subprocess.run(['wmic', 'cpu', 'get', 'name'], 
                                                      capture_output=True, text=True, timeout=5)
                                if result.returncode == 0:
                                    lines = result.stdout.strip().split('\n')
                                    if len(lines) > 1:
                                        processor_name = lines[1].strip()
                            except:
                                processor_name = "Unknown Processor"
                    else:
                        # Method 4: Try /proc/cpuinfo on Linux
                        try:
                            with open('/proc/cpuinfo', 'r') as f:
                                for line in f:
                                    if line.startswith('model name'):
                                        processor_name = line.split(':')[1].strip()
                                        break
                        except:
                            processor_name = "Unknown Processor"
            except:
                processor_name = "Unknown Processor"
            
            # Get core counts safely
            physical_cores = psutil.cpu_count(logical=False) or 1
            logical_cores = psutil.cpu_count(logical=True) or 1
            
            # Get frequency info safely
            freq_current = "N/A"
            freq_min = "N/A"
            freq_max = "N/A"
            if cpu_freq:
                freq_current = f"{cpu_freq.current:.1f}" if cpu_freq.current else "N/A"
                freq_min = f"{cpu_freq.min:.1f}" if cpu_freq.min else "N/A"
                freq_max = f"{cpu_freq.max:.1f}" if cpu_freq.max else "N/A"
            
            return {
                'processor': processor_name,
                'physical_cores': physical_cores,
                'logical_cores': logical_cores,
                'frequency_current': freq_current,
                'frequency_min': freq_min,
                'frequency_max': freq_max,
                'platform': platform.platform(),
                'architecture': platform.architecture()[0]
            }
        except Exception as e:
            print(f"Error getting CPU information: {e}")
            # Return default values instead of empty dict
            return {
                'processor': 'Unknown',
                'physical_cores': 1,
                'logical_cores': 1,
                'frequency_current': 'N/A',
                'frequency_min': 'N/A',
                'frequency_max': 'N/A',
                'platform': platform.platform(),
                'architecture': platform.architecture()[0]
            }

    def _cpu_intensive_task(self, duration=1.0, complexity=1000000):
        """CPU intensive task"""
        start_time = time.time()
        operations = 0
        
        while time.time() - start_time < duration:
            # Complex mathematical calculations
            for i in range(complexity):
                math.sqrt(i * random.random())
                operations += 1
                
        return operations

    def _matrix_multiplication(self, size=100):
        """Matrix multiplication for CPU test"""
        import numpy as np
        a = np.random.rand(size, size)
        b = np.random.rand(size, size)
        result = np.dot(a, b)
        return result.sum()

    def single_core_test(self, duration=5):
        """Test single-core"""
        print(f"Running single-core test for {duration} seconds...")
        start_time = time.time()
        operations = self._cpu_intensive_task(duration)
        end_time = time.time()
        
        return {
            'duration': end_time - start_time,
            'operations': operations,
            'ops_per_second': operations / (end_time - start_time)
        }

    def multi_threading_test(self, duration=5):
        """Test multi-threading"""
        print(f"Running multi-threading test for {duration} seconds...")
        num_threads = self.cpu_info['logical_cores']
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(self._cpu_intensive_task, duration) for _ in range(num_threads)]
            results = [future.result() for future in futures]
        end_time = time.time()
        
        total_operations = sum(results)
        return {
            'duration': end_time - start_time,
            'total_operations': total_operations,
            'ops_per_second': total_operations / (end_time - start_time),
            'threads_used': num_threads
        }

    def multi_processing_test(self, duration=5):
        """Test multi-processing"""
        print(f"Running multi-processing test for {duration} seconds...")
        num_processes = self.cpu_info['logical_cores']
        
        start_time = time.time()
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = [executor.submit(self._cpu_intensive_task, duration) for _ in range(num_processes)]
            results = [future.result() for future in futures]
        end_time = time.time()
        
        total_operations = sum(results)
        return {
            'duration': end_time - start_time,
            'total_operations': total_operations,
            'ops_per_second': total_operations / (end_time - start_time),
            'processes_used': num_processes
        }

    def matrix_benchmark(self, matrix_size=200):
        """Benchmark matrix multiplication"""
        print(f"Running benchmark matrix {matrix_size}x{matrix_size}...")
        try:
            start_time = time.time()
            result = self._matrix_multiplication(matrix_size)
            end_time = time.time()
            
            return {
                'duration': end_time - start_time,
                'matrix_size': matrix_size,
                'result_sum': result
            }
        except ImportError:
            print("NumPy not available, skipping matrix test")
            return None

    def memory_bandwidth_test(self, size_mb=100):
        """Test memory bandwidth"""
        print(f"Running memory bandwidth test ({size_mb} MB)...")
        
        # Alloca memoria
        data_size = size_mb * 1024 * 1024  # Converti in bytes
        data = bytearray(data_size)
        
        # Test writing
        start_time = time.time()
        for i in range(0, len(data), 1024):
            data[i:i+1024] = b'1' * 1024
        write_time = time.time() - start_time
        
        # Test reading
        start_time = time.time()
        total = 0
        for i in range(0, len(data), 1024):
            total += sum(data[i:i+1024])
        read_time = time.time() - start_time
        
        return {
            'data_size_mb': size_mb,
            'write_time': write_time,
            'read_time': read_time,
            'write_bandwidth_mbps': (data_size / (1024*1024)) / write_time,
            'read_bandwidth_mbps': (data_size / (1024*1024)) / read_time
        }

    def run_complete_benchmark(self):
        """Run complete benchmark"""
        print("=" * 60)
        print("           COMPLETE CPU BENCHMARK")
        print("=" * 60)
        
        # Display system information
        self._display_system_info()
        
        print("\n" + "=" * 60)
        print("           START PERFORMANCE TEST")
        print("=" * 60)
        
        # Run all tests
        self.results['single_core'] = self.single_core_test(3)
        self.results['multi_threading'] = self.multi_threading_test(3)
        self.results['multi_processing'] = self.multi_processing_test(3)
        self.results['matrix'] = self.matrix_benchmark(150)
        self.results['memory_bandwidth'] = self.memory_bandwidth_test(50)
        
        # Display results
        self._display_results()

    def _display_system_info(self):
        """Display detailed system information"""
        print("\nSYSTEM INFORMATION:")
        print("-" * 40)
        print(f"🖥️  Processor: {self.cpu_info.get('processor', 'N/A')}")
        print(f"🔢 Physical cores: {self.cpu_info.get('physical_cores', 'N/A')}")
        print(f"⚡ Logical cores: {self.cpu_info.get('logical_cores', 'N/A')}")
        print(f"📈 Current frequency: {self.cpu_info.get('frequency_current', 'N/A')} MHz")
        print(f"📉 Minimum frequency: {self.cpu_info.get('frequency_min', 'N/A')} MHz")
        print(f"📈 Maximum frequency: {self.cpu_info.get('frequency_max', 'N/A')} MHz")
        print(f"📈 Platform: {self.cpu_info.get('platform', 'N/A')}")
        print(f"📈 Architecture: {self.cpu_info.get('architecture', 'N/A')}")
        
        # Debug information
        print(f"\n🔍 Debug - CPU info keys: {list(self.cpu_info.keys())}")
        print(f"🔍 Debug - psutil version: {psutil.__version__}")
        print(f"🔍 Debug - Platform: {platform.system()}")

    def _display_results(self):
        """Display results"""
        print("\n📊 RESULTS:")
        print("-" * 40)
        print(f"🔢 Single-core: {self.results['single_core']['duration']:.2f} seconds")
        print(f"🔢 Multi-threading: {self.results['multi_threading']['duration']:.2f} seconds")
        print(f"🔢 Multi-processing: {self.results['multi_processing']['duration']:.2f} seconds")
        
        # Handle matrix results safely
        if self.results['matrix']:
            print(f"🔢 Matrix: {self.results['matrix']['duration']:.2f} seconds")
        else:
            print("🔢 Matrix: Skipped (NumPy not available)")
        
        # Handle memory bandwidth results safely
        if 'memory_bandwidth' in self.results and self.results['memory_bandwidth']:
            mb_result = self.results['memory_bandwidth']
            if 'duration' in mb_result:
                print(f"🔢 Memory bandwidth: {mb_result['duration']:.2f} seconds")
            else:
                print(f"🔢 Memory bandwidth: Write {mb_result.get('write_bandwidth_mbps', 0):.2f} MB/s, Read {mb_result.get('read_bandwidth_mbps', 0):.2f} MB/s")
        else:
            print("🔢 Memory bandwidth: Failed")

if __name__ == "__main__":
    benchmark = CPUBenchmark()
    benchmark.run_complete_benchmark()