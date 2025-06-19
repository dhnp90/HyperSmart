import os

def resolve_path(relative_path):
    """
    Resolves a relative path to an absolute path based on the location of the root directory of the project.

    :param relative_path: Path relative to the project's root directory.
    :return: Absolute path.
    """
    # Get the absolute path of the project's root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This will go up one level to src
    
    # Join the root directory with the relative path to form the full absolute path
    full_path = os.path.join(project_root, relative_path)
    
    # Return the absolute path
    return full_path
