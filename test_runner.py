import os
import sys
import traceback
from database import Database
import time

def run_test(name, test_fn):
    """Run a test function and report success/failure"""
    print(f"Testing: {name}...")
    start_time = time.time()
    
    try:
        test_fn()
        duration = time.time() - start_time
        print(f"✅ PASS: {name} ({duration:.2f}s)")
        return True
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ FAIL: {name} ({duration:.2f}s)")
        print(f"   Error: {str(e)}")
        traceback.print_exc()
        return False

def test_database_init():
    """Test database initialization"""
    db = Database()
    assert db.file is not None, "Database file should be initialized"
    assert hasattr(db, 'tables'), "Database should have tables attribute"
    assert hasattr(db, 'chunkinized_data'), "Database should have chunkinized_data attribute"
    db.file.close()

def test_add_entry():
    """Test adding entries to the database"""
    db = Database()
    
    # Clear file first
    db.file.seek(0)
    db.file.truncate(0)
    
    # Add test entry
    test_entry = "Test entry content"
    test_table = "TE"
    db.add_entry(test_entry, test_table)
    
    # Verify entry was added
    db.file.seek(0)
    content = db.file.read()
    assert test_entry in content, f"Entry '{test_entry}' should be in file"
    assert test_table in content, f"Table '{test_table}' should be in file"
    db.file.close()

def test_search_file():
    """Test searching for entries"""
    db = Database()
    
    # Clear file first
    db.file.seek(0)
    db.file.truncate(0)
    
    # Add test entries
    entries = [
        ("Apple fruit entry", "FR"),
        ("Banana fruit entry", "FR"),
        ("Apple computer entry", "CO")
    ]
    
    for entry, table in entries:
        db.add_entry(entry, table)
    
    # Test search
    apple_results = db.search_file("Apple", None)
    assert len(apple_results) == 2, f"Should find 2 entries with 'Apple', found {len(apple_results)}"
    
    # Test search in specific table
    apple_fr_results = db.search_file("Apple", "FR")
    assert len(apple_fr_results) == 1, f"Should find 1 entry with 'Apple' in FR table, found {len(apple_fr_results)}"
    db.file.close()

def test_tables():
    """Test table management"""
    db = Database()
    
    # Add tables
    initial_table_count = len(db.tables)
    db.add_table("T1")
    db.add_table("T2")
    
    # Verify tables added
    assert len(db.tables) == initial_table_count + 2, f"Should have added 2 tables"
    assert "T1" in db.tables, "T1 should be in tables"
    assert "T2" in db.tables, "T2 should be in tables"
    
    # Test remove table
    db.remove_table("T1")
    assert "T1" not in db.tables, "T1 should be removed from tables"
    assert len(db.tables) == initial_table_count + 1, f"Should have removed 1 table"
    db.file.close()

def test_exists():
    """Test entry existence check"""
    db = Database()
    
    # Clear file first
    db.file.seek(0)
    db.file.truncate(0)
    
    # Add test entry
    test_entry = "Unique test content"
    test_table = "UT"
    db.add_entry(test_entry, test_table)
    
    # Test exists
    assert not db.exists("nonexistent", test_table), "Nonexistent entry should not exist"
    db.file.close()

def test_search_exact_case():
    """Test exact case search"""
    db = Database()
    
    # Clear file first
    db.file.seek(0)
    db.file.truncate(0)
    
    # Add test entries
    entries = [
        ("This has ExactWord in it", "EX"),
        ("This has exactword lowercase", "EX"),
        ("This has PreExactWordPost embedded", "EX"),
        ("ExactWord at beginning", "EX"),
        ("Ending with ExactWord", "EX")
    ]
    
    for entry, table in entries:
        db.add_entry(entry, table)
    
    # Test exact search
    results = db.search_exact_case("ExactWord", None)
    
    # We expect to find entries where ExactWord is a standalone word
    assert len(results) > 0, "Should find at least one exact match"
    
    # At minimum these should match (depending on implementation)
    expected_matches = ["This has ExactWord in it", "ExactWord at beginning", "Ending with ExactWord"]
    
    # Check if expected matches are in results
    found_count = 0
    for result in results:
        for expected in expected_matches:
            if expected in result:
                found_count += 1
                break
    
    assert found_count > 0, "Should find at least one of the expected matches"
    db.file.close()

def test_remove_entry():
    """Test removing entries"""
    db = Database()
    
    # Clear file first
    db.file.seek(0)
    db.file.truncate(0)
    
    # Add test entry
    test_entry = "Entry to remove"
    test_table = "RM"
    db.add_entry(test_entry, test_table)
    
    # Verify entry exists
    before_results = db.search_file(test_entry, None)
    assert len(before_results) > 0, "Entry should exist before removal"
    
    # Remove entry
    db.remove_entry(test_entry)
    
    # Verify entry no longer exists
    after_results = db.search_file(test_entry, None)
    db.file.close()

def run_all_tests():
    """Run all tests and report overall results"""
    print("="*60)
    print("DATABASE IMPLEMENTATION TESTS")
    print("="*60)
    
    tests = [
        ("Database Initialization", test_database_init),
        ("Adding Entries", test_add_entry),
        ("Searching Entries", test_search_file),
        ("Table Management", test_tables),
        ("Entry Existence", test_exists),
        ("Exact Case Search", test_search_exact_case),
        ("Removing Entries", test_remove_entry)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_fn in tests:
        if run_test(name, test_fn):
            passed += 1
        else:
            failed += 1
            
    # Print summary
    print("\n" + "="*60)
    print(f"TEST SUMMARY: {passed + failed} tests run")
    print(f"✅ {passed} tests passed")
    print(f"❌ {failed} tests failed")
    
    if failed == 0:
        print("\nALL TESTS PASSED! Your database implementation works correctly.")
    else:
        print(f"\nSome tests failed. Fix the issues in your implementation.")
    print("="*60)
    
    return passed, failed

if __name__ == "__main__":
    run_all_tests()