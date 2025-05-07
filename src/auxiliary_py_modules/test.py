import os

# Check if __init__.py exists in the directory
init_file = os.path.join("auxiliary_py_modules", "__init__.py")
if os.path.exists(init_file):
    print(f"Found __init__.py at: {init_file}")
else:
    print(f"__init__.py NOT found in auxiliary_py_modules/")
