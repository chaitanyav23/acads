from lookup import TABLE, ITERATIONS, DOT_TOL, NOP_INDEX

# Rotate a starting point by a certain angle
# The angle is not given directly, instead cos and sin are given
def rotate( vec, sin_t, cos_t, direction ):
    
    x, y = vec
    # CW rotations effectively use a negative angle
    sin_t *= direction
    return x * cos_t - y * sin_t, x * sin_t + y * cos_t

# Return the dot product of two vectors
# The sticky flag attaches the output to target if close enough
def dot( vec0, vec1, /, target = 1, sticky = False ):
    
    dot = vec0[ 0 ] * vec1[ 0 ] + vec0[ 1 ] * vec1[ 1 ]
    return target if ( dot >= target - DOT_TOL ) and sticky else dot

def my_single_best( heading, start = ( 1, 0 ) ):
    
    # Create a list of angles and alignments keeping in mid tie break order
    directions = [ 1, -1 ]
    steps = []
    
    # A (possibly non-Pythonic) way to (mis)use list comprehension to run a nested loop
    # This will produce a list of None values which will disappear into nothingness
    [ steps.append( ( idx, sin_t, cos_t, direction ) )\
        for idx, ( _, sin_t, cos_t ) in enumerate( TABLE )\
        for direction in directions ]
    
    # Rotate by every possible angle and direction
    alignments = [ ( rotate( start, sin_t, cos_t, direction ), idx, direction )\
                    for idx, sin_t, cos_t, direction in steps ]
    
    # Find argmax using our old trick
    # Using the sticky flag ensures that the largest angle yeilding alignment is chosen
    return max( alignments, key = lambda tup: dot( tup[ 0 ], heading, sticky = True ) )

def my_best( heading, start = ( 1, 0 ) ):
    
    current = start
    idx_list = []
    dir_list = []
        
    for iteration in range( ITERATIONS ):
            
        current, next_idx, next_dir = my_single_best( heading, start = current )
        idx_list.append( next_idx )
        dir_list.append( next_dir )
        
        # If we are already aligned, start filling NOPS and conclude
        if dot( current, heading ) >= 1 - DOT_TOL:
            idx_list.extend( [ NOP_INDEX ] * ( ITERATIONS - len( idx_list ) ) )
            dir_list.extend( [ 1 ] * ( ITERATIONS - len( dir_list ) ) )
            break
    
    return current, idx_list, dir_list

def jodtara( sx, sy ):
    
    _, single_best_angle, single_best_direction = my_single_best( ( sx, sy ) )
    my_final_heading, my_angle_ids, my_directions = my_best( ( sx, sy ) )
    
    my_summary = {
        "single_best": [ single_best_angle, single_best_direction ],
        "angle_ids": my_angle_ids,
        "directions": my_directions,
        "final_heading": list( my_final_heading ),
    }
    return my_summary