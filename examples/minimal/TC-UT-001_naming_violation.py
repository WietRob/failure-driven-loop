import subprocess


def test_naming_violation_detected():
    test_file = "/tmp/failure-driven-loop/examples/minimal/tests/unit/test_auth.py"

    result = subprocess.run(
        ["fdl-validate-naming", "--file", test_file],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0, "Should fail with naming violation"
    assert "Invalid naming format" in result.stdout, "Should show naming error"
    assert "TC-{LEVEL}-{ID}_{component}.py" in result.stdout, "Should show expected format"
    print("✅ Naming violation detected correctly")
