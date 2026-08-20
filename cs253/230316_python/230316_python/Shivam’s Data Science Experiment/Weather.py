# I have taken X as a unit of Time, precisely Days of the year 
# Next for Y, I have chosen Temperature as deg. C
# Since A,C,E are scale factors they should lie between -20 to +20 
# B,D,F are frequency/shape modifiers so for periodic func. values should be between -0.5 to +0.5, and for non-periodic func. values should be between -5 to +5 

import numpy as np 

import matplotlib.pyplot as plt 
import random
import math

def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)

def generate_dataset(n, x_min, x_max):
    X = np.random.uniform(low = x_min, high = x_max, size = n)
    Y = np.zeros(n)
    h = {1,2,3,4,5,6}
    g = {1,2,3,5,6}

    for i in range(n):
        for j in range(3):
            c = random.uniform(-20,40)
            if X[i] <= 0:
                func = random.choice(list(g))
            else:
                func = random.choice(list(h))
            
            if func == 1 or func == 2 or func == 3:
                d = random.uniform(-0.5,0.5)
            else:
                d = random.uniform(-5,5)

            if func == 1:
                Y[i] += c*math.sin(d*X[i])
            elif func == 2:
                Y[i] += c*math.cos(d*X[i])                
            elif func == 3:
                Y[i] += c*math.tan(d*X[i])
            elif func == 4:
                d = abs(d)
                Y[i] += c*math.log(d*X[i])                
            elif func == 5:
                Y[i] += c*((d*X[i])**2)                               
            elif func == 6:
                Y[i] += c*((d*X[i])**3)

    return X, Y

def plot_scatter(X,Y):
    plt.figure(figsize=(12, 6))  
    plt.scatter(X, Y, s=20, alpha=0.7, label='Global Temperature')

    plt.title('Analyzing trends in climate change using Global Temperature', fontsize=16)

    plt.xlabel('Day of the Year', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)

    plt.legend(fontsize=10)

    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    # plt.style.use('seaborn-v0_8-whitegrid') 

    plt.show()

def plot_histogram(X, Y):
    plt.figure(figsize=(10, 6))
    plt.hist(Y, bins=20, color='skyblue', edgecolor='black', alpha=0.7, label='Temperature Distribution')

    plt.title('Distribution of Global Temperatures', fontsize=16)
    plt.xlabel('Days of the Year', fontsize=12)
    plt.ylabel('Temperature', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    # plt.style.use('seaborn-v0_8-whitegrid')
    plt.show()

def plot_line(X, Y):
    plt.figure(figsize=(12, 6))
    plt.plot(X, Y, marker='o', linestyle='-', color='steelblue', linewidth=1, markersize=4, label='Daily Temperature Trend')

    plt.title('Temperature Trend', fontsize=16)
    plt.xlabel('Day of the Year', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    # plt.style.use('seaborn-v0_8-whitegrid')
    plt.show()

def plot_boxplot(X, Y):
    plt.figure(figsize=(8, 6))
    plt.boxplot(Y, labels=['Global Temperature'], patch_artist=True, boxprops=dict(facecolor='lightcoral', alpha=0.7), medianprops=dict(color='black'))

    plt.title('Statistical Distribution of Global Temperatures', fontsize=16)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    # plt.style.use('seaborn-v0_8-whitegrid')
    plt.show()

def main():
    print("\nThis is a program which Can model how global temperatures (Y) rise over time (X) due to increasing greenhouse gas emissions\n")

    set_random_seed(2025)

    while True:
        x_min = int(input("\nEnter the minimum value of X represents 'Number of Days': "))
        if x_min < 0:
            print("\nPlease enter a positive integer")
            continue
        elif x_min == 365:
            print("\nMinimum value of X cannot be equal to the upper bound")
            continue
        else:
            break
    
    while True:
        x_max = int(input("\nEnter maximum value of X: "))
        if x_min < x_max <= 365:
            break
        else:
            print("\nPlease enter a valid number")

    while True:
        n = int(input("\nEnter the number of data points (N) to generate: "))
        if x_min <= n <= x_max:
            break
        else:
            print("\nEnter a valid value")

    X, Y = generate_dataset(n, x_min, x_max)
    plot_scatter(X,Y)
    plot_histogram(X, Y)
    plot_line(X, Y)
    plot_boxplot(X, Y)


if __name__ == "__main__":
    main()
