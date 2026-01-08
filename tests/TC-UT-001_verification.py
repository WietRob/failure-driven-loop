"""
TC-UT-001: Failure-Driven Loop Installation Verification

Validates: Package installation and CLI commands work correctly

Tests:
1. Package imports successfully
2. All CLI commands are available
3. Loop executes end-to-end
"""

import subprocess
import sys
from pathlib import Path


def test_package_import():
    """Test that package imports successfully."""
    try:
        import failure_loop

        assert failure_loop.__version__ == "1.0.0"
        print("✅ Package imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False


def test_cli_commands():
    """Test that all CLI commands are available."""
    commands = [
        "fdl-validate-naming",
        "fdl-validate-links",
        "fdl-log-feedback",
        "fdl-analyze-patterns",
        "fdl-tree-analyzer",
    ]

    all_available = True
    for cmd in commands:
        result = subprocess.run(
            ["which", cmd],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ {cmd} available")
        else:
            print(f"❌ {cmd} not found in PATH")
            all_available = False

    return all_available


def test_validate_naming():
    """Test naming validation command."""
    # Create test file with naming violation
    test_file = Path("/tmp/test_naming.py")
    test_file.write_text("def test_auth():\n    assert True\n")

    # Run validation
    result = subprocess.run(
        ["fdl-validate-naming", "--file", str(test_file)],
        capture_output=True,
        text=True,
    )

    # Should fail with naming violation
    if result.returncode != 0 and "Invalid naming format" in result.stdout:
        print("✅ Naming validation detects violations")
        test_file.unlink()
        return True
    else:
        print(f"❌ Naming validation failed: {result.stdout}")
        test_file.unlink()
        return False


def test_log_feedback():
    """Test feedback logging command."""
    result = subprocess.run(
        [
            "fdl-log-feedback",
            "--type",
            "mistake",
            "--context",
            "Test context",
            "--feedback",
            "Test feedback",
            "--category",
            "Testing",
            "--severity",
            "low",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and "Feedback logged" in result.stdout:
        print("✅ Feedback logging works")
        return True
    else:
        print(f"❌ Feedback logging failed: {result.stdout}")
        return False


def test_tree_analyzer():
    """Test tree analyzer command."""
    # Create minimal requirement
    req_dir = Path("/tmp/test_requirements")
    req_dir.mkdir(exist_ok=True)
    req_file = req_dir / "SW-REQ-TEST.md"
    req_file.write_text("---\nid: SW-REQ-TEST\ntitle: Test Requirement\ntested_by: []\n---\n")

    result = subprocess.run(
        [
            "fdl-tree-analyzer",
            "--sw",
            "SW-REQ-TEST",
            "--requirements-dir",
            str(req_dir),
            "--tests-dir",
            "/tmp",
            "--code-dir",
            "/tmp",
        ],
        capture_output=True,
        text=True,
    )

    # Should show gap
    if result.returncode == 0 and "GAP" in result.stdout:
        print("✅ Tree analyzer shows gaps")
        req_file.unlink()
        req_dir.rmdir()
        return True
    else:
        print(f"❌ Tree analyzer failed: {result.stdout}")
        req_file.unlink()
        req_dir.rmdir()
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("FAILURE-DRIVEN LOOP VERIFICATION")
    print("=" * 60)
    print()

    results = []

    # Test 1: Package import
    print("1. Testing package import...")
    results.append(test_package_import())
    print()

    # Test 2: CLI commands
    print("2. Testing CLI commands...")
    results.append(test_cli_commands())
    print()

    # Test 3: Naming validation
    print("3. Testing naming validation...")
    results.append(test_validate_naming())
    print()

    # Test 4: Feedback logging
    print("4. Testing feedback logging...")
    results.append(test_log_feedback())
    print()

    # Test 5: Tree analyzer
    print("5. Testing tree analyzer...")
    results.append(test_tree_analyzer())
    print()

    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if all(results):
        print()
        print("✅ All verification tests passed!")
        print("   Package is ready for use.")
        return 0
    else:
        print()
        print("❌ Some tests failed.")
        print("   Check output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
