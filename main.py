# imports
from tenma import Tenma


def main():

    # Connect to TENMA
    TENMA = Tenma()

    TENMA.set_value('V', 24)
    TENMA.set_value('I', 10)
    
    TENMA.increment('V', -2)
    TENMA.increment('I', -1.0)

    TENMA.increment('V', -2)
    TENMA.increment('I', -1)

    TENMA.increment('V', -2)
    TENMA.increment('I', -1)

    TENMA.increment('V', -2)
    TENMA.increment('I', -1)

    
    print('Voltage record (time, value) : \n', TENMA.get_record('V'))
    print('Current record (time, value) : \n', TENMA.get_record('I'))

    
    
# main program
if __name__ == '__main__':
    main()
