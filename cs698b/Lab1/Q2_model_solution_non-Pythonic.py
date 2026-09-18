def gen_anagrams_non_recursive( word ):
    
    anagram_list = []
    
    for idx, char in enumerate( word ):
        
        sub_word = word[ :idx ] + word[ idx + 1: ]
        
        for sub_idx, sub_char in enumerate( sub_word ):
            
            # We are assured that a sub_sub_word will always be a single character
            # This is because all strings are assured to be of length 3
            # This technique will require as many levels of nesting as characters
            sub_sub_word = sub_word[ :sub_idx ] + sub_word[ sub_idx + 1: ]
            
            anagram = char + sub_char + sub_sub_word
            anagram_list.append( anagram )
        
    return anagram_list

def shabd_kala( word ):
    
    AST = '*'
    DOT = '.'
    n = len( word )
    
    border = ""
    for i in range( n + 2 ):
        border = border + AST
    
    my_framed = [ border, AST + word + AST, border ]
    
    my_diagonal = []
    for i in range( n ):
        row = []
        
        for j in range( n ):
            if i == j:
                row.append( word[ i ] )
            else:
                row.append( "." )
        row_str = ""
        
        for k in range( len( row ) ):
            row_str = row_str + row[ k ]
        
        my_diagonal.append( row_str )
    
    my_pyramidal = []
    for i in range( 1, n + 1 ):
        my_pyramidal.append( word[ :i ] )
    
    my_anagramal = sorted( gen_anagrams_non_recursive( word ) )

    my_summary = {
        "framed" : my_framed,
        "diagonal" : my_diagonal,
        "pyramidal" : my_pyramidal,
        "anagramal" : my_anagramal,
    }
    return my_summary