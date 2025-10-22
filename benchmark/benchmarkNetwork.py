import psutil
import time
import socket
import threading
import requests
import statistics
from concurrent.futures import ThreadPoolExecutor
import urllib.parse

class NetworkBenchmark:
    def __init__(self):
        self.results = {}
        self.network_info = self._get_network_info()
        
    def _get_network_info(self):
        """Ottiene informazioni dettagliate sulla rete"""
        try:
            network_info = {}
            
            # Informazioni interfacce di rete
            network_info['interfaces'] = []
            for interface, addrs in psutil.net_if_addrs().items():
                interface_info = {
                    'name': interface,
                    'addresses': []
                }
                for addr in addrs:
                    interface_info['addresses'].append({
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                network_info['interfaces'].append(interface_info)
            
            # Statistiche di rete
            net_io = psutil.net_io_counters()
            network_info['stats'] = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout
            }
            
            return network_info
        except Exception as e:
            print(f"Errore nel recupero informazioni rete: {e}")
            return {}
    
    def _ping_test(self, host="8.8.8.8", count=10):
        """Test ping"""
        print(f"Test ping verso {host} ({count} pacchetti)...")
        
        try:
            import subprocess
            import platform
            
            # Comando ping dipendente dal sistema operativo
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", str(count), host]
            else:
                cmd = ["ping", "-c", str(count), host]
            
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            end_time = time.time()
            
            if result.returncode == 0:
                # Estrai statistiche dal output
                output = result.stdout
                lines = output.split('\n')
                
                # Cerca righe con statistiche
                stats_line = None
                for line in lines:
                    if 'time=' in line or 'time<' in line:
                        stats_line = line
                        break
                
                if stats_line:
                    # Estrai tempo di risposta (semplificato)
                    times = []
                    for line in lines:
                        if 'time=' in line:
                            try:
                                time_part = line.split('time=')[1].split()[0]
                                if 'ms' in time_part:
                                    times.append(float(time_part.replace('ms', '')))
                            except:
                                pass
                    
                    if times:
                        avg_time = statistics.mean(times)
                        min_time = min(times)
                        max_time = max(times)
                    else:
                        avg_time = min_time = max_time = 0
                else:
                    avg_time = min_time = max_time = 0
                
                return {
                    'success': True,
                    'host': host,
                    'packets_sent': count,
                    'avg_time_ms': avg_time,
                    'min_time_ms': min_time,
                    'max_time_ms': max_time,
                    'total_time': end_time - start_time
                }
            else:
                return {
                    'success': False,
                    'host': host,
                    'error': 'Ping failed',
                    'total_time': end_time - start_time
                }
        except Exception as e:
            return {
                'success': False,
                'host': host,
                'error': str(e),
                'total_time': 0
            }
    
    def _download_speed_test(self, url="http://speedtest.ftp.otenet.gr/files/test1Mb.db", timeout=30):
        """Test velocità download"""
        print(f"Test velocità download...")
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=timeout, stream=True)
            end_time = time.time()
            
            if response.status_code == 200:
                # Calcola velocità
                content_length = int(response.headers.get('content-length', 0))
                if content_length == 0:
                    # Se non abbiamo content-length, leggiamo tutto
                    data = response.content
                    content_length = len(data)
                
                download_time = end_time - start_time
                speed_mbps = (content_length / (1024 * 1024)) / download_time if download_time > 0 else 0
                
                return {
                    'success': True,
                    'url': url,
                    'size_mb': content_length / (1024 * 1024),
                    'time_seconds': download_time,
                    'speed_mbps': speed_mbps
                }
            else:
                return {
                    'success': False,
                    'url': url,
                    'error': f'HTTP {response.status_code}',
                    'time_seconds': end_time - start_time
                }
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'time_seconds': 0
            }
    
    def _connection_test(self, host="google.com", port=80, timeout=10):
        """Test connessione TCP"""
        print(f"Test connessione TCP {host}:{port}...")
        
        try:
            start_time = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            end_time = time.time()
            sock.close()
            
            return {
                'success': result == 0,
                'host': host,
                'port': port,
                'time_seconds': end_time - start_time,
                'error': 'Connection failed' if result != 0 else None
            }
        except Exception as e:
            return {
                'success': False,
                'host': host,
                'port': port,
                'time_seconds': 0,
                'error': str(e)
            }
    
    def _dns_resolution_test(self, domains=None):
        """Test risoluzione DNS"""
        if domains is None:
            domains = ["google.com", "github.com", "stackoverflow.com", "reddit.com", "wikipedia.org"]
        
        print(f"Test risoluzione DNS ({len(domains)} domini)...")
        
        results = []
        for domain in domains:
            try:
                start_time = time.time()
                ip = socket.gethostbyname(domain)
                end_time = time.time()
                
                results.append({
                    'domain': domain,
                    'ip': ip,
                    'time_seconds': end_time - start_time,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'domain': domain,
                    'ip': None,
                    'time_seconds': 0,
                    'success': False,
                    'error': str(e)
                })
        
        # Calcola statistiche
        successful = [r for r in results if r['success']]
        if successful:
            avg_time = statistics.mean([r['time_seconds'] for r in successful])
            min_time = min([r['time_seconds'] for r in successful])
            max_time = max([r['time_seconds'] for r in successful])
        else:
            avg_time = min_time = max_time = 0
        
        return {
            'domains_tested': len(domains),
            'successful_resolutions': len(successful),
            'failed_resolutions': len(results) - len(successful),
            'avg_time_seconds': avg_time,
            'min_time_seconds': min_time,
            'max_time_seconds': max_time,
            'results': results
        }
    
    def _bandwidth_test(self, test_size_mb=10):
        """Test bandwidth locale"""
        print(f"Test bandwidth locale ({test_size_mb} MB)...")
        
        # Crea server locale
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('localhost', 0))
        server_socket.listen(1)
        
        port = server_socket.getsockname()[1]
        
        def server_worker():
            """Worker server"""
            conn, addr = server_socket.accept()
            data = b'X' * (1024 * 1024)  # 1MB di dati
            for _ in range(test_size_mb):
                conn.send(data)
            conn.close()
        
        # Avvia server in thread separato
        server_thread = threading.Thread(target=server_worker)
        server_thread.start()
        
        # Test client
        time.sleep(0.1)  # Aspetta che il server sia pronto
        
        try:
            start_time = time.time()
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', port))
            
            total_received = 0
            while total_received < test_size_mb * 1024 * 1024:
                data = client_socket.recv(1024 * 1024)
                if not data:
                    break
                total_received += len(data)
            
            end_time = time.time()
            client_socket.close()
            
            bandwidth_mbps = (total_received / (1024 * 1024)) / (end_time - start_time)
            
            return {
                'success': True,
                'data_mb': total_received / (1024 * 1024),
                'time_seconds': end_time - start_time,
                'bandwidth_mbps': bandwidth_mbps
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'time_seconds': 0,
                'bandwidth_mbps': 0
            }
        finally:
            server_socket.close()
            server_thread.join()
    
    def run_complete_benchmark(self):
        """Esegue benchmark completo della rete"""
        print("=" * 60)
        print("           COMPLETE NETWORK BENCHMARK")
        print("=" * 60)
        
        # Mostra informazioni sistema
        self._display_network_info()
        
        print("\n" + "=" * 60)
        print("           START NETWORK PERFORMANCE TEST")
        print("=" * 60)
        
        # Esegui tutti i test
        self.results['ping'] = self._ping_test("8.8.8.8", 5)
        self.results['download'] = self._download_speed_test()
        self.results['connection'] = self._connection_test("google.com", 80)
        self.results['dns'] = self._dns_resolution_test()
        self.results['bandwidth'] = self._bandwidth_test(5)
        
        # Mostra risultati
        self._display_results()
    
    def _display_network_info(self):
        """Mostra informazioni rete"""
        print("\n🌐 NETWORK INFORMATION:")
        print("-" * 40)
        
        # Mostra interfacce di rete
        for interface in self.network_info.get('interfaces', []):
            if interface['name'] != 'lo':  # Salta loopback
                print(f"🔌 Interface: {interface['name']}")
                for addr in interface['addresses']:
                    if addr['family'] == 'AddressFamily.AF_INET':
                        print(f"   📍 IPv4: {addr['address']}")
                    elif addr['family'] == 'AddressFamily.AF_INET6':
                        print(f"   📍 IPv6: {addr['address']}")
        
        # Mostra statistiche
        stats = self.network_info.get('stats', {})
        if stats:
            print(f"\n📊 Network Statistics:")
            print(f"   📤 Bytes Sent: {stats.get('bytes_sent', 0):,}")
            print(f"   📥 Bytes Received: {stats.get('bytes_recv', 0):,}")
            print(f"   📦 Packets Sent: {stats.get('packets_sent', 0):,}")
            print(f"   📦 Packets Received: {stats.get('packets_recv', 0):,}")
            if stats.get('errin', 0) > 0 or stats.get('errout', 0) > 0:
                print(f"   ⚠️  Errors In: {stats.get('errin', 0)}")
                print(f"   ⚠️  Errors Out: {stats.get('errout', 0)}")
    
    def _display_results(self):
        """Mostra risultati benchmark"""
        print("\n📊 NETWORK BENCHMARK RESULTS:")
        print("-" * 50)
        
        # Risultati ping
        ping = self.results['ping']
        if ping['success']:
            print(f"🏓 Ping Test:")
            print(f"   🎯 Host: {ping['host']}")
            print(f"   📦 Packets: {ping['packets_sent']}")
            print(f"   ⏱️  Avg Time: {ping['avg_time_ms']:.2f} ms")
            print(f"   ⏱️  Min Time: {ping['min_time_ms']:.2f} ms")
            print(f"   ⏱️  Max Time: {ping['max_time_ms']:.2f} ms")
        else:
            print(f"🏓 Ping Test: ❌ Failed - {ping.get('error', 'Unknown error')}")
        
        # Risultati download
        download = self.results['download']
        if download['success']:
            print(f"\n📥 Download Test:")
            print(f"   🌐 URL: {download['url']}")
            print(f"   📊 Size: {download['size_mb']:.2f} MB")
            print(f"   ⏱️  Time: {download['time_seconds']:.2f} seconds")
            print(f"   🚀 Speed: {download['speed_mbps']:.2f} MB/s")
        else:
            print(f"\n📥 Download Test: ❌ Failed - {download.get('error', 'Unknown error')}")
        
        # Risultati connessione
        connection = self.results['connection']
        if connection['success']:
            print(f"\n🔗 Connection Test:")
            print(f"   🎯 Host: {connection['host']}:{connection['port']}")
            print(f"   ⏱️  Time: {connection['time_seconds']:.3f} seconds")
        else:
            print(f"\n🔗 Connection Test: ❌ Failed - {connection.get('error', 'Unknown error')}")
        
        # Risultati DNS
        dns = self.results['dns']
        print(f"\n🌐 DNS Resolution Test:")
        print(f"   📊 Domains Tested: {dns['domains_tested']}")
        print(f"   ✅ Successful: {dns['successful_resolutions']}")
        print(f"   ❌ Failed: {dns['failed_resolutions']}")
        if dns['successful_resolutions'] > 0:
            print(f"   ⏱️  Avg Time: {dns['avg_time_seconds']:.3f} seconds")
            print(f"   ⏱️  Min Time: {dns['min_time_seconds']:.3f} seconds")
            print(f"   ⏱️  Max Time: {dns['max_time_seconds']:.3f} seconds")
        
        # Risultati bandwidth
        bandwidth = self.results['bandwidth']
        if bandwidth['success']:
            print(f"\n🚀 Local Bandwidth Test:")
            print(f"   📊 Data: {bandwidth['data_mb']:.2f} MB")
            print(f"   ⏱️  Time: {bandwidth['time_seconds']:.2f} seconds")
            print(f"   🚀 Speed: {bandwidth['bandwidth_mbps']:.2f} MB/s")
        else:
            print(f"\n🚀 Local Bandwidth Test: ❌ Failed - {bandwidth.get('error', 'Unknown error')}")

if __name__ == "__main__":
    benchmark = NetworkBenchmark()
    benchmark.run_complete_benchmark()
