def megha_summary( rainfall_list ):
    
    my_total = sum( rainfall_list )
    
    # Avoid divide by zero error
    my_average = my_total / max( len( rainfall_list ), 1 )
    
    # Python treats True as unity for arithmetic
    my_rainy_days = sum( [ rain > 0 for rain in rainfall_list ] )
    
    # Creating a custom argmax function by hacking the key argument alongwith enumeration
    # Note the use of conditional expression to take care of edge case
    my_rainiest_day = 1 + max( enumerate( rainfall_list ), key = lambda tp: tp[ 1 ] )[ 0 ]\
                        if len( rainfall_list ) > 0\
                        else None
    
    # Find longest drought using a cute trick using a modified cumulative sum
    
    # First, find out days on which it did not rain
    drought_or_not = [ 0 if rain > 0 else 1 for rain in rainfall_list ]   
    
    # Standard cumulative sum simply adds the current element to a running total
    # In the modified version, multiply the current element to the total before adding
    # This will make every zero in the list reset the running total to zero
    # Since our drought_or_not list is binary, this will give the longest "run" :D
    total = 0
    
    # The walrus operator in Python is an example of syntactic sugar
    # It allows simultaneous assignment and usage in an expression
    mod_cum_sum = [ total := ( total + 1 ) * drought for drought in drought_or_not ]
    # Note the use of conditional expression to take care of edge case
    my_longest_drought = max( mod_cum_sum ) if len( drought_or_not ) > 0 else 0
    
    my_summary = {
        "total" : my_total,
        "average" : my_average,
        "rainy_days" : my_rainy_days,
        "rainiest_day" : my_rainiest_day,
        "longest_drought" : my_longest_drought,
    }
    return my_summary