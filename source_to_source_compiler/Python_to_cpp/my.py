def partition(arr, low, high):
    pivot = arr[high]  # Choosing the last element as the pivot
    i = low - 1  # Pointer for the smaller element

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap elements

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Place pivot in correct position
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)  # Get pivot index
        quick_sort(arr, low, pi - 1)  # Sort left sub-array
        quick_sort(arr, pi + 1, high)  # Sort right sub-array

def main():
    arr = [10, 7, 8, 9, 1, 5]
    print("Unsorted array:", arr)
    quick_sort(arr, 0, len(arr) - 1)
    print("Sorted array:", arr)

if __name__ == "__main__":
    main()