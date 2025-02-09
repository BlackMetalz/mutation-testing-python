# Sample for init env in projects

```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

# gitignore
The **/ pattern means "this pattern will be matched in the current directory and any subdirectory", so it will work for all nested Python projects.
For example, this will ignore:

```
python/project1/env/
python/project1/subproject/env/
python/project2/env/
python/deep/nested/project/env/
```

# Output example.
- Make sure pytest is able to run: `pytest test_calculator.py -v`
```

=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.5.0 -- /data/github/kienlt-cicd/mutation-testing-python/env/bin/python3
cachedir: .pytest_cache
rootdir: /data/github/kienlt-cicd/mutation-testing-python
configfile: pyproject.toml
collected 4 items                                                                                                                                                                                                 

test_calculator.py::test_add PASSED                                                                                                                                                                         [ 25%]
test_calculator.py::test_subtract PASSED                                                                                                                                                                    [ 50%]
test_calculator.py::test_multiply PASSED                                                                                                                                                                    [ 75%]
test_calculator.py::test_divide PASSED                                          
```

- Mutation testing: `mutmut run` (without `pyproject.toml` we have to run: `mutmut run --paths-to-mutate calculator.py`)
```
- Mutation testing starting -

These are the steps:
1. A full test suite run will be made to make sure we
   can run the tests successfully and we know how long
   it takes (to detect infinite loops for example)
2. Mutants will be generated and checked

Results are stored in .mutmut-cache.
Print found mutants with `mutmut results`.

Legend for output:
🎉 Killed mutants.   The goal is for everything to end up in this bucket.
⏰ Timeout.          Test suite took 10 times as long as the baseline so were killed.
🤔 Suspicious.       Tests took a long time, but not long enough to be fatal.
🙁 Survived.         This means your tests need to be expanded.
🔇 Skipped.          Skipped.

1. Running tests without mutations
⠴ Running...Done

2. Checking mutants
⠋ 7/7  🎉 6  ⏰ 0  🤔 0  🙁 1  🔇 0
```

# Work on mutation testing:
- As you can see there is 1 survived. Lets dive deep into it: `mutmut results`
```
To apply a mutant on disk:
    mutmut apply <id>

To show a mutant:
    mutmut show <id>


Survived 🙁 (1)

---- calculator.py (1) ----

6
```

- Let's see what is it: `mutmut show 6`
```
--- calculator.py
+++ calculator.py
@@ -9,7 +9,7 @@
 
 def divide(a: int, b: int) -> float:
     if b == 0:
-        raise ValueError("Cannot divide by zero")
+        raise ValueError("XXCannot divide by zeroXX")
     return a / b
```

# Explain on mutation fix xD
how the `test_divide` function tests the `divide` function, focusing on each test case:

```python
def test_divide():
    # Test case 1: Normal division
    assert divide(6, 2) == 3.0  # Tests if 6/2 gives exactly 3.0
    assert divide(5, 2) == 2.5  # Tests if 5/2 gives exactly 2.5
    
    # Test case 2: Division by zero error
    try:
        divide(1, 0)           # Try to divide 1 by 0
        pytest.fail("Expected ValueError")  # If we reach here, test should fail
    except ValueError as e:    # Catch the specific ValueError
        assert str(e) == "Cannot divide by zero"  # Verify exact error message
```

Let's break down what happens in each case:

1. **Normal Division Cases**:
   - `divide(6, 2) == 3.0`: Tests whether 6÷2 equals 3.0
   - `divide(5, 2) == 2.5`: Tests whether 5÷2 equals 2.5
   - These verify that regular division works correctly

2. **Division by Zero Case**:
   ```python
   try:
       divide(1, 0)  # This line triggers the ValueError in divide()
   ```
   When `b = 0`, the divide function hits this code:
   ```python
   if b == 0:
       raise ValueError("Cannot divide by zero")
   ```

   The test then:
   ```python
   except ValueError as e:
       assert str(e) == "Cannot divide by zero"
   ```
   - Catches the ValueError
   - Checks if the error message exactly matches "Cannot divide by zero"
   - If the message is different (like "XXCannot divide by zeroXX" in the mutation), the test fails

This test is now comprehensive because it verifies:
1. Correct results for valid divisions
2. That division by zero raises an error
3. The exact error message content

The mutation test previously survived because we weren't checking the error message content. Now we are, so any change to the message will cause the test to fail.

# Is __init__.py required
In modern Python projects, `__init__.py` files are not always required, but they serve several important purposes:

1. **Package Marking**: 
   - Prior to Python 3.3, `__init__.py` was required to mark a directory as a Python package
   - With Python 3.3+, the concept of "namespace packages" allows packages without `__init__.py`

2. **Common Use Cases**:
   - Initialize package-level variables
   - Import key classes/functions to make them available at package level
   - Define package-level documentation
   - Perform package initialization when imported

Here's a typical example of an `__init__.py`:

```python
"""
Calculator package for mutation testing example.
"""

from .calculator import Calculator

__version__ = '0.1.0'
__all__ = ['Calculator']
```

**Recommendations**:
- Include `__init__.py` if you want to:
  - Make imports cleaner
  - Share common package-level attributes
  - Support older Python versions
  - Follow traditional Python packaging practices
- Skip `__init__.py` if you:
  - Use simple scripts
  - Don't need package functionality
  - Only use Python 3.3+
  - Use namespace packages

For your mutation testing project, I recommend including an `__init__.py` file for better organization and compatibility.