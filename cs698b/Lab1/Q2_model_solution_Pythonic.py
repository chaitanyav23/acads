def gen_anagrams( word ):
    
    # Base case for recursion: a single letter word is its own (sole) anagram
    if len( word ) == 1:
        return [ word ]
    
    anagram_list = []
    for idx, char in enumerate( word ):
        # Strings are immutable so create a new string by removing that word
        sub_anagram_list = gen_anagrams( word[ :idx ] + word[ idx + 1: ] )
        anagram_list.extend( [ char + sub_anagram for sub_anagram in sub_anagram_list ] )
        
    return anagram_list

def shabd_kala( word ):
    
    AST = '*'
    DOT = '.'
    n = len( word )
    
    my_framed = [ AST * ( n + 2 ), AST + word + AST, AST * ( n + 2 ) ]
    
    my_diagonal = [ DOT * idx + char + DOT * ( n - idx - 1 )\
                        for idx, char in enumerate( word ) ]
    
    my_pyramidal = [ word[ : idx + 1 ] for idx, char in enumerate( word ) ]
    
    my_anagramal = sorted( gen_anagrams( word ) )

    my_summary = {
        "framed" : my_framed,
        "diagonal" : my_diagonal,
        "pyramidal" : my_pyramidal,
        "anagramal" : my_anagramal,
    }
    return my_summary