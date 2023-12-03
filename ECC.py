import random
from sympy import randprime
def modinv(k, p):
    return pow(k, -1, p)

def doubling(x1, y1, p, a):
    c = modinv(2 * y1, p)
    s = (3 * x1 ** 2 + a) % p
    s = (s * c) % p
    x3 = (s ** 2 - 2 * x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3

def addition(x1, y1, x2, y2, p):
    c = modinv(x2 - x1, p)
    s = (y2 - y1) % p
    s = (s * c) % p
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3

def calculate_public_key(x1, y1, p, a, mul):
    binary_representation = bin(mul)[2:]
    x3 = x1
    y3 = y1

    for i in range(1, len(binary_representation)):
        x3, y3 = doubling(x3, y3, p, a)
        if binary_representation[i] == '1':
            x3, y3 = addition(x3, y3, x1, y1, p)

    return x3, y3


def is_quadratic_residue(y_square, p):
    # Check if y_square is a quadratic residue modulo p
    return pow(y_square, (p - 1) // 2, p) == 1

def generate_random_point(a, b, p):
    while True:
        x = random.randint(1, p - 1)
        y_square = (x**3 + a*x + b) % p

        if is_quadratic_residue(y_square, p):
            y = pow(y_square, (p + 1) // 4, p)  # Calculate the square root modulo p
            return x, y


def generate_g_a_b_p():
    p = 17
    a = 2
    b = 2
    x1 = 5
    y1 = 1
    return p, a, b, x1, y1


def generate_alice_key(p):
    a1 = random.randrange(2, p)
    return a1

def generate_bob_key(p):
    a1 = random.randrange(2, p)
    return a1

# p = 17
# a = 2
# b = 2
# x1 = 5
# y1 = 1
# mul = 3

# generate prime number
# key_length = 128
# p = randprime(2**(key_length-1), 2**key_length - 1)

# generate Alice and Bob keys
# a1 = random.randrange(2, p)
# b1 = random.randrange(2, p)
#
# # generate a and b
# while True:
#     a = random.randrange(2, p)
#     b = random.randrange(2, p)
#
#     if((4 * a**3 + 27 * b**2) % p != 0):
#         break
#
# # generate a random point
# x1, y1 = generate_random_point(a, b, p)
#
# print(f"a = {a}, b = {b}, p = {p}, x1 = {x1}, y1 = {y1}, Alice_key = {a1}, Bob_key = {b1}")
#
# pubAx, pubAy = calculate_public_key(x1, y1, p, a, a1)
# pubBx, pubBy = calculate_public_key(x1, y1, p, a, b1)
# print(f"Alice Public Key: {a1}P = ({pubAx}, {pubAy})")
# print(f"Bob Public Key: {b1}P = ({pubBx}, {pubBy})")
# shared_keyAx, shared_keyAy = calculate_public_key(pubBx, pubBy, p, a, a1)
# shared_keyBx, shared_keyBy = calculate_public_key(pubAx, pubAy, p, a, b1)
# print(f"Alice Shared Key: {(a1 * b1) % p}P = ({shared_keyAx}, {shared_keyAy})")
# print(f"Bob Shared Key: {(a1 * b1) % p}P = ({shared_keyBx}, {shared_keyBy})")