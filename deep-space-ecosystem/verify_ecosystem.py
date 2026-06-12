"""
Ecosystem-Wide Test Runner and Verification Suite.
Sets up the python path internally and runs all unit tests across all 9 repositories.
"""

import os
import sys
import unittest


def main():
    # Get the parent directory of this script (deep-space-ecosystem)
    ecosystem_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(ecosystem_dir)
    
    # Define source directories to add to PYTHONPATH
    src_paths = [
        os.path.join(ecosystem_dir, "deep-space-core", "src"),
        os.path.join(ecosystem_dir, "deep-space-mission-planner"),
        os.path.join(ecosystem_dir, "deep-space-propulsion-simulator"),
        os.path.join(ecosystem_dir, "deep-space-digital-twin"),
        os.path.join(ecosystem_dir, "deep-space-knowledge"),
        os.path.join(ecosystem_dir, "deep-space-knowledge", "mathematics"),
    ]
    
    for path in src_paths:
        if path not in sys.path:
            sys.path.insert(0, path)
            
    print("=" * 70)
    print("Deep Space Ecosystem Verification Test Suite")
    print("=" * 70)
    print(f"Ecosystem directory: {ecosystem_dir}")
    print("Configured Python paths:")
    for p in src_paths:
        print(f"  - {os.path.relpath(p, workspace_dir)}")
    print("-" * 70)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Discovery directories
    test_dirs = [
        ("deep-space-core", os.path.join(ecosystem_dir, "deep-space-core", "tests")),
        ("deep-space-mission-planner", os.path.join(ecosystem_dir, "deep-space-mission-planner", "tests")),
        ("deep-space-propulsion-simulator", os.path.join(ecosystem_dir, "deep-space-propulsion-simulator", "tests")),
        ("deep-space-digital-twin", os.path.join(ecosystem_dir, "deep-space-digital-twin", "tests")),
        ("deep-space-knowledge", os.path.join(ecosystem_dir, "deep-space-knowledge", "mathematics", "tests")),
    ]
    
    for name, test_dir in test_dirs:
        if os.path.exists(test_dir):
            print(f"Discovering tests in {name}...")
            discovered = loader.discover(start_dir=test_dir, pattern="test_*.py", top_level_dir=test_dir)
            suite.addTests(discovered)
        else:
            print(f"Warning: Test directory not found: {os.path.relpath(test_dir, workspace_dir)}")
            
    print("-" * 70)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 70)
    print("Verification Summary:")
    print(f"  Tests Run: {result.testsRun}")
    print(f"  Errors   : {len(result.errors)}")
    print(f"  Failures : {len(result.failures)}")
    print("=" * 70)
    
    if not result.wasSuccessful():
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
