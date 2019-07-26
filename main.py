# imports
from tenma import Tenma
import numpy as np


def main():
    
    # Connect to TENMA
    TENMA = Tenma()
    
    """
    Testing individual voltages and currents to see if TENMA.get_value
    function gives same value as power source.
    To test current, change key in set_value to 'I'.
    """
    
    TENMA.set_value('V', 10)
    print (TENMA.get_value('V'), TENMA.get_value('I'))
    
    """
    Testing voltages of 1-10V to see if current responds amd current from 0 to
    1A to see if voltage changes.
    """
    
    # IV scan
    for i in range(11) :
        TENMA.set_value('V', i)
        print (TENMA.get_value('V'))
        print (TENMA.get_value('I'))
    
    for i in np.arange(0,1.1,0.1) :
        TENMA.set_value('I', i)
        print (TENMA.get_value('V'), TENMA.get_value('I'))


# main program
if __name__ == '__main__':
    main()
