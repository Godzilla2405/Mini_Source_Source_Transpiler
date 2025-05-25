def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

def main():
    n = 5
    print(f"Factorial of {n} is {factorial(n)}")

if __name__ == "__main__":
    main() 