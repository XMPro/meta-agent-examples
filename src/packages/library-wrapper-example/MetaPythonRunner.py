from contextlib import contextmanager
import importlib.util
import os
import threading

class DataProcessor:
    def __init__(self, filename, timeout):
        self.filename = filename
        self.module = None
        self.timeout = timeout

    def _import_module(self, file_path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            raise ImportError(f"Cannot import module from {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _load_module(self):
        """Load the module from the given filename."""
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"File {self.filename} does not exist")
        
        spec = importlib.util.spec_from_file_location("module.name", self.filename)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def execute_on_create(self, data):
        """Execute the on_create function from the dynamically loaded module."""
        if self.module is None:
            self._load_module()
        
        if hasattr(self.module, 'on_create'):
            return self.module.on_create(data)
        else:
            raise AttributeError("The module does not have an 'on_create' function.")
    
    def execute_on_receive(self, data):
        """Execute the on_receive function from the dynamically loaded module."""
        if self.module is None:
            self._load_module()
        
        if hasattr(self.module, 'on_receive'):
            return self.module.on_receive(data)
        else:
            raise AttributeError("The module does not have an 'on_receive' function.")
        
    def execute_on_destroy(self):
        """Execute the on_destroy function from the dynamically loaded module."""
        if self.module is None:
            self._load_module()
        
        if hasattr(self.module, 'on_destroy'):
            return self.module.on_destroy()
        else:
            raise AttributeError("The module does not have an 'on_destroy' function.")
    
    def execute_with_timeout(self, func, *args):
        """Run a function with a timeout."""
        result = None
        exception = None
        def target():
            nonlocal result, exception
            try:
                result = func(*args)
            except Exception as e:
                exception = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(self.timeout)

        if thread.is_alive():
            raise TimeoutError(f"Execution timed out after {self.timeout} seconds")
        if exception:
            raise exception

        return result