def validate_input(n, s):

    if not isinstance(n, int) or n <= 0:
        print("Error: Number must be a positive integer")
        return False
    
    if not isinstance(s, str) or not s.isalpha():
        print("Error: String must be non-empty and contain only letters")
        return False
    
    return True

def process_string(n, s):
    
    if n % 2 == 0 :
        ans = s[::-1]
    else:
        vowels = {'a','e','i','o','u'}
        new = (
            c.upper() if c in vowels else c.lower()
            for c in s
        )
        ans = "".join(new)
        # print(ans)
    
    return ans

def count_set_bits(n) :
    bin_n = format(n, 'b')
    return bin_n.count('1')

def extract_substrings(s, k):
    ans = []
    n = len(s)
    if k > n :
        return ans
    
    for i in range(n - k + 1):
        x = s[i : i + k]
        ans.append(x)
        
    return ans

def sort_or_reverse(n, s, substrings):
    
    if n & len(s) == 0 :
        return sorted(substrings)
    else :
        return(substrings[::-1])

def main():

    while True:
        try:
            n = int(input("Enter a positive integer: "))
        except ValueError:
            print("Please enter a valid integer")
            continue
        
        s = input("Enter a non-empty string with only letters: ")
        
        if validate_input(n, s):
            s = process_string(n, s)
            # print(s)
            break
        else:
            print("\nPlease try again.\n")
            
    # print(s)
    
    k = count_set_bits(n)
    # print(k)
    
    substrings = extract_substrings(s, k)
    # print(substrings)
    
    ans = sort_or_reverse(n, s, substrings)
    print(ans)
            

if __name__ == "__main__":
    main()