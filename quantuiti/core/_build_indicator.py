import importlib
import inspect
def build_indicator(self, function):
    
    func_name = function.__name__
    args = inspect.getargspec(function)
    try:
        method = importlib.import_module(f'quantuiti.indicators.{func_name}', f'{func_name}')
        method = getattr(method, func_name)

        setattr(self, func_name, method)
    except ModuleNotFoundError:
        print("indicator does not exit, building...")
        to_write = list(inspect.getsourcelines(function))[0]
        to_write = [ to_write for to_write in to_write if "@Engine" not in to_write ]
        
        with open(f'quantuiti/indicators/{func_name}.py', 'w+') as file:
            file.writelines(to_write)
        
        setattr(self, func_name, function)
    print(getattr(self, 'cci'))
