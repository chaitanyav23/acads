import random

def get_random_string(outcomes):
    if not outcomes:
        return None
    return random.choice(list(outcomes))

def play(n, rand, score):
    ans = 0
    if n == rand:
        print("\nShmucks, it's a tie! You get to play again.")
        score[0] = score[0] + 1
        ans = 0
    elif (n == 1 and rand == 3) or (n == 2 and rand == 1) or (n == 3 and rand == 2):
        print("\nCongratulations, you win!!")
        score[1] = score[1] + 1
        ans = 1
    else:
        print("\nYou lose... better luck next time!")
        score[2] = score[2] + 1
        ans = 2
    print("\nTotal Score:\n")
    print("Ties = ", score[0])
    print("Wins = ", score[1])
    print("Losses = ", score[2])
    
    return ans
    


def solve(n, score):
    outcomes = {1, 2, 3}
    mapping = {1 :"rock", 2 : "paper", 3 : "scissors"}
    rand = get_random_string(outcomes)
    computer = mapping[rand]
    print(f"\nRandom outcome from set: {computer}")
    flag = play(n, rand, score)

    if flag != 0:
        x = input("\nDo you want to go another Round? (Enter Quit): ").lower()
        if x.strip() == "quit":
            return 1
        else:
            return 0
    return 0

def main():
    mapping = {"rock": 1, "paper": 2, "scissors": 3}
    result = 0
    score = [0,0,0]

    while True:
        s = input("\nEnter 'rock', 'paper', or 'scissors': ").lower().strip()

        if s in mapping:
            if not s.isalpha():
                print("\nError: String must be non-empty and contain only letters")
                continue

            n = mapping[s]
            result = solve(n, score)
        else:
            print("\nInvalid input. Please enter 'rock', 'paper', or 'scissors'.")
            continue

        if result == 0:
            print("\nHere we go again!")
        else:
            print("\nThank you for playing! Hope you come back soon.")
            break

if __name__ == "__main__":
    main()
