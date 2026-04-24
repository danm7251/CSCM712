def invertArray(arr):
    return {key: i for i, key in enumerate(arr)}

def countSort(arr):

    counts = {}

    # Adds 1 to number of occurences, if key doesn't exist yet, get() returns default value 0.
    for item in arr:
        counts[item] = counts.get(item, 0) + 1
    
    # Get keys
    keys = sorted(counts.keys())
    
    # Make new array
    arr.clear()
    for key in keys:
        count = counts[key]
        for _ in range(count):
            arr.append(key)
            
    return arr

if __name__ == "__main__":
    data = [4, 1, 4, 3, 2, 1, 4, 2]
    print(f"Original: {data}")
    countSort(data)
    print(f"Sorted:   {data}")