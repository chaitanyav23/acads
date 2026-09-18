CONST = "Good Morning FDE1"

def welcome( name_ ):
    '''
    This function will print a polite message indented for the recipient
    The message will be from the dunder variable __name__

    Input
    -----
        name_: the name of the recipient

    Output
    ------
        None
    '''
    print( f"Hello {name_}, my name is {__name__}" )

def main():
    print( "My name is", __name__ )
    print( "My file is", __file__ )

if __name__ == "__main__":
    print( "I can access the constant", CONST )
    main()
