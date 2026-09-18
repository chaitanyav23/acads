def is_monotone( vals ):
    
    # Use the zipping trick to compare consecutive values in a sequence
    # Is the sequence always increasing?
    is_inc = all( a < b for a, b in zip( vals, vals[ 1: ] ) )
    # Is the sequence always decreasing?
    is_dec = all( a > b for a, b in zip( vals, vals[ 1: ] ) )
    return is_inc or is_dec

def phalana_bodh( x, y ):
    
    step = x[ 1 ] - x[ 0 ]
    
    # All y values appear twice in the trapezoidal sum except the end points
    my_trapezoid_sum = 0.5 * step * ( 2 * sum( y ) - y[ 0 ] - y[ -1 ] )
    
    # Compare to max instead of comparing twice
    my_local_maxima = [ i for i in range( 1, len( y ) - 1 )\
                            if y[ i ] > max( y[i - 1], y[i + 1] ) ]
                            
    # Find all monotone sequences
    monotone_sequences = [ ( start, end )\
                                for start in range( len( y ) )\
                                for end in range( start, len( y ) + 1 )\
                                if end - start > 1 and is_monotone( y[ start : end ] ) ]
    
    # Handy shortcut to find the length of a segment
    len_seg = lambda segment: segment[ 1 ] - segment[ 0 ]
    
    # Empty list is falsy and non empty lists are truthy
    max_monotone = max( map( len_seg, monotone_sequences ) )\
                        if monotone_sequences else 0
    
    my_longest_monotone = sorted( seq for seq in monotone_sequences\
                                    if len_seg( seq ) == max_monotone )
    
    # Some bit of calculus required here
    sum_x = sum( x )
    sum_y = sum( y )
    sum_xx = sum( v * v for v in x )
    sum_xy = sum( u * v for u, v in zip( x, y ) )
    n = len( x )
    
    my_slope = ( n * sum_xy - sum_x * sum_y ) / ( n * sum_xx - sum_x * sum_x )
    my_intercept = ( sum_y - my_slope * sum_x ) / n
    
    my_summary = {
        "trapezoid_sum" : my_trapezoid_sum,
        "local_maxima" : my_local_maxima,
        "longest_monotone" : my_longest_monotone,
        "best_linear_fit" : { "slope": my_slope, "intercept": my_intercept }
    }
    return my_summary