from synonyms import SYNONYM_GROUPS as sg

# Using conditional expressions makes life simpler
# If the last character of the token is alphabetical, it is non-puncutated
def depunctuate( p_token ):
    return ( p_token, '' ) if p_token[ -1 ].isalpha() else ( p_token[ :-1 ], p_token[ -1 ] )

def jala_chinhit( string ):
    
    # Create inverted index to ease lookup later
    inv_idx = {}
    for i, pair in enumerate( sg ):
        for j, word in enumerate( pair ):
            inv_idx[ word ] = i, j
    
    # Create "punctuated" tokens i.e. tokens with possible punctuation marks after them
    punc_tokens = string.split()
    # De-puncutate the tokens but preserve the punctuation marks
    tokens = [ depunctuate( p_token ) for p_token in punc_tokens ]
    
    my_swappable_count = sum( [ 1 for t in tokens if t[ 0 ] in inv_idx ] )
    
    # inv_idx[ t[ 0 ] ] gives me the ( i, j )-tuple that gives index of the swappable pair
    # as well as the index of the token within that pair
    my_naive_signature = ''.join( [ str( inv_idx[ t[ 0 ] ][ 1 ] ) if t[ 0 ] in inv_idx else '-' for t in tokens ] )
    
    my_naive_watermark = int( my_naive_signature.replace( '-', '' ), base = 2 )
    
    # Deebo's signature depends on the length of the string
    str_len = len( tokens )
    deebo_sig = bin( str_len )[ 2: ].rjust( my_swappable_count, '0' )

    # Find new tokens to embed Deebo's watermark
    deebo_tokens = []
    # Since the message contains swappable and non-swappable tokens
    # This helps me keep track of which all swappable tokens have been handled
    swap_idx = 0
    
    for t in tokens:
        
        # Non-swappable token -- copy-paste as it is
        if t[ 0 ] not in inv_idx:
            deebo_tokens.append( t[ 0 ] + t[ 1 ] )
        # Swappable token -- may need to swap
        else:
            # At which index in the table will I find the pair containing this token
            idx_in_table = inv_idx[ t[ 0 ] ][ 0 ]
            # Which index in the pair should go in order to embed Deebo's watermark
            idx_in_pair = int( deebo_sig[ swap_idx ] )
            # Remember to add back any punctuation mark stored in t[ 1 ]
            deebo_tokens.append( sg[ idx_in_table ][ idx_in_pair ] + t[ 1 ] )
            swap_idx += 1
        my_embed_Deebo_watermark = ' '.join( deebo_tokens )
    
    my_summary = {
        "swappable_count" : my_swappable_count,
        "naive_signature" : my_naive_signature,
        "naive_watermark" : my_naive_watermark,
        "embed_Deebo_watermark" : my_embed_Deebo_watermark,
    }
    return my_summary