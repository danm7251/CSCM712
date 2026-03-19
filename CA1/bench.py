from timeit import Timer
import csv

def function_A(n): 
    total = 0 

    for i in range(n): 
        total = total + i

    return total

# I would estimate T(n) = n + 1


def function_B(n): 
    count = 0 

    for i in range(n): 
        for j in range(n): 
            for k in range(n): 
                count = count + 1 

    return count 

# I would estimate T(n) = n^3 + 1

word_list = ["algorithm", "data", "structure", "performance", "concatenation"] * 1500 

def concat_plus(word_list): 
    result = "" 
    for word in word_list: 
        result += word   
    return result 

def concat_join(words): 
    return "".join(words) 

if __name__ == "__main__":
    ns = [10, 100, 500, 750, 1000, 1750, 2500, 3750, 5000, 6250, 7500, 8750, 10000, 12500, 15000, 30000, 60000, 120000]
    results = []

    for n in ns:
        word_list = ["algorithm", "data", "structure", "performance", "concatenation"] * n
        #plus_timer = Timer(f"concat_plus({word_list})", "from __main__ import concat_plus")
        join_timer = Timer(f"concat_join({word_list})", "from __main__ import concat_join")

        #plus_time = plus_timer.timeit(number=1000)
        join_time = join_timer.timeit(number=1000)

        #print(f"Plus time for list of size {n}: {plus_time}")
        print(f"Join time for list of size {n}: {join_time}")
        results.append([n, join_time])

    with open("times.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "join_time"])
        writer.writerows(results)