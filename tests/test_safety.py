"""Tests for safety module."""
from shellex.safety import check_safety, SafetyLevel


def test_safe_commands():
    assert check_safety("ls -la") == SafetyLevel.SAFE
    assert check_safety("find . -name '*.py'") == SafetyLevel.SAFE
    assert check_safety("grep -r 'TODO' src/") == SafetyLevel.SAFE
    assert check_safety("wc -l *.txt") == SafetyLevel.SAFE
    assert check_safety("cat README.md") == SafetyLevel.SAFE


def test_normal_commands():
    assert check_safety("rm temp.txt") == SafetyLevel.NORMAL
    assert check_safety("sudo apt update") == SafetyLevel.NORMAL
    assert check_safety("kill -9 1234") == SafetyLevel.NORMAL


def test_dangerous_rm_variations():
    assert check_safety("rm -rf /home ") == SafetyLevel.DANGEROUS
    assert check_safety("rm -fr /tmp ") == SafetyLevel.DANGEROUS
    assert check_safety("rm -rfi /var ") == SafetyLevel.DANGEROUS
    assert check_safety("rm -Rf /opt ") == SafetyLevel.DANGEROUS
    assert check_safety("rm --recursive --force /") == SafetyLevel.DANGEROUS
    assert check_safety("rm --force --recursive /") == SafetyLevel.DANGEROUS


def test_dangerous_other():
    assert check_safety("dd if=/dev/zero of=/dev/sda") == SafetyLevel.DANGEROUS
    assert check_safety("mkfs.ext4 /dev/sda1") == SafetyLevel.DANGEROUS
    assert check_safety("chmod -R 777 /") == SafetyLevel.DANGEROUS


def test_edge_cases():
    assert check_safety("") == SafetyLevel.SAFE
    assert check_safety("echo hello") == SafetyLevel.SAFE
