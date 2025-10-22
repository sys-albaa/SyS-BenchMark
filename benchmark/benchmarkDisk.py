import psutil
import time
import os
import tempfile
import random
import threading
from concurrent.futures import ThreadPoolExecutor

class DiskBenchmark:
    def __init__(self):
        self.results = {}
        self.disk_info = self._get_disk_info()
        
    def _get_disk_info(self):
        """Ottiene informazioni dettagliate sui dischi"""
        try:
            disk_info = {}
            
            # Informazioni dischi fisici
            disk_usage = psutil.disk_usage('/')
            disk_info['total_gb'] = round(disk_usage.total / (1024**3), 2)
            disk_info['used_gb'] = round(disk_usage.used / (1024**3), 2)
            disk_info['free_gb'] = round(disk_usage.free / (1024**3), 2)
            disk_info['percentage_used'] = disk_usage.percent
            
            # Informazioni dischi specifici
            disk_info['partitions'] = []
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    disk_info['partitions'].append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total_gb': round(partition_usage.total / (1024**3), 2),
                        'used_gb': round(partition_usage.used / (1024**3), 2),
                        'free_gb': round(partition_usage.free / (1024**3), 2),
                        'percentage_used': partition_usage.percent
                    })
                except PermissionError:
                    continue
            
            return disk_info
        except Exception as e:
            print(f"Errore nel recupero informazioni disco: {e}")
            return {}
    
    def _sequential_write_test(self, file_size_mb=100):
        """Test scrittura sequenziale"""
        print(f"Test scrittura sequenziale ({file_size_mb} MB)...")
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Genera dati casuali
            data_size = file_size_mb * 1024 * 1024
            chunk_size = 1024 * 1024  # 1MB chunks
            data_chunk = os.urandom(chunk_size)
            
            start_time = time.time()
            with open(temp_path, 'wb') as f:
                for _ in range(data_size // chunk_size):
                    f.write(data_chunk)
            write_time = time.time() - start_time
            
            write_speed = (data_size / (1024*1024)) / write_time
            
            return {
                'write_time': write_time,
                'write_speed_mbps': write_speed,
                'file_size_mb': file_size_mb
            }
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _sequential_read_test(self, file_size_mb=100):
        """Test lettura sequenziale"""
        print(f"Test lettura sequenziale ({file_size_mb} MB)...")
        
        # Crea file temporaneo
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Scrivi dati nel file
            data_size = file_size_mb * 1024 * 1024
            chunk_size = 1024 * 1024
            data_chunk = os.urandom(chunk_size)
            
            with open(temp_path, 'wb') as f:
                for _ in range(data_size // chunk_size):
                    f.write(data_chunk)
            
            # Test lettura
            start_time = time.time()
            with open(temp_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
            read_time = time.time() - start_time
            
            read_speed = (data_size / (1024*1024)) / read_time
            
            return {
                'read_time': read_time,
                'read_speed_mbps': read_speed,
                'file_size_mb': file_size_mb
            }
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _random_access_test(self, file_size_mb=50):
        """Test accesso casuale"""
        print(f"Test accesso casuale ({file_size_mb} MB)...")
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Crea file con dati
            data_size = file_size_mb * 1024 * 1024
            chunk_size = 1024  # 1KB chunks
            data_chunk = os.urandom(chunk_size)
            
            with open(temp_path, 'wb') as f:
                for _ in range(data_size // chunk_size):
                    f.write(data_chunk)
            
            # Test accesso casuale
            num_operations = 1000
            start_time = time.time()
            
            with open(temp_path, 'rb') as f:
                for _ in range(num_operations):
                    # Posizione casuale
                    pos = random.randint(0, data_size - chunk_size)
                    f.seek(pos)
                    f.read(chunk_size)
            
            access_time = time.time() - start_time
            
            return {
                'access_time': access_time,
                'operations': num_operations,
                'ops_per_second': num_operations / access_time,
                'file_size_mb': file_size_mb
            }
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _small_file_test(self, num_files=1000, file_size_kb=1):
        """Test file piccoli"""
        print(f"Test file piccoli ({num_files} files da {file_size_kb} KB)...")
        
        temp_dir = tempfile.mkdtemp()
        file_paths = []
        
        try:
            # Crea file piccoli
            start_time = time.time()
            for i in range(num_files):
                file_path = os.path.join(temp_dir, f"test_file_{i}.tmp")
                with open(file_path, 'wb') as f:
                    f.write(os.urandom(file_size_kb * 1024))
                file_paths.append(file_path)
            create_time = time.time() - start_time
            
            # Leggi file piccoli
            start_time = time.time()
            for file_path in file_paths:
                with open(file_path, 'rb') as f:
                    f.read()
            read_time = time.time() - start_time
            
            # Cancella file piccoli
            start_time = time.time()
            for file_path in file_paths:
                os.unlink(file_path)
            delete_time = time.time() - start_time
            
            return {
                'create_time': create_time,
                'read_time': read_time,
                'delete_time': delete_time,
                'files_created': num_files,
                'files_per_second': num_files / create_time
            }
        finally:
            # Pulisci directory temporanea
            try:
                os.rmdir(temp_dir)
            except:
                pass
    
    def _concurrent_io_test(self, num_threads=4, file_size_mb=25):
        """Test I/O concorrente"""
        print(f"Test I/O concorrente ({num_threads} thread, {file_size_mb} MB per thread)...")
        
        def worker_thread(thread_id):
            """Worker thread per test concorrente"""
            temp_path = f"temp_concurrent_{thread_id}.tmp"
            data_size = file_size_mb * 1024 * 1024
            chunk_size = 1024 * 1024
            data_chunk = os.urandom(chunk_size)
            
            # Scrittura
            write_start = time.time()
            with open(temp_path, 'wb') as f:
                for _ in range(data_size // chunk_size):
                    f.write(data_chunk)
            write_time = time.time() - write_start
            
            # Lettura
            read_start = time.time()
            with open(temp_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
            read_time = time.time() - read_start
            
            # Pulisci
            os.unlink(temp_path)
            
            return {
                'write_time': write_time,
                'read_time': read_time,
                'write_speed_mbps': (data_size / (1024*1024)) / write_time,
                'read_speed_mbps': (data_size / (1024*1024)) / read_time
            }
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_thread, i) for i in range(num_threads)]
            results = [future.result() for future in futures]
        total_time = time.time() - start_time
        
        # Calcola statistiche aggregate
        total_write_speed = sum(r['write_speed_mbps'] for r in results)
        total_read_speed = sum(r['read_speed_mbps'] for r in results)
        
        return {
            'total_time': total_time,
            'threads_used': num_threads,
            'total_write_speed_mbps': total_write_speed,
            'total_read_speed_mbps': total_read_speed,
            'avg_write_speed_mbps': total_write_speed / num_threads,
            'avg_read_speed_mbps': total_read_speed / num_threads
        }
    
    def run_complete_benchmark(self):
        """Esegue benchmark completo del disco"""
        print("=" * 60)
        print("           COMPLETE DISK BENCHMARK")
        print("=" * 60)
        
        # Mostra informazioni sistema
        self._display_disk_info()
        
        print("\n" + "=" * 60)
        print("           START DISK PERFORMANCE TEST")
        print("=" * 60)
        
        # Esegui tutti i test
        self.results['sequential_write'] = self._sequential_write_test(100)
        self.results['sequential_read'] = self._sequential_read_test(100)
        self.results['random_access'] = self._random_access_test(50)
        self.results['small_files'] = self._small_file_test(500, 1)
        self.results['concurrent_io'] = self._concurrent_io_test(4, 25)
        
        # Mostra risultati
        self._display_results()
    
    def _display_disk_info(self):
        """Mostra informazioni disco"""
        print("\n💾 DISK INFORMATION:")
        print("-" * 40)
        print(f"📊 Total Space: {self.disk_info.get('total_gb', 'N/A')} GB")
        print(f"📊 Used Space: {self.disk_info.get('used_gb', 'N/A')} GB")
        print(f"📊 Free Space: {self.disk_info.get('free_gb', 'N/A')} GB")
        print(f"📊 Usage: {self.disk_info.get('percentage_used', 'N/A')}%")
        
        print(f"\n📁 PARTITIONS:")
        for partition in self.disk_info.get('partitions', []):
            print(f"   💿 {partition['device']} ({partition['mountpoint']})")
            print(f"      Type: {partition['fstype']}")
            print(f"      Size: {partition['total_gb']} GB")
            print(f"      Used: {partition['used_gb']} GB ({partition['percentage_used']}%)")
    
    def _display_results(self):
        """Mostra risultati benchmark"""
        print("\n📊 DISK BENCHMARK RESULTS:")
        print("-" * 50)
        
        # Risultati scrittura sequenziale
        seq_write = self.results['sequential_write']
        print(f"📝 Sequential Write:")
        print(f"   ⏱️  Time: {seq_write['write_time']:.2f} seconds")
        print(f"   🚀 Speed: {seq_write['write_speed_mbps']:.2f} MB/s")
        
        # Risultati lettura sequenziale
        seq_read = self.results['sequential_read']
        print(f"\n📖 Sequential Read:")
        print(f"   ⏱️  Time: {seq_read['read_time']:.2f} seconds")
        print(f"   🚀 Speed: {seq_read['read_speed_mbps']:.2f} MB/s")
        
        # Risultati accesso casuale
        random_access = self.results['random_access']
        print(f"\n🎲 Random Access:")
        print(f"   ⏱️  Time: {random_access['access_time']:.2f} seconds")
        print(f"   🔄 Operations: {random_access['operations']}")
        print(f"   ⚡ Ops/sec: {random_access['ops_per_second']:.2f}")
        
        # Risultati file piccoli
        small_files = self.results['small_files']
        print(f"\n📄 Small Files:")
        print(f"   📁 Files: {small_files['files_created']}")
        print(f"   ⏱️  Create Time: {small_files['create_time']:.2f} seconds")
        print(f"   ⏱️  Read Time: {small_files['read_time']:.2f} seconds")
        print(f"   ⏱️  Delete Time: {small_files['delete_time']:.2f} seconds")
        print(f"   ⚡ Files/sec: {small_files['files_per_second']:.2f}")
        
        # Risultati I/O concorrente
        concurrent = self.results['concurrent_io']
        print(f"\n🧵 Concurrent I/O:")
        print(f"   🧵 Threads: {concurrent['threads_used']}")
        print(f"   ⏱️  Total Time: {concurrent['total_time']:.2f} seconds")
        print(f"   📝 Total Write Speed: {concurrent['total_write_speed_mbps']:.2f} MB/s")
        print(f"   📖 Total Read Speed: {concurrent['total_read_speed_mbps']:.2f} MB/s")
        print(f"   📝 Avg Write Speed: {concurrent['avg_write_speed_mbps']:.2f} MB/s")
        print(f"   📖 Avg Read Speed: {concurrent['avg_read_speed_mbps']:.2f} MB/s")

if __name__ == "__main__":
    benchmark = DiskBenchmark()
    benchmark.run_complete_benchmark()
