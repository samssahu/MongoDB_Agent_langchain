"""
Comprehensive Testing Suite with Confusion Matrix Metrics
Tests: Simple, Filter, Aggregation (SUM, AVG, MIN, MAX), Complex, Edge Cases
Metrics: TP, TN, FP, FN, Accuracy, Precision, Recall, F1-Score
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings("ignore")

# Fix Unicode encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from natural_language_to_mql import NaturalLanguageToMQL

class ConfusionMatrixMetrics:
    """Calculate confusion matrix metrics"""
    
    def __init__(self):
        self.tp = 0  # True Positive - Correct answer provided
        self.tn = 0  # True Negative - Correctly identified as not available
        self.fp = 0  # False Positive - Incorrect answer provided
        self.fn = 0  # False Negative - Should have answered but didn't
    
    def add_result(self, query: str, expected_type: str, result_status: str):
        """
        Add test result
        expected_type: 'valid', 'invalid'
        result_status: 'correct', 'incorrect', 'no_answer'
        """
        if expected_type == 'valid' and result_status == 'correct':
            self.tp += 1
        elif expected_type == 'valid' and result_status == 'incorrect':
            self.fp += 1
        elif expected_type == 'valid' and result_status == 'no_answer':
            self.fn += 1
        elif expected_type == 'invalid' and result_status == 'no_answer':
            self.tn += 1
        elif expected_type == 'invalid' and result_status == 'incorrect':
            self.fp += 1
    
    def get_accuracy(self):
        """Accuracy = (TP + TN) / (TP + TN + FP + FN)"""
        total = self.tp + self.tn + self.fp + self.fn
        if total == 0:
            return 0
        return (self.tp + self.tn) / total * 100
    
    def get_precision(self):
        """Precision = TP / (TP + FP)"""
        if (self.tp + self.fp) == 0:
            return 0
        return self.tp / (self.tp + self.fp) * 100
    
    def get_recall(self):
        """Recall = TP / (TP + FN)"""
        if (self.tp + self.fn) == 0:
            return 0
        return self.tp / (self.tp + self.fn) * 100
    
    def get_f1_score(self):
        """F1 = 2 * (Precision * Recall) / (Precision + Recall)"""
        precision = self.get_precision()
        recall = self.get_recall()
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)
    
    def get_specificity(self):
        """Specificity = TN / (TN + FP)"""
        if (self.tn + self.fp) == 0:
            return 0
        return self.tn / (self.tn + self.fp) * 100


class ComprehensiveTestSuite:
    """Complete test suite with all query types"""
    
    def __init__(self):
        try:
            self.converter = NaturalLanguageToMQL()
            self.metrics = ConfusionMatrixMetrics()
            self.results = []
            print("✅ Agent initialized successfully\n")
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            raise
    
    def test_query(self, query: str, query_type: str, expected_success: bool = True):
        """Test a single query"""
        try:
            print(f"📝 Query: {query}")
            print(f"   Type: {query_type}")
            
            # Capture answer
            self.converter.ask(query)
            
            # Determine if answer was successful
            last_answer = self.converter.messages[-1].content if self.converter.messages else ""
            
            is_no_data = "not available" in last_answer.lower() or "no" in last_answer.lower()[:20]
            
            if expected_success and not is_no_data and len(last_answer) > 10:
                status = "PASS"
                result_status = "correct"
                self.metrics.add_result(query, 'valid', 'correct')
                print("   ✅ PASS: Correct answer provided\n")
            elif not expected_success and is_no_data:
                status = "PASS"
                result_status = "no_answer"
                self.metrics.add_result(query, 'invalid', 'no_answer')
                print("   ✅ PASS: Correctly identified as not available\n")
            else:
                status = "FAIL"
                result_status = "incorrect" if expected_success else "no_answer"
                print(f"   ❌ FAIL: Unexpected response\n")
                if expected_success:
                    self.metrics.add_result(query, 'valid', 'incorrect')
                else:
                    self.metrics.add_result(query, 'invalid', result_status)
            
            self.results.append({
                "query": query,
                "type": query_type,
                "status": status,
                "expected": expected_success,
                "result_status": result_status
            })
            
        except Exception as e:
            print(f"   ⚠️  Error: {str(e)[:100]}")
            print("   ❌ FAIL: Exception occurred\n")
            self.results.append({
                "query": query,
                "type": query_type,
                "status": "FAIL",
                "expected": expected_success,
                "result_status": "error"
            })
            self.metrics.add_result(query, 'valid' if expected_success else 'invalid', 'incorrect')
    
    def run_all_tests(self):
        """Run all test categories"""
        print("\n" + "=" * 80)
        print("   🧪 COMPREHENSIVE TESTING SUITE WITH CONFUSION MATRIX METRICS")
        print("=" * 80)
        
        # ===== CATEGORY 1: SIMPLE QUERIES =====
        print("\n" + "=" * 80)
        print("TEST 1: SIMPLE QUERIES")
        print("=" * 80 + "\n")
        
        simple_queries = [
            ("Find all crops in the database", "simple_filter", True),
            ("Show me all states", "simple_distinct", True),
            ("List unique seasons", "simple_distinct", True),
        ]
        
        for query, qtype, expected in simple_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 2: FILTER QUERIES =====
        print("\n" + "=" * 80)
        print("TEST 2: FILTER QUERIES")
        print("=" * 80 + "\n")
        
        filter_queries = [
            ("Find all crops in Odisha", "filter_state", True),
            ("Show crops from KHARIF season", "filter_season", True),
            ("List crops with cropCode A0402", "filter_exact", True),
            ("Show crops in district KHORDHA", "filter_district", True),
            ("Find crops from year 2023-24", "filter_year", True),
        ]
        
        for query, qtype, expected in filter_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 3: AGGREGATION QUERIES - SUM =====
        print("\n" + "=" * 80)
        print("TEST 3: AGGREGATION - SUM QUERIES")
        print("=" * 80 + "\n")
        
        sum_queries = [
            ("What is the total estimated yield of all crops?", "aggregation_sum", True),
            ("Calculate total intake quantity", "aggregation_sum", True),
            ("Sum of all processed quantity", "aggregation_sum", True),
            ("Total tested quantity across all crops", "aggregation_sum", True),
        ]
        
        for query, qtype, expected in sum_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 4: AGGREGATION QUERIES - AVERAGE =====
        print("\n" + "=" * 80)
        print("TEST 4: AGGREGATION - AVERAGE QUERIES")
        print("=" * 80 + "\n")
        
        avg_queries = [
            ("What is the average estimated yield?", "aggregation_avg", True),
            ("Calculate average intake quantity", "aggregation_avg", True),
            ("What is the mean processed quantity?", "aggregation_avg", True),
            ("Average tested quantity", "aggregation_avg", True),
        ]
        
        for query, qtype, expected in avg_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 5: AGGREGATION QUERIES - MIN/MAX =====
        print("\n" + "=" * 80)
        print("TEST 5: AGGREGATION - MIN/MAX QUERIES")
        print("=" * 80 + "\n")
        
        minmax_queries = [
            ("What is the maximum estimated yield?", "aggregation_max", True),
            ("Find minimum intake quantity", "aggregation_min", True),
            ("Show maximum processed quantity", "aggregation_max", True),
            ("What is the minimum tested quantity?", "aggregation_min", True),
            ("Find the highest pass quantity", "aggregation_max", True),
            ("Show the lowest yield value", "aggregation_min", True),
        ]
        
        for query, qtype, expected in minmax_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 6: COMPLEX QUERIES =====
        print("\n" + "=" * 80)
        print("TEST 6: COMPLEX QUERIES")
        print("=" * 80 + "\n")
        
        complex_queries = [
            ("Find all groundnut crops in Odisha", "complex_multi_filter", True),
            ("Show crops with estimated yield greater than 50", "complex_comparison", True),
            ("List crops from KHARIF 2023 in Odisha", "complex_multi_filter", True),
            ("Find crops with pass quantity less than 100", "complex_comparison", True),
            ("Show crops between year 2022-23 and 2023-24", "complex_range", True),
        ]
        
        for query, qtype, expected in complex_queries:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 7: EDGE CASES =====
        print("\n" + "=" * 80)
        print("TEST 7: EDGE CASES")
        print("=" * 80 + "\n")
        
        edge_cases = [
            ("Find crops with zero estimated yield", "edge_zero", True),
            ("Show crops from year 2099", "edge_nonexistent", True),
            ("Find crops sorted by estimated yield", "edge_sorting", True),
            ("Show top 5 crops by intake quantity", "edge_limit", True),
            ("Find FOUNDATION I destination class crops", "edge_special_chars", True),
        ]
        
        for query, qtype, expected in edge_cases:
            self.test_query(query, qtype, expected)
        
        # ===== CATEGORY 8: INVALID QUERIES =====
        print("\n" + "=" * 80)
        print("TEST 8: INVALID/OUT-OF-SCOPE QUERIES")
        print("=" * 80 + "\n")
        
        invalid_queries = [
            ("What is the capital of France?", "invalid_general", False),
            ("Tell me a joke about programming", "invalid_general", False),
            ("How do I cook biryani?", "invalid_general", False),
            ("What is 2+2?", "invalid_math", False),
            ("Who is the president of India?", "invalid_general", False),
        ]
        
        for query, qtype, expected in invalid_queries:
            self.test_query(query, qtype, expected)
        
        print("\n" + "=" * 80)
        print("   ✅ ALL TESTS COMPLETED")
        print("=" * 80)
        
        return self.results


def main():
    """Main execution"""
    suite = ComprehensiveTestSuite()
    results = suite.run_all_tests()
    
    # Print Confusion Matrix Summary
    print("\n" + "=" * 80)
    print("   📊 CONFUSION MATRIX METRICS")
    print("=" * 80)
    
    print(f"\nTrue Positives (TP):   {suite.metrics.tp}")
    print(f"True Negatives (TN):   {suite.metrics.tn}")
    print(f"False Positives (FP):  {suite.metrics.fp}")
    print(f"False Negatives (FN):  {suite.metrics.fn}")
    
    total = suite.metrics.tp + suite.metrics.tn + suite.metrics.fp + suite.metrics.fn
    print(f"\nTotal Tests: {total}")
    
    # Print Performance Metrics
    print("\n" + "-" * 80)
    print("   📈 PERFORMANCE METRICS")
    print("-" * 80)
    
    accuracy = suite.metrics.get_accuracy()
    precision = suite.metrics.get_precision()
    recall = suite.metrics.get_recall()
    f1 = suite.metrics.get_f1_score()
    specificity = suite.metrics.get_specificity()
    
    print(f"\n✅ Accuracy:     {accuracy:.2f}%")
    print(f"✅ Precision:    {precision:.2f}%")
    print(f"✅ Recall:       {recall:.2f}%")
    print(f"✅ F1-Score:     {f1:.2f}%")
    print(f"✅ Specificity:  {specificity:.2f}%")
    
    # Print Detailed Results by Category
    print("\n" + "=" * 80)
    print("   📋 DETAILED RESULTS BY CATEGORY")
    print("=" * 80)
    
    categories = {}
    for result in results:
        cat = result['type'].split('_')[0]
        if cat not in categories:
            categories[cat] = {'total': 0, 'passed': 0}
        categories[cat]['total'] += 1
        if result['status'] == 'PASS':
            categories[cat]['passed'] += 1
    
    for cat in sorted(categories.keys()):
        total = categories[cat]['total']
        passed = categories[cat]['passed']
        rate = (passed / total * 100) if total > 0 else 0
        print(f"\n{cat.upper()}:")
        print(f"   Passed: {passed}/{total} ({rate:.1f}%)")
    
    # Save comprehensive report
    report = {
        "timestamp": datetime.now().isoformat(),
        "confusion_matrix": {
            "TP": suite.metrics.tp,
            "TN": suite.metrics.tn,
            "FP": suite.metrics.fp,
            "FN": suite.metrics.fn,
            "total": total
        },
        "performance_metrics": {
            "accuracy": round(accuracy, 2),
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1, 2),
            "specificity": round(specificity, 2)
        },
        "results": results,
        "category_summary": categories
    }
    
    # Save report
    with open("comprehensive_test_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ Comprehensive report saved to: comprehensive_test_report.json")
    print("=" * 80)
    
    return report


if __name__ == "__main__":
    main()
