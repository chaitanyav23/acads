import sys
import statistics

def analyze_temperatures(temp,n):
    
    m = statistics.mean(temp)
    M = statistics.median(temp)
    
    print(f"\nThe Mean of the given temperature(s) is: ", m)
    print(f"\nThe Median of the given temperature(s) is: ", M)
    
    if n == 1:
        print("\nSample variance needs at least two data points to apply Bessel's correction")
        print("\nBeing the square root of variance standard deviation also requires at least two data points")
        print("\nWith the amount of sample data the only analysis of temperatures we can achieve is the one mentioned above")
        return
        
    std = statistics.stdev(temp)
    var = statistics.variance(temp)
    
    print(f"\nThe Sample Variance calculated using the Bessel's formula of the given temperature(s) is: ", var)
    print(f"\nThe Sample Standard Deviation calculated using the sample variance of the given temperature(s) is: ", std)
    print("\n")

    return    

def main():

    n = int(input("\nEnter the size of the array: "))
    if n == 0:
        print("\nStatisticsError: mean/median requires at least one data point and (sample)variance/standard deviation requires at least two data points\n")
        print("The program will now be terminated, please enter a valid value next time\n")
        sys.exit(1)
        
    array = []
    for i in range(n):
        element = int(input(f"\nEnter element at index {i+1}: \n"))
        array.append(element)
        
    analyze_temperatures(array,n)
    
if __name__ == "__main__":
    main()
