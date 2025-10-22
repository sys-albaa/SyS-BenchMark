#!/usr/bin/env python3
"""
SyS-BenchMark - Complete Benchmark System
Main menu for selecting benchmarks
"""

import os
import sys
import time
from benchmark.benchmarkCPU import CPUBenchmark
from benchmark.benchmarkRAM import RAMBenchmark
from benchmark.benchmarkDisk import DiskBenchmark
from benchmark.benchmarkNetwork import NetworkBenchmark

class BenchmarkSystem:
    def __init__(self):
        self.benchmarks = {
            '1': ('CPU Benchmark', CPUBenchmark),
            '2': ('RAM Benchmark', RAMBenchmark),
            '3': ('Disk Benchmark', DiskBenchmark),
            '4': ('Network Benchmark', NetworkBenchmark),
            '5': ('Complete System Benchmark', None)
        }
    
    def display_banner(self):
        """Display the system banner"""
        print("=" * 70)
        print("           🚀 SyS-BenchMark - Complete System Benchmark 🚀")
        print("=" * 70)
        print("📊 Professional tool for system performance testing developed by albaa")
        print("🔧 Choose the type of benchmark to run:")
        print("=" * 70)
    
    def display_menu(self):
        """Display the main menu"""
        print("\nMAIN MENU:")
        print("-" * 50)
        for key, (name, _) in self.benchmarks.items():
            if key == '5':
                print(f"  {key}. {name} (All benchmarks)")
            else:
                print(f"  {key}. {name}")
        print("  0. Exit")
        print("-" * 50)
    
    def get_user_choice(self):
        """Get the user's choice"""
        while True:
            try:
                choice = input("\n🎯 Enter your choice (0-5): ").strip()
                if choice in ['0', '1', '2', '3', '4', '5']:
                    return choice
                else:
                    print("❌ Invalid choice! Enter a number between 0 and 5.")
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
    
    def run_single_benchmark(self, benchmark_class):
        """Run a single benchmark"""
        try:
            print(f"\n🚀 Starting {benchmark_class.__name__}...")
            benchmark = benchmark_class()
            benchmark.run_complete_benchmark()
            print(f"\n✅ {benchmark_class.__name__} completed successfully!")
        except Exception as e:
            print(f"\n❌ Error during execution: {e}")
    
    def run_complete_benchmark(self):
        """Run all benchmarks in sequence"""
        print("\n🚀 Start Complete System Benchmark...")
        print("⏱️  This process may take several minutes...")
        
        benchmarks_to_run = [
            ('CPU Benchmark', CPUBenchmark),
            ('RAM Benchmark', RAMBenchmark),
            ('Disk Benchmark', DiskBenchmark),
            ('Network Benchmark', NetworkBenchmark)
        ]
        
        total_start = time.time()
        
        for i, (name, benchmark_class) in enumerate(benchmarks_to_run, 1):
            print(f"\n{'='*60}")
            print(f"📊 {i}/4 - {name}")
            print(f"{'='*60}")
            
            try:
                benchmark = benchmark_class()
                benchmark.run_complete_benchmark()
                print(f"\n✅ {name} completed!")
            except Exception as e:
                print(f"\n❌ Error in {name}: {e}")
            
            if i < len(benchmarks_to_run):
                print("\n⏳ Pause of 3 seconds before the next test...")
                time.sleep(3)
        
        total_time = time.time() - total_start
        print(f"\n🎉 Complete System Benchmark completed in {total_time:.2f} seconds!")
    
    def run(self):
        """Main method to execute the system"""
        while True:
            # Clear the screen (works on Windows, Linux, macOS)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            self.display_banner()
            self.display_menu()
            
            choice = self.get_user_choice()
            
            if choice == '0':
                print("\n👋 Thank you for using SyS-BenchMark!")
                print("🔗 For support and updates: https://github.com/your-repo")
                break
            
            elif choice == '5':
                # Complete System Benchmark
                confirm = input("\n⚠️  The Complete System Benchmark will take several minutes. Continue? (s/n): ").lower()
                if confirm in ['s', 'si', 'y', 'yes']:
                    self.run_complete_benchmark()
                else:
                    print("❌ Operation cancelled.")
            
            else:
                # Singolo benchmark
                benchmark_name, benchmark_class = self.benchmarks[choice]
                confirm = input(f"\n⚠️  Run {benchmark_name}? (s/n): ").lower()
                if confirm in ['s', 'si', 'y', 'yes']:
                    self.run_single_benchmark(benchmark_class)
                else:
                    print("❌ Operation cancelled.")
            
            # Pausa prima di tornare al menu
            input("\n⏸️  Press ENTER to return to the main menu...")

def main():
    """Main function"""
    try:
        system = BenchmarkSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
