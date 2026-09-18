from lookup import TABLE, ITERATIONS, DEG_TOL, NOP_INDEX

# Rotate a starting point by a certain angle
# The angle is given directly
def rotate( theta, delta, direction ):
    return theta + direction * delta

# Return the absolute angular difference
# The sticky flag attaches theta1 to theta2 if close enough
def diff( theta1, theta2, /, sticky = False ):
    
    diff = abs( theta1 - theta2 )
    return 0 if ( diff <= DEG_TOL ) and sticky else diff

def my_single_best( heading, start = 0 ):
    
    # Create a list of angles and alignments keeping in mid tie break order
    directions = [ 1, -1 ]
    steps = []
    
    for idx, theta in enumerate( TABLE ):
        for direction in directions:
            steps.append( ( idx, theta, direction ) )
    
    # Rotate by every possible angle and direction
    alignments = [ ( rotate( start, theta, direction ), idx, direction )\
                    for idx, theta, direction in steps ]
    
    # Find argmin using our old trick
    # Using the sticky flag ensures that the largest angle yeilding alignment is chosen
    return min( alignments, key = lambda tup: diff( tup[ 0 ], heading, sticky = True ) )

def my_best( heading, start = 0 ):
    
    current = start
    idx_list = []
    dir_list = []
        
    for iteration in range( ITERATIONS ):
            
        current, next_idx, next_dir = my_single_best( heading, start = current )
        idx_list.append( next_idx )
        dir_list.append( next_dir )
        
        # If we are already aligned, start filling NOPS and conclude
        if diff( current, heading ) <= DEG_TOL:
            idx_list.extend( [ NOP_INDEX ] * ( ITERATIONS - len( idx_list ) ) )
            dir_list.extend( [ 1 ] * ( ITERATIONS - len( dir_list ) ) )
            break
    
    return current, idx_list, dir_list

def jodtara_lite( theta ):
    
    _, single_best_angle, single_best_direction = my_single_best( theta )
    my_final_heading, my_angle_ids, my_directions = my_best( theta )
    
    my_summary = {
        "single_best": [ single_best_angle, single_best_direction ],
        "angle_ids": my_angle_ids,
        "directions": my_directions,
        "final_heading": my_final_heading,
    }
    return my_summary