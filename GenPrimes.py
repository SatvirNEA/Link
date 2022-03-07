def writefile(primes):
        file = open("Primes.txt" , "a+")        # Creates Primes.txt if not already there, with read and write perms
        file.truncate(0)     # Clears file of any existing data
        for position in range (0, len(primes)):     # For each element in the primes list
            file.write(str(primes[position]))       # Iteratively writes each prime to a new line in the text file
            file.write("\n")
        file.close()

def genprimes (limit):
    primes = [None] * 125      # Generates initial list of primes to be populated
    position = 0        # Start position/counter to be used for appending

    for number in range(2, limit + 1):  # Checks all numbers between 2 and the max number (+ 1 used for inclusivity)  
        prime = True      # Assume number is prime until disproven
        for divisor in range(2, number // 2):     # Creates divisors between 1 and half the number (increases efficiency)
            if number % divisor == 0:       # If the remainder from dividing the two numbers is 0, it has a factor and so is not a prime
                prime = False

        if prime and number != 4:       # If a number is prime, it is entered into the list of primes, also prevents 4 from being prime
            primes[position] = number
            position += 1

    writefile(primes)   # Calls procedure that writes to file