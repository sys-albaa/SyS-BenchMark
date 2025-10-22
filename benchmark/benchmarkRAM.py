import psutil
import time
import os
import threading
import random
import statistics
from concurrent.futures import ThreadPoolExecutor

class RAMBenchmark:
    def __init__(self):
        self.results = {}
        self.memory_info = self._get_memory_info()
        
    def _get_memory_info(self):
        """Ottiene informazioni dettagliate sulla memoria"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            return {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'used_gb': round(memory.used / (1024**3), 2),
                'percentage_used': memory.percent,
                'swap_total_gb': round(swap.total / (1024**3), 2),
                'swap_used_gb': round(swap.used / (1024**3), 2),
                'swap_percentage': swap.percent
            }
        except Exception as e:
            print(f"Errore nel recupero informazioni memoria: {e}")
            return {}
    
    def _memory_allocation_test(self, size_mb=100):
        """Test di allocazione memoria"""
        print(f"Test allocazione memoria ({size_mb} MB)...")
        start_time = time.time()
        
        # Alloca blocchi di memoria
        data_blocks = []
        block_size = size_mb * 1024 * 1024 // 10  # Dividi in 10 blocchi
        
        for i in range(10):
            block = bytearray(block_size)
            # Riempi con dati casuali
            for j in range(0, len(block), 1024):
                block[j:j+1024] = os.urandom(min(1024, len(block)-j))
            data_blocks.append(block)
        
        allocation_time = time.time() - start_time
        
        # Test di accesso casuale
        access_start = time.time()
        total_sum = 0
        for _ in range(1000):
            block_idx = random.randint(0, len(data_blocks)-1)
            byte_idx = random.randint(0, len(data_blocks[block_idx])-1)
            total_sum += data_blocks[block_idx][byte_idx]
        access_time = time.time() - access_start
        
        return {
            'allocation_time': allocation_time,
            'access_time': access_time,
            'total_allocated_mb': size_mb,
            'access_operations': 1000
        }
    
    def _memory_bandwidth_test(self, size_mb=200):
        """Test bandwidth memoria"""
        print(f"Test bandwidth memoria ({size_mb} MB)...")
        
        # Alloca memoria
        data_size = size_mb * 1024 * 1024
        data = bytearray(data_size)
        
        # Test scrittura sequenziale
        write_start = time.time()
        for i in range(0, len(data), 1024):
            data[i:i+1024] = os.urandom(min(1024, len(data)-i))
        write_time = time.time() - write_start
        
        # Test lettura sequenziale
        read_start = time.time()
        total = 0
        for i in range(0, len(data), 1024):
            total += sum(data[i:i+1024])
        read_time = time.time() - read_start
        
        # Test accesso casuale
        random_start = time.time()
        for _ in range(10000):
            idx = random.randint(0, len(data)-1)
            total += data[idx]
        random_time = time.time() - random_start
        
        return {
            'write_bandwidth_mbps': (data_size / (1024*1024)) / write_time,
            'read_bandwidth_mbps': (data_size / (1024*1024)) / read_time,
            'random_access_ops_per_sec': 10000 / random_time,
            'write_time': write_time,
            'read_time': read_time,
            'random_time': random_time
        }
    
    def _memory_stress_test(self, duration=10):
        """Test di stress memoria"""
        print(f"Test stress memoria ({duration} secondi)...")
        
        def stress_worker():
            """Worker per stress test"""
            start_time = time.time()
            operations = 0
            data_blocks = []
            
            while time.time() - start_time < duration:
                # Alloca blocchi di memoria
                block_size = random.randint(1024*1024, 10*1024*1024)  # 1-10 MB
                block = bytearray(block_size)
                
                # Riempi con dati
                for i in range(0, len(block), 1024):
                    block[i:i+1024] = os.urandom(min(1024, len(block)-i))
                
                data_blocks.append(block)
                operations += 1
                
                # Pulisci alcuni blocchi per evitare OOM
                if len(data_blocks) > 50:
                    data_blocks = data_blocks[-25:]  # Mantieni solo gli ultimi 25
            
            return operations
        
        # Esegui stress test con threading
        num_threads = min(4, psutil.cpu_count())
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(stress_worker) for _ in range(num_threads)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        total_operations = sum(results)
        
        return {
            'duration': end_time - start_time,
            'total_operations': total_operations,
            'ops_per_second': total_operations / (end_time - start_time),
            'threads_used': num_threads
        }
    
    def _memory_latency_test(self):
        """Test latenza memoria"""
        print("Test latenza memoria...")
        
        # Test con diverse dimensioni di array
        sizes = [1024, 10240, 102400, 1024000]  # 1KB, 10KB, 100KB, 1MB
        results = {}
        
        for size in sizes:
            # Alloca array
            data = [random.randint(0, 255) for _ in range(size)]
            
            # Test accesso sequenziale
            start_time = time.time()
            for _ in range(1000):
                for i in range(0, size, 10):  # Ogni 10 elementi
                    _ = data[i]
            seq_time = time.time() - start_time
            
            # Test accesso casuale
            start_time = time.time()
            for _ in range(1000):
                idx = random.randint(0, size-1)
                _ = data[idx]
            rand_time = time.time() - start_time
            
            results[size] = {
                'sequential_time': seq_time,
                'random_time': rand_time,
                'sequential_latency_ns': (seq_time * 1000000000) / (1000 * (size // 10)),
                'random_latency_ns': (rand_time * 1000000000) / 1000
            }
        
        return results
    
    def run_complete_benchmark(self):
        """Esegue benchmark completo della memoria"""
        print("=" * 60)
        print("           COMPLETE RAM BENCHMARK")
        print("=" * 60)
        
        # Mostra informazioni sistema
        self._display_memory_info()
        
        print("\n" + "=" * 60)
        print("           START MEMORY PERFORMANCE TEST")
        print("=" * 60)
        
        # Esegui tutti i test
        self.results['allocation'] = self._memory_allocation_test(100)
        self.results['bandwidth'] = self._memory_bandwidth_test(200)
        self.results['stress'] = self._memory_stress_test(5)
        self.results['latency'] = self._memory_latency_test()
        
        # Mostra risultati
        self._display_results()
    
    def _display_memory_info(self):
        """Mostra informazioni memoria"""
        print("\n💾 MEMORY INFORMATION:")
        print("-" * 40)
        print(f"📊 Total RAM: {self.memory_info.get('total_gb', 'N/A')} GB")
        print(f"📊 Available RAM: {self.memory_info.get('available_gb', 'N/A')} GB")
        print(f"📊 Used RAM: {self.memory_info.get('used_gb', 'N/A')} GB")
        print(f"📊 RAM Usage: {self.memory_info.get('percentage_used', 'N/A')}%")
        print(f"💿 Total Swap: {self.memory_info.get('swap_total_gb', 'N/A')} GB")
        print(f"💿 Used Swap: {self.memory_info.get('swap_used_gb', 'N/A')} GB")
        print(f"💿 Swap Usage: {self.memory_info.get('swap_percentage', 'N/A')}%")
    
    def _display_results(self):
        """Mostra risultati benchmark"""
        print("\n📊 RAM BENCHMARK RESULTS:")
        print("-" * 50)
        
        # Risultati allocazione
        alloc = self.results['allocation']
        print(f"🔧 Memory Allocation:")
        print(f"   ⏱️  Allocation Time: {alloc['allocation_time']:.3f} seconds")
        print(f"   ⏱️  Access Time: {alloc['access_time']:.3f} seconds")
        print(f"   📊 Allocated: {alloc['total_allocated_mb']} MB")
        
        # Risultati bandwidth
        bw = self.results['bandwidth']
        print(f"\n🚀 Memory Bandwidth:")
        print(f"   📝 Write Speed: {bw['write_bandwidth_mbps']:.2f} MB/s")
        print(f"   📖 Read Speed: {bw['read_bandwidth_mbps']:.2f} MB/s")
        print(f"   🎲 Random Access: {bw['random_access_ops_per_sec']:.0f} ops/sec")
        
        # Risultati stress test
        stress = self.results['stress']
        print(f"\n💪 Memory Stress Test:")
        print(f"   ⏱️  Duration: {stress['duration']:.2f} seconds")
        print(f"   🔄 Operations: {stress['total_operations']}")
        print(f"   ⚡ Ops/sec: {stress['ops_per_second']:.2f}")
        print(f"   🧵 Threads: {stress['threads_used']}")
        
        # Risultati latenza
        latency = self.results['latency']
        print(f"\n⏱️  Memory Latency:")
        for size, result in latency.items():
            size_kb = size // 1024
            print(f"   📏 {size_kb}KB - Seq: {result['sequential_latency_ns']:.1f}ns, Rand: {result['random_latency_ns']:.1f}ns")

if __name__ == "__main__":
    benchmark = RAMBenchmark()
    benchmark.run_complete_benchmark()
