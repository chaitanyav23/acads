import math

def find_all_primes_up_to(limit):
    prime = [1] * (limit + 1)
    prime[0] = prime[1] = 0

    for i in range(2, int(math.sqrt(limit)) + 1):
        if prime[i] == 1:
            for j in range(i * i, limit + 1, i):
                prime[j] = 0

    primes = [i for i in range(2, limit + 1) if prime[i]]
    return primes

def sum_of_primes(n):
    if n < 1:
        return 0
    if n == 1:
        return 2

    if n < 6:
        upper = 15
    else:
        upper = int(n * (math.log(n) + math.log(math.log(n)))) + 10

    primes = find_all_primes_up_to(upper)

    return sum(primes[:n])

def main():
    n = int(input("Enter a positive integer to calulate the sum of prime upto that number: "))
    
    print("The sum of the first n prime numbers: ", sum_of_primes(n))
    
if __name__ == "__main__":
    main()
