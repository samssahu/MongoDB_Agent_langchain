import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import seaborn as sns


class AccuracyAnalyzer:
    """Analyze and visualize test accuracy metrics"""
    
    def __init__(self, results_file: str = "test_results.json"):
        self.results_file = results_file
        self.data = self.load_results()
        
    def load_results(self) -> Dict[str, Any]:
        """Load test results from JSON file"""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Results file '{self.results_file}' not found. Run tests first.")
            return None
    
    def print_detailed_report(self):
        """Print detailed test report"""
        if not self.data:
            return
        
        print("\n" + "=" * 100)
        print("                        DETAILED TEST REPORT")
        print("=" * 100)
        
        summary = self.data.get("summary", {})
        print("\n📊 SUMMARY STATISTICS:")
        print(f"   Total Tests:     {summary.get('total', 0)}")
        print(f"   ✅ Passed:       {summary.get('passed', 0)}")
        print(f"   ❌ Failed:       {summary.get('failed', 0)}")
        print(f"   ⏭️  Skipped:      {summary.get('skipped', 0)}")
        print(f"   Pass Rate:       {summary.get('pass_rate', 'N/A')}")
        
        results = self.data.get("results", [])
        
        # Group by test category
        categories = {}
        for result in results:
            test_name = result.get("test_name", "Unknown")
            category = test_name.split(":")[0].strip()
            
            if category not in categories:
                categories[category] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "tests": []
                }
            
            categories[category]["total"] += 1
            status = result.get("status", "UNKNOWN")
            if status == "PASS":
                categories[category]["passed"] += 1
            elif status == "FAIL":
                categories[category]["failed"] += 1
            elif status == "SKIP":
                categories[category]["skipped"] += 1
            
            categories[category]["tests"].append(result)
        
        # Print by category
        print("\n📋 RESULTS BY CATEGORY:")
        print("-" * 100)
        
        for category, cat_data in sorted(categories.items()):
            total = cat_data["total"]
            passed = cat_data["passed"]
            failed = cat_data["failed"]
            skipped = cat_data["skipped"]
            rate = (passed / total * 100) if total > 0 else 0
            
            print(f"\n{category}:")
            print(f"   Total:  {total} | ✅ Passed: {passed} | ❌ Failed: {failed} | ⏭️  Skipped: {skipped}")
            print(f"   Success Rate: {rate:.1f}%")
            
            # Print individual tests
            for test in cat_data["tests"]:
                status_icon = "✅" if test["status"] == "PASS" else ("❌" if test["status"] == "FAIL" else "⏭️")
                print(f"   {status_icon} {test['test_name']}")
                if test.get("details"):
                    print(f"      Details: {test['details']}")
        
        print("\n" + "=" * 100)
    
    def print_accuracy_metrics(self):
        """Print accuracy metrics"""
        if not self.data:
            return
        
        results = self.data.get("results", [])
        summary = self.data.get("summary", {})
        
        print("\n" + "=" * 100)
        print("                        ACCURACY METRICS")
        print("=" * 100)
        
        # Calculate metrics by test type
        test_types = {}
        for result in results:
            test_name = result.get("test_name", "")
            # Extract test type
            if "Simple Query" in test_name:
                test_type = "Simple Query"
            elif "Filter Query" in test_name:
                test_type = "Filter Query"
            elif "Aggregation Query" in test_name:
                test_type = "Aggregation Query"
            elif "Complex Query" in test_name:
                test_type = "Complex Query"
            elif "Edge Case" in test_name:
                test_type = "Edge Case"
            elif "NL Variation" in test_name:
                test_type = "NL Variation"
            elif "Typo Test" in test_name:
                test_type = "Typo Test"
            elif "Invalid Query" in test_name:
                test_type = "Invalid Query"
            elif "Numeric Query" in test_name:
                test_type = "Numeric Query"
            elif "Grouping Query" in test_name:
                test_type = "Grouping Query"
            else:
                test_type = "Other"
            
            if test_type not in test_types:
                test_types[test_type] = {"passed": 0, "total": 0, "details": []}
            
            test_types[test_type]["total"] += 1
            if result["status"] == "PASS":
                test_types[test_type]["passed"] += 1
            
            test_types[test_type]["details"].append(result)
        
        # Print metrics
        print("\n🎯 ACCURACY BY TEST TYPE:")
        print("-" * 100)
        print(f"{'Test Type':<25} {'Accuracy':<15} {'Passed':<10} {'Total':<10}")
        print("-" * 100)
        
        for test_type in sorted(test_types.keys()):
            data = test_types[test_type]
            accuracy = (data["passed"] / data["total"] * 100) if data["total"] > 0 else 0
            print(f"{test_type:<25} {accuracy:>6.1f}%{'':<8} {data['passed']:>5}/{data['total']:<4}")
        
        print("\n" + "=" * 100)
    
    def print_failure_analysis(self):
        """Print analysis of failures"""
        if not self.data:
            return
        
        results = self.data.get("results", [])
        failures = [r for r in results if r["status"] == "FAIL"]
        
        if not failures:
            print("\n✅ No failures found!")
            return
        
        print("\n" + "=" * 100)
        print("                        FAILURE ANALYSIS")
        print("=" * 100)
        print(f"\nFound {len(failures)} failure(s):\n")
        
        for i, failure in enumerate(failures, 1):
            print(f"{i}. {failure['test_name']}")
            print(f"   Query: {failure['query']}")
            print(f"   Error: {failure['details']}")
            print()
        
        print("=" * 100)
    
    def generate_report(self):
        """Generate comprehensive report"""
        self.print_detailed_report()
        self.print_accuracy_metrics()
        self.print_failure_analysis()
    
    def export_to_csv(self, filename: str = "test_results.csv"):
        """Export results to CSV"""
        if not self.data:
            return
        
        results = self.data.get("results", [])
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False)
        print(f"\n✅ Results exported to {filename}")
    
    def create_visualizations(self, output_dir: str = "."):
        """Create visualization charts"""
        if not self.data:
            return
        
        results = self.data.get("results", [])
        summary = self.data.get("summary", {})
        
        # 1. Overall Pass/Fail/Skip Distribution
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('MongoDB Agent Test Suite - Accuracy Analysis', fontsize=16, fontweight='bold')
        
        # Chart 1: Overall distribution
        statuses = [r["status"] for r in results]
        status_counts = {
            "PASS": statuses.count("PASS"),
            "FAIL": statuses.count("FAIL"),
            "SKIP": statuses.count("SKIP")
        }
        colors = ["#2ecc71", "#e74c3c", "#f39c12"]
        axes[0, 0].pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%',
                       colors=colors, startangle=90)
        axes[0, 0].set_title('Overall Test Results Distribution')
        
        # Chart 2: Pass rate by category
        categories = {}
        for result in results:
            category = result.get("test_name", "").split(":")[0].strip()
            if category not in categories:
                categories[category] = {"passed": 0, "total": 0}
            categories[category]["total"] += 1
            if result["status"] == "PASS":
                categories[category]["passed"] += 1
        
        cat_names = list(categories.keys())
        cat_rates = [(categories[c]["passed"] / categories[c]["total"] * 100) if categories[c]["total"] > 0 else 0
                     for c in cat_names]
        
        axes[0, 1].bar(range(len(cat_names)), cat_rates, color=["#2ecc71" if x == 100 else "#f39c12" if x >= 50 else "#e74c3c" 
                                                                  for x in cat_rates])
        axes[0, 1].set_xticks(range(len(cat_names)))
        axes[0, 1].set_xticklabels(cat_names, rotation=45, ha='right')
        axes[0, 1].set_ylabel('Pass Rate (%)')
        axes[0, 1].set_title('Pass Rate by Test Category')
        axes[0, 1].axhline(y=100, color='g', linestyle='--', alpha=0.3)
        axes[0, 1].set_ylim(0, 105)
        
        # Chart 3: Test count by category
        axes[1, 0].barh(cat_names, [categories[c]["total"] for c in cat_names], color="#3498db")
        axes[1, 0].set_xlabel('Number of Tests')
        axes[1, 0].set_title('Test Count by Category')
        
        # Chart 4: Summary statistics
        axes[1, 1].axis('off')
        summary_text = f"""
Test Summary Statistics

Total Tests: {summary.get('total', 0)}
✅ Passed: {summary.get('passed', 0)}
❌ Failed: {summary.get('failed', 0)}
⏭️ Skipped: {summary.get('skipped', 0)}

Overall Pass Rate: {summary.get('pass_rate', 'N/A')}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        axes[1, 1].text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
                       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/test_results_visualization.png", dpi=300, bbox_inches='tight')
        print(f"\n✅ Visualization saved to {output_dir}/test_results_visualization.png")
        plt.close()


def main():
    """Main analysis runner"""
    print("\n" + "=" * 100)
    print("   📊 MongoDB Agent Test Analysis")
    print("=" * 100)
    
    analyzer = AccuracyAnalyzer("test_results.json")
    
    if analyzer.data:
        analyzer.generate_report()
        
        # Try to export and visualize
        try:
            analyzer.export_to_csv()
        except Exception as e:
            print(f"\n⚠️  Could not export to CSV: {e}")
        
        try:
            analyzer.create_visualizations()
        except Exception as e:
            print(f"\n⚠️  Could not create visualizations: {e}")
    else:
        print("\n❌ No test results found. Please run test_agent.py first.")


if __name__ == "__main__":
    main()
