#!/usr/bin/env python3
"""
AUTOMATED TEST RUNNER for Drone Optimization Dashboard
Systematically runs test cases and collects results
Version: 2.4.0
"""

import json
import time
import pandas as pd
from datetime import datetime
from test_cases import TEST_CASES, validate_results
import subprocess
import requests
import os

class DroneTestRunner:
    def __init__(self, dashboard_url="http://127.0.0.1:8050"):
        self.dashboard_url = dashboard_url
        self.results = []
        
    def run_test_case(self, case_name, algorithms=None):
        """Run a specific test case with selected algorithms"""
        if case_name not in TEST_CASES:
            print(f"❌ Test case '{case_name}' not found")
            return None
            
        test_case = TEST_CASES[case_name]
        if algorithms is None:
            algorithms = list(test_case["expected_results"].keys())
            
        print(f"\n🧪 Running Test Case: {test_case['name']}")
        print(f"📝 Description: {test_case['description']}")
        
        case_results = {
            "test_case": case_name,
            "timestamp": datetime.now().isoformat(),
            "algorithm_results": {}
        }
        
        for algorithm in algorithms:
            print(f"\n🔄 Testing {algorithm.upper()}...")
            
            # Simulate running the algorithm with test case parameters
            result = self._simulate_algorithm_run(test_case, algorithm)
            
            # Validate results
            validation = validate_results(case_name, algorithm, result)
            
            case_results["algorithm_results"][algorithm] = {
                "simulation_results": result,
                "validation": validation,
                "status": "✅ PASSED" if validation["valid"] else "❌ FAILED"
            }
            
            print(f"   📊 Coverage: {result.get('final_coverage', 0):.1f}%")
            print(f"   🔢 Iterations: {result.get('iterations', 0)}")
            print(f"   ⏱️ Time: {result.get('execution_time', 0):.2f}s")
            print(f"   {case_results['algorithm_results'][algorithm]['status']}")
            
        self.results.append(case_results)
        return case_results
    
    def _simulate_algorithm_run(self, test_case, algorithm):
        """Simulate algorithm execution with test case parameters"""
        # This would integrate with your actual dashboard
        # For now, simulate realistic results based on algorithm characteristics
        
        env = test_case["environment"]
        criteria = test_case["stopping_criteria"]
        
        # Algorithm-specific base performance
        base_performance = {
            "greedy": {"coverage": 60, "speed": 1.5},
            "ga": {"coverage": 65, "speed": 0.8},
            "pso": {"coverage": 70, "speed": 1.2},
            "sa": {"coverage": 62, "speed": 0.6},
            "ga_sa": {"coverage": 75, "speed": 0.5},
            "gwo": {"coverage": 68, "speed": 0.9},
            "mrfo": {"coverage": 72, "speed": 0.7}
        }
        
        # Simulate execution time
        start_time = time.time()
        time.sleep(0.1)  # Simulate processing
        execution_time = time.time() - start_time
        
        # Calculate simulated results
        base = base_performance.get(algorithm, {"coverage": 65, "speed": 1.0})
        area_factor = (env["grid_width"] * env["grid_height"]) / 2500  # Normalize to 50x50
        drone_factor = env["num_drones"] / 15  # Normalize to 15 drones
        
        final_coverage = base["coverage"] * (1 + 0.1 * drone_factor) * (1 - 0.05 * area_factor)
        final_coverage = max(10, min(95, final_coverage))
        
        max_iter = criteria["max_iterations"]
        if criteria.get("enable_early_stopping", True):
            iterations = min(max_iter, int(max_iter * 0.3 + 50))
        else:
            iterations = max_iter
            
        return {
            "algorithm": algorithm,
            "final_coverage": final_coverage,
            "iterations": iterations,
            "execution_time": execution_time,
            "stopping_reason": "Target achieved" if final_coverage >= criteria["target_coverage"] else "Converged",
            "environment": env,
            "stopping_criteria": criteria
        }
    
    def run_all_test_cases(self):
        """Run all predefined test cases"""
        print("🚀 Starting Complete Test Suite")
        print("=" * 50)
        
        for case_name in TEST_CASES.keys():
            self.run_test_case(case_name)
            
        self._generate_summary_report()
        
    def run_algorithm_comparison(self, case_name):
        """Run all algorithms on a specific test case for comparison"""
        if case_name not in TEST_CASES:
            print(f"❌ Test case '{case_name}' not found")
            return
            
        algorithms = ["greedy", "ga", "pso", "sa", "ga_sa", "gwo", "mrfo"]
        return self.run_test_case(case_name, algorithms)
    
    def _generate_summary_report(self):
        """Generate a comprehensive test report"""
        if not self.results:
            print("No test results to report")
            return
            
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = sum(len(result["algorithm_results"]) for result in self.results)
        passed_tests = sum(
            1 for result in self.results 
            for alg_result in result["algorithm_results"].values() 
            if alg_result["validation"]["valid"]
        )
        
        print(f"📈 Overall Success Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
        
        # Create detailed report
        report_data = []
        for result in self.results:
            case_name = result["test_case"]
            for algorithm, alg_result in result["algorithm_results"].items():
                sim_result = alg_result["simulation_results"]
                validation = alg_result["validation"]
                
                report_data.append({
                    "Test Case": case_name,
                    "Algorithm": algorithm.upper(),
                    "Coverage (%)": f"{sim_result['final_coverage']:.1f}",
                    "Iterations": sim_result["iterations"],
                    "Time (s)": f"{sim_result['execution_time']:.2f}",
                    "Status": "PASSED" if validation["valid"] else "FAILED",
                    "Expected Coverage": f"{validation['expected_coverage'][0]}-{validation['expected_coverage'][1]}%"
                })
        
        df = pd.DataFrame(report_data)
        print("\n📋 Detailed Results:")
        print(df.to_string(index=False))
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"\n💾 Report saved to: {filename}")
        
        return df

def main():
    """Interactive test runner"""
    runner = DroneTestRunner()
    
    print("🎯 Drone Optimization Test Runner")
    print("Available options:")
    print("1. Run specific test case")
    print("2. Run algorithm comparison")
    print("3. Run all test cases")
    print("4. List available test cases")
    
    while True:
        choice = input("\nEnter your choice (1-4, 'q' to quit): ").strip()
        
        if choice == 'q':
            break
        elif choice == '1':
            case_name = input("Enter test case name: ").strip()
            algorithms = input("Enter algorithms (comma-separated, or 'all'): ").strip()
            if algorithms.lower() == 'all':
                algorithms = None
            else:
                algorithms = [alg.strip() for alg in algorithms.split(',')]
            runner.run_test_case(case_name, algorithms)
            
        elif choice == '2':
            case_name = input("Enter test case name: ").strip()
            runner.run_algorithm_comparison(case_name)
            
        elif choice == '3':
            runner.run_all_test_cases()
            
        elif choice == '4':
            print("\n📋 Available Test Cases:")
            for key, test_case in TEST_CASES.items():
                print(f"  {key}: {test_case['name']}")
                print(f"    {test_case['description']}")
                
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
