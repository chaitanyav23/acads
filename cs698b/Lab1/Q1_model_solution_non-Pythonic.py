def megha_summary( rainfall_list ):
    
    my_total = 0
    my_rainy_days = 0
    
    # Set initial value carefully so that in the edge case of
    # empty list, the initial value itself is correct answer
    # since the loop will not execute at all in that case
    max_rain = -1
    my_rainiest_day = None
    
    my_longest_drought = 0
    current_drought_length = 0
    
    for idx, rain in enumerate( rainfall_list, start = 1 ):
        my_total += rain
        if rain > 0:
            my_rainy_days += 1
            current_drought_length = 0
        else:
            current_drought_length += 1
            if current_drought_length > my_longest_drought:
                my_longest_drought = current_drought_length

        if rain > max_rain:
            max_rain = rain
            my_rainiest_day = idx
    
    my_summary = {
        "total" : my_total,
        "average" : my_total / max( len( rainfall_list ), 1 ),
        "rainy_days" : my_rainy_days,
        "rainiest_day" : my_rainiest_day,
        "longest_drought" : my_longest_drought,
    }
    return my_summary