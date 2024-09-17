from math import sqrt

def is_prime(num):
    if num == 2:
        return True

    if num == 1:
        return False

    print(sqrt(num))
    for i in range(2, int(sqrt(num))+1):
        print(i)
        if num % i == 0:
            return False

    return True


num = 4
print(f"Is {num} prime: {is_prime(num)}")


str1 = "Hello"
str2 = 'there'
bob = str1 + str2
print(bob)