# SyS-BenchMark
Complete Benchmark System for Windows, Linux and macOS

## Description

SyS-BenchMark is a modular and comprehensive system for benchmarking system performance. It offers an interactive menu that allows you to choose between different types of benchmarks: CPU, RAM, Disk, and Network. Each benchmark is implemented in a separate module for maximum flexibility and maintainability.

## Project Structure

```
SyS-BenchMark/
├── main.py                 # Main menu and user interface
├── benchmark/              # Benchmark modules directory
│   ├── __init__.py        # Package initialization
│   ├── benchmarkCPU.py    # Multi-core CPU benchmark
│   ├── benchmarkRAM.py    # RAM memory benchmark
│   ├── benchmarkDisk.py   # Disk and storage benchmark
│   └── benchmarkNetwork.py # Network connection benchmark
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Features

### 🖥️ CPU Benchmark (`benchmark/benchmarkCPU.py`)
- **Single-core test**: Evaluates single core performance
- **Multi-threading test**: Utilizes all logical cores with threading
- **Multi-processing test**: Leverages multiprocessing for parallel performance
- **Matrix benchmark**: Matrix multiplication tests with NumPy
- **Memory bandwidth test**: Evaluates memory bandwidth

### 💾 RAM Benchmark (`benchmark/benchmarkRAM.py`)
- **Memory allocation test**: Memory allocation and access tests
- **Memory bandwidth test**: Memory read/write speed tests
- **Memory stress test**: Stress testing with multiple threading
- **Memory latency test**: Latency tests with different array sizes

### 💿 Disk Benchmark (`benchmark/benchmarkDisk.py`)
- **Sequential read/write**: Sequential read/write speed tests
- **Random access test**: Random file access tests
- **Small files test**: Performance with small files
- **Concurrent I/O test**: Concurrent I/O testing with threading

### 🌐 Network Benchmark (`benchmark/benchmarkNetwork.py`)
- **Ping test**: Network latency testing
- **Download speed test**: Download speed testing
- **Connection test**: TCP connection testing
- **DNS resolution test**: DNS resolution testing
- **Local bandwidth test**: Local bandwidth testing

## Characteristics

### 🎯 Interactive Menu
- User-friendly interface with emojis and clear formatting
- Individual benchmark selection
- "Complete System Benchmark" option for all tests
- Confirmation before execution
- Robust error handling

### 📊 System Information
Each benchmark collects and displays detailed information:
- **CPU**: Processor, cores, frequencies, architecture
- **RAM**: Total memory, used, swap, statistics
- **Disk**: Total space, used, partitions, filesystem
- **Network**: Network interfaces, statistics, IP addresses

### 🚀 Performance and Results
- Tests optimized to maximize resource utilization
- Detailed results with specific metrics for each component
- Support for multi-core and multi-threading systems
- Intelligent system resource management

## Requirements

### System
- Python 3.6 or higher
- Windows 10+, Linux, or macOS
- Administrator privileges (optional, for some network tests)

### Python Dependencies
```
psutil>=5.9.0      # System and process information
numpy>=1.21.0      # Advanced mathematical calculations
requests>=2.28.0   # HTTP network testing
```

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sys-albaa/SyS-BenchMark.git
cd SyS-BenchMark
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### 🚀 Quick Start
```bash
python main.py
```

### 📋 Main Menu
```
🚀 SyS-BenchMark - Complete Benchmark System 🚀
======================================================================
📊 Professional tool for system performance testing
🔧 Choose the type of benchmark to run:
======================================================================

📋 MAIN MENU:
--------------------------------------------------
  1. CPU Benchmark
  2. RAM Benchmark  
  3. Disk Benchmark
  4. Network Benchmark
  5. Complete System Benchmark (All benchmarks)
  0. Exit
--------------------------------------------------
```

### 🎯 Individual Benchmark Execution
```bash
# CPU only
python benchmark/benchmarkCPU.py

# RAM only
python benchmark/benchmarkRAM.py

# Disk only
python benchmark/benchmarkDisk.py

# Network only
python benchmark/benchmarkNetwork.py
```

## Output Examples

### CPU Benchmark
```
🖥️  Processor: Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz
🔢 Physical cores: 8
⚡ Logical cores: 16
📈 Current frequency: 3800.0 MHz

🚀 Single-core: 3.45 seconds
🚀 Multi-threading: 1.23 seconds  
🚀 Multi-processing: 1.18 seconds
```

### RAM Benchmark
```
💾 Total RAM: 32.0 GB
📊 Available RAM: 24.5 GB
📊 Used RAM: 7.5 GB

🚀 Write Speed: 12,450.32 MB/s
📖 Read Speed: 15,230.18 MB/s
🎲 Random Access: 8,500,000 ops/sec
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## Support

For support and questions:
- 📧 Email: support@sysbenchmark.com
- 🐛 Issues: [GitHub Issues](https://github.com/sys-albaa/SyS-BenchMark/issues)
- 📖 Wiki: [Complete Documentation](https://github.com/sys-albaa/SyS-BenchMark/wiki)
