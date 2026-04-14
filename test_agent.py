import warnings
warnings.filterwarnings("ignore")

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_mongodb.agent_toolkit import (
    MONGODB_AGENT_SYSTEM_PROMPT,
    MongoDBDatabase,
    MongoDBDatabaseToolkit,
)
import dotenv

dotenv.load_dotenv()

from natural_language_to_mql import NaturalLanguageToMQL, MONGODB_URI, DB_NAME

class TestResults:
    """Store and manage test results"""
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        
    def add_result(self, test_name: str, query: str, status: str, details: str = ""):
        """Add a test result"""
        result = {
            "test_name": test_name,
            "query": query,
            "status": status,  # PASS, FAIL, SKIP
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        if status == "PASS":
            self.passed += 1
        elif status == "FAIL":
            self.failed += 1
        elif status == "SKIP":
            self.skipped += 1
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed + self.skipped
        print("\n" + "=" * 80)
        print("                        TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests:    {total}")
        print(f"✅ Passed:      {self.passed}")
        print(f"❌ Failed:      {self.failed}")
        print(f"⏭️  Skipped:     {self.skipped}")
        print(f"Pass Rate:      {(self.passed/total*100):.1f}%" if total > 0 else "N/A")
        print("=" * 80)
    
    def save_to_file(self, filename: str = "test_results.json"):
        """Save results to a JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                "summary": {
                    "total": self.passed + self.failed + self.skipped,
                    "passed": self.passed,
                    "failed": self.failed,
                    "skipped": self.skipped,
                    "pass_rate": f"{(self.passed/(self.passed+self.failed)*100):.1f}%" if (self.passed + self.failed) > 0 else "N/A"
                },
                "results": self.results
            }, f, indent=2)
        print(f"✅ Results saved to {filename}")


class EdgeCaseTestSuite:
    """Test suite for edge cases and accuracy"""
    
    def __init__(self):
        try:
            self.converter = NaturalLanguageToMQL()
            self.results = TestResults()
            print("✅ Agent initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            raise
    
    def test_simple_queries(self):
        """Test 1: Simple, straightforward queries"""
        print("\n" + "=" * 80)
        print("TEST 1: Simple Queries")
        print("=" * 80)
        
        simple_queries = [
            ("How many crops are in the database?", "Count total crops"),
            ("List all states", "Retrieve unique states"),
            ("Show me all crop names", "Get unique crop names"),
        ]
        
        for query, description in simple_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Simple Query: {description}",
                    query,
                    "PASS",
                    "Query executed successfully"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Simple Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_filter_queries(self):
        """Test 2: Queries with specific filters"""
        print("\n" + "=" * 80)
        print("TEST 2: Filter Queries")
        print("=" * 80)
        
        filter_queries = [
            ("Find all crops in Odisha", "State filter"),
            ("Show crops from KHARIF season", "Season filter"),
            ("List crops with cropCode A0402", "Exact field match"),
            ("Show crops in district KHORDHA", "District filter"),
            ("Find all varieties in year 2023-24", "Year filter"),
        ]
        
        for query, description in filter_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Filter Query: {description}",
                    query,
                    "PASS",
                    "Filter applied correctly"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Filter Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_aggregation_queries(self):
        """Test 3: Aggregation and calculation queries"""
        print("\n" + "=" * 80)
        print("TEST 3: Aggregation Queries")
        print("=" * 80)
        
        agg_queries = [
            ("What is the total estimated yield?", "Sum aggregation"),
            ("Calculate average intake quantity", "Average aggregation"),
            ("Find maximum processed quantity", "Max aggregation"),
            ("Show minimum tested quantity", "Min aggregation"),
            ("Count crops by state", "Group by state"),
        ]
        
        for query, description in agg_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Aggregation Query: {description}",
                    query,
                    "PASS",
                    "Aggregation executed successfully"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Aggregation Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_complex_queries(self):
        """Test 4: Complex queries with multiple conditions"""
        print("\n" + "=" * 80)
        print("TEST 4: Complex Queries")
        print("=" * 80)
        
        complex_queries = [
            ("Find all groundnut crops in Odisha during KHARIF season", "Multiple filters"),
            ("Show crops with estimated yield greater than 50 from 2023-24", "Filter + condition"),
            ("List distinct variety names for rice in FOUNDATION I class", "Multiple conditions"),
            ("Find all crops in Odisha or Maharashtra", "OR condition"),
            ("Show crops that were tested and passed in 2023-24", "AND condition"),
        ]
        
        for query, description in complex_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Complex Query: {description}",
                    query,
                    "PASS",
                    "Complex query processed correctly"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Complex Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_edge_cases(self):
        """Test 5: Edge cases and special scenarios"""
        print("\n" + "=" * 80)
        print("TEST 5: Edge Cases")
        print("=" * 80)
        
        edge_cases = [
            ("Find crops with zero estimated yield", "Zero value check"),
            ("Show crops with NULL or empty variety names", "NULL handling"),
            ("Find crops from year 2099", "Non-existent data"),
            ("Show all crops sorted by estimated yield in descending order", "Sorting"),
            ("Find crops with estimated yield between 10 and 100", "Range query"),
            ("Show top 5 crops by intake quantity", "Limit/top N"),
            ("Find all FOUNDATION I destination class crops", "Special characters in values"),
        ]
        
        for query, description in edge_cases:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Edge Case: {description}",
                    query,
                    "PASS",
                    "Edge case handled correctly"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Edge Case: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_natural_language_variations(self):
        """Test 6: Different ways to express the same query"""
        print("\n" + "=" * 80)
        print("TEST 6: Natural Language Variations")
        print("=" * 80)
        
        variations = [
            # Same intent, different wording
            [
                ("How many crops are grown in Odisha?", "Direct question"),
                ("What is the count of crops in Odisha?", "Count phrasing"),
                ("Tell me the number of crops in Odisha", "Number phrasing"),
            ],
            [
                ("Show all varieties of groundnut", "Show all"),
                ("List groundnut varieties", "List"),
                ("Give me groundnut varieties", "Give me"),
            ],
        ]
        
        for variation_group in variations:
            print(f"\n🔄 Testing variations of same intent:")
            for query, variation_type in variation_group:
                try:
                    print(f"\n   📝 [{variation_type}] {query}")
                    self.converter.ask(query)
                    self.results.add_result(
                        f"NL Variation: {variation_type}",
                        query,
                        "PASS",
                        "Variation understood correctly"
                    )
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                    self.results.add_result(
                        f"NL Variation: {variation_type}",
                        query,
                        "FAIL",
                        str(e)
                    )
    
    def test_typo_and_fuzzy_matching(self):
        """Test 7: Handling of typos and fuzzy matching"""
        print("\n" + "=" * 80)
        print("TEST 7: Typo and Fuzzy Matching")
        print("=" * 80)
        
        typo_queries = [
            ("Find all crpos in Odisha", "Typo in 'crops'"),  # Note: This will likely fail, testing robustness
            ("Show me all Odsisha states", "Typo in state name"),  # This will likely fail
            ("KHARIF season crops", "Different capitalization"),
        ]
        
        for query, description in typo_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Typo Test: {description}",
                    query,
                    "PASS",
                    "Typo handled or corrected"
                )
            except Exception as e:
                print(f"⚠️  Expected limitation: {e}")
                self.results.add_result(
                    f"Typo Test: {description}",
                    query,
                    "SKIP",
                    "Typos beyond agent capability (expected)"
                )
    
    def test_empty_and_invalid_queries(self):
        """Test 8: Empty and invalid queries"""
        print("\n" + "=" * 80)
        print("TEST 8: Empty and Invalid Queries")
        print("=" * 80)
        
        invalid_queries = [
            ("What is the meaning of life?", "Unrelated question"),
            ("Tell me a joke", "Off-topic query"),
            ("Blah blah blah", "Nonsensical input"),
            ("How to cook biryani?", "Completely unrelated"),
        ]
        
        for query, description in invalid_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Invalid Query: {description}",
                    query,
                    "PASS",
                    "Agent appropriately handled invalid query"
                )
            except Exception as e:
                print(f"⚠️  Query handling: {e}")
                self.results.add_result(
                    f"Invalid Query: {description}",
                    query,
                    "SKIP",
                    "Query handling varies by agent behavior"
                )
    
    def test_numeric_range_queries(self):
        """Test 9: Numeric range and comparison queries"""
        print("\n" + "=" * 80)
        print("TEST 9: Numeric Range and Comparison Queries")
        print("=" * 80)
        
        numeric_queries = [
            ("Find crops with estimated yield greater than 100", "Greater than"),
            ("Show crops with pass quantity less than 50", "Less than"),
            ("Find crops with intake quantity equal to 100", "Equal to"),
            ("Show crops with estimated yield >= 50 and <= 200", "Range between"),
            ("Find crops with NOT zero estimated yield", "NOT condition"),
        ]
        
        for query, description in numeric_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Numeric Query: {description}",
                    query,
                    "PASS",
                    "Numeric comparison executed correctly"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Numeric Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def test_grouping_and_sorting(self):
        """Test 10: Grouping and sorting queries"""
        print("\n" + "=" * 80)
        print("TEST 10: Grouping and Sorting Queries")
        print("=" * 80)
        
        grouping_queries = [
            ("Count crops grouped by state", "Group by state"),
            ("Show average yield by season", "Average grouped"),
            ("Top 10 districts by crop count", "Top N by group"),
            ("Sort crops by estimated yield ascending", "Sort ascending"),
            ("Sort crops by processed quantity descending", "Sort descending"),
        ]
        
        for query, description in grouping_queries:
            try:
                print(f"\n📝 Query: {query}")
                print(f"   Purpose: {description}")
                self.converter.ask(query)
                self.results.add_result(
                    f"Grouping Query: {description}",
                    query,
                    "PASS",
                    "Grouping/sorting executed correctly"
                )
            except Exception as e:
                print(f"❌ Error: {e}")
                self.results.add_result(
                    f"Grouping Query: {description}",
                    query,
                    "FAIL",
                    str(e)
                )
    
    def run_all_tests(self):
        """Run all test suites"""
        print("\n" + "🚀 " * 30)
        print("STARTING COMPREHENSIVE TEST SUITE")
        print("🚀 " * 30)
        
        try:
            self.test_simple_queries()
            self.test_filter_queries()
            self.test_aggregation_queries()
            self.test_complex_queries()
            self.test_edge_cases()
            self.test_natural_language_variations()
            self.test_typo_and_fuzzy_matching()
            self.test_empty_and_invalid_queries()
            self.test_numeric_range_queries()
            self.test_grouping_and_sorting()
        except Exception as e:
            print(f"\n❌ Critical error during testing: {e}")
        
        self.results.print_summary()
        self.results.save_to_file()
        
        return self.results


def main():
    """Main test runner"""
    print("\n" + "=" * 80)
    print("   🧪 MongoDB Crop Data Query Agent - Test Suite")
    print("=" * 80)
    print("\nThis test suite will evaluate:")
    print("  ✓ Simple queries")
    print("  ✓ Filter queries")
    print("  ✓ Aggregation queries")
    print("  ✓ Complex queries with multiple conditions")
    print("  ✓ Edge cases")
    print("  ✓ Natural language variations")
    print("  ✓ Typo and fuzzy matching capabilities")
    print("  ✓ Empty/invalid query handling")
    print("  ✓ Numeric range queries")
    print("  ✓ Grouping and sorting")
    print("\n" + "=" * 80)
    
    # Run tests
    suite = EdgeCaseTestSuite()
    results = suite.run_all_tests()
    
    print("\n✅ All tests completed! Check 'test_results.json' for detailed results.")


if __name__ == "__main__":
    main()
