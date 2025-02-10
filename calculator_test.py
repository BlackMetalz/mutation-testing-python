import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 1) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 2) == 3.0
    assert divide(5, 2) == 2.5
    # This will raise a survivor in mutation testing
    """
    with pytest.raises(ValueError):
        divide(1, 0)
    """
    # This will not raise a survivor in mutation testing
    # Test division by zero error message explicitly
    try:
        divide(1, 0)
        pytest.fail("Expected ValueError")  # Should not reach this line
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"