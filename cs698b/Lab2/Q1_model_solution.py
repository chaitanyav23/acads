def monotone( seq, rev = False ):
    
    # To check for monotonically decreasing, simply reverse the sequence
    if rev:
        seq = seq[ ::-1 ]
    # The all builtin checks if every value in a sequence is truthy
    # It returns True by default if the sequence is empty
    return all( prv < nxt for prv, nxt in zip( seq, seq[ 1: ] ) )

def gen_collatz( n ):
    
    # Initialize the sequence so that for small n edge cases, it gives correct value
    n, size, peak = ( n, 1, n )
    while n > 1:
        # We use the Walrus operator to trick Python into doing our bidding
        # Usually Python does not update values inside a multi-assignment or unpacking step
        # For example, a, b = b, a will happily swap the values
        # However, the use of the Walrus operator changes this default behavior
        n, size, peak = ( n := 3 * n + 1 if n & 1 else n // 2 ), size + 1, max( peak, n )
    return size, peak

def ganitagya( n ):
    
    # map( int, str( n ) ) will map an integer to a list of its digits
    digits = list( map( int, str( n ) ) )
    # use of bitwise operators to find parity / evenness
    even_digits = [ d for d in digits if not d & 1 ]
    odd_digits = [ d for d in digits if d & 1 ]
    
    my_is_parity_ordered = monotone( even_digits ) and monotone( odd_digits, rev = True )
    
    # Find subset digits using masks
    num_digits = len( digits )
    subset_numbers = []
    
    # The numbers 1, 2, 3, ..., 2 ** num_digits - 1 become bitstring masks
    # when interpreted in binary representation
    for i in range( 1, 2 ** num_digits ):
        mask = str( bin( i ) )[ 2: ].rjust( num_digits, '0' )
        subset_numbers.append( int( ''.join( [ digit for ( digit, mask_digit ) in zip( str( n ), mask ) if mask_digit == '1' ] ) ) )
    
    my_subset_numbers = sorted( set( subset_numbers ) )
    
    my_collatz_length, my_collatz_peak = gen_collatz( n )
    
    my_summary = {
        "even_digits": even_digits,
        "is_parity_ordered": my_is_parity_ordered,
        "subset_numbers": my_subset_numbers,
        "collatz_report": { "length": my_collatz_length, "peak": my_collatz_peak },
    }
    return my_summary