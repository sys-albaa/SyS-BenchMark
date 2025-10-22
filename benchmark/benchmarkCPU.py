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
            cpu_freq = psutil.cpu_freq()
            return {
                'processor': psutil.cpu_info().processor,
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'frequency_current': cpu_freq.current if cpu_freq else "N/A",
                'frequency_min': cpu_freq.min if cpu_freq else "N/A",
                'frequency_max': cpu_freq.max if cpu_freq else "N/A",
                'platform': platform.platform(),
                'architecture': platform.architecture()[0]
            }
        except Exception as e:
            print(f"Error getting CPU information: {e}")
            return {}

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

    def _display_results(self):
        """Display results"""
        print("\n📊 RESULTS:")
        print("-" * 40)
        print(f"🔢 Single-core: {self.results['single_core']['duration']:.2f} seconds")
        print(f"🔢 Multi-threading: {self.results['multi_threading']['duration']:.2f} seconds")
        print(f"🔢 Multi-processing: {self.results['multi_processing']['duration']:.2f} seconds")
        print(f"🔢 Matrix: {self.results['matrix']['duration']:.2f} seconds")
        print(f"🔢 Memory bandwidth: {self.results['memory_bandwidth']['duration']:.2f} seconds")

if __name__ == "__main__":
    benchmark = CPUBenchmark()
    benchmark.run_complete_benchmark()