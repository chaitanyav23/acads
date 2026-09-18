def varnamala( string ):
    
    alphabet = list( map( chr, range( ord( 'a' ), ord( 'z' ) + 1 ) ) )
    
    # Find how frequently does each character appear in the string
    my_frequencies = { char : string.count( char ) for char in alphabet }
    
    # Find non-space neighbors
    my_neighbor_map = { c : { n for n in alphabet if c + n in string } for c in alphabet }
    update_map = { c : { None } for c in alphabet\
                    if my_frequencies[ c ] > 0 and my_neighbor_map[ c ] == set() }
    my_neighbor_map.update( update_map )
    
    # Find list of echoing substrings
    # Note that this is a set to take care of cases where a string echoes more than twice
    echo_list = set( string[ i : j ]\
                    for i in range( len( string ) )\
                    for j in range( len( string ) )\
                    if j > i and string[ i : j ] in string[ i + 1: ] )
    
    # Empty list is falsy and non empty lists are truthy
    max_echo = max( map( len, echo_list ) ) if echo_list else 0
    my_longest_echo = sorted( [ echo for echo in echo_list if len( echo ) == max_echo ] )
    
    first_occurence = { c : string.index( c ) for c in alphabet if c in string }

    # If the key argument in sorted is a tuple, then sorted will sort by first element
    # of the tuple, then break ties according to the second element, and so on
    # Python uses stable sorting which ensures that any ties that remain unbroken
    # are broken using the location of the element in original sequence
    # Notice that the first key is negative frequency since we want descending frequencies
    my_signature = ''.join( sorted( first_occurence,\
                    key = lambda c: ( -my_frequencies[ c ], first_occurence[ c ] ) ) )
    
    my_summary = {
        "frequencies" : my_frequencies,
        "neighbor_map" : my_neighbor_map,
        "longest_echo" : my_longest_echo,
        "signature" : my_signature,
    }
    return my_summary