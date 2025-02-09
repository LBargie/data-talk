import importlib

def process_globals():
    # Dynamically import the module that executed the script
    caller_module = importlib.import_module('__main__')
    
    # Access global variables from the calling module dynamically
    if hasattr(caller_module, 'global_var1') and hasattr(caller_module, 'global_var2'):
        print(f"global_var1: {caller_module.global_var1}")
        print(f"global_var2: {caller_module.global_var2}")
    else:
        print("Global variables not found.")
