import inspect
import types

def algorithm(self, supp_function):
    """
    pulls the function outside of algorithm file and converts it into a method defined within the Engine
        supp_function: supplied function
    """

    # algorithm supplied to decorator must be a function
    if type(supp_function) is not types.FunctionType:
        error = Exception('[*] Algorithm supplied is not of type', function)
        raise error
        exit()
    if self._algorithm is not None:
        error = Exception('[*] Algorithm already supplied -- SKIPPING...')
        raise error 
        return

    func_params =  inspect.signature(supp_function).parameters
    if len(func_params) > 0:
        print(f'[*] function parameters {func_params} will be ignored')
    
    lines = inspect.getsource(supp_function).split('\n')
    index = 0
    temp = []
    for line in lines:
        if '@' in line and 'algorithm' in line:
            pass
        elif 'def' in line:
            pass
        else:
            temp.append(line + '\n')
        index+=1

    temp = 'async def function(self=self): \n' + ''.join(temp)
    exec(temp)
    loc = locals()['function']
    self._algorithm = loc 
    
    if self.backtest:
        self.backtest_algorithm()
    else:
        self.livetest_algorithm()
    if self.build:
        self.BuildPythonFile()