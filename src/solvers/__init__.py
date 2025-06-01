# Needed to register the solvers correctly
# As Python imports modules in the order they are defined, 
# we need to ensure that the registry is populated before any solvers are imported.

# First, make sure the registry is imported
__all__ = ['Solver', 'SolverRegistry']

# Then dynamically import all modules in this package
import pkgutil
import importlib

# Skip these modules when importing
SKIP_MODULES = {'__init__', 'registry', 'solver'}

# This auto-discovers and imports all modules in the current package
for _, module_name, _ in pkgutil.iter_modules(__path__):
    if module_name not in SKIP_MODULES:
        # Import the module which will trigger the registration
        importlib.import_module(f"{__name__}.{module_name}")
        
# For debugging: show what solvers were registered
# print(f"Registered solvers: {SolverRegistry.list_solvers()}")