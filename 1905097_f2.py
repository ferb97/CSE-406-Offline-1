import random
from sympy import randprime
import math
import time
from prettytable import PrettyTable


# Calculating Modular Inverse
def modinv(k, p):
    return pow(k, -1, p)


# Doubling Operation
def doubling(x1, y1, p, a):
    c = modinv(2 * y1, p)
    s = (3 * x1 ** 2 + a) % p
    s = (s * c) % p
    x3 = (s ** 2 - 2 * x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3


# Adding Operation
def addition(x1, y1, x2, y2, p):
    c = modinv(x2 - x1, p)
    s = (y2 - y1) % p
    s = (s * c) % p
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return x3, y3


# Determining y value of the point
def mem_s_i(i, x, p):
    return pow(x, (p - 1)>>i, p) == 1

def tonelli_sqrt(c, p):

    if not mem_s_i(1, c, p):
        return 0

    q = p - 1
    ell = 0
    while q % 2 == 0:
        ell = ell + 1
        q = q // 2

    while True:
        n = random.randrange(1, p)
        if not mem_s_i(1, n, p):
            break

    ninv = pow(n, p - 2, p)
    e = 0
    for i in range(2, ell + 1):
        if not mem_s_i(i, pow(ninv, e, p) * c, p):
            e = e + 2**(i - 1)

    a = pow(pow(ninv, e, p) * c, (q + 1) // 2, p)
    b = (pow(n, e // 2, p) * a) % p
    return b


# Generating a, b, prime p and a point on the curve
def generate_g_a_b_p(key_length):
    # generate p
    p = randprime(2**(key_length-1), 2**key_length - 1)

    # generate a and b
    while True:
        a = random.randrange(2, p)
        b = random.randrange(2, p)

        if((4 * a**3 + 27 * b**2) % p != 0):
            break

    # generate point
    while True:
        x1 = random.randrange(1, p)
        c = (x1 ** 3 + a * x1 + b) % p
        if c == 0:
            y1 = 0
            break

        y1 = tonelli_sqrt(c, p)
        if y1 != 0:
            break

    return p, a, b, x1, y1


# Calculating Lower Bound of Order of the curve
def lower_bound_of_order(p):
    return int(p + 1 - 2 * math.sqrt(p))


# Generate Private Key from the Prime
def generate_private_key(p):
    order_lower_bound = lower_bound_of_order(p)
    a1 = random.randrange(2, order_lower_bound)
    return a1


# Public Key Calculation
def calculate_public_key(x1, y1, p, a, mul):
    binary_representation = bin(mul)[2:]
    x3 = x1
    y3 = y1

    for i in range(1, len(binary_representation)):
        x3, y3 = doubling(x3, y3, p, a)
        if binary_representation[i] == '1':
            x3, y3 = addition(x3, y3, x1, y1, p)

    return x3, y3


# Shared Key Calculation
def calculate_shared_key(x1, y1, p, a, mul):
    return calculate_public_key(x1, y1, p, a, mul)


# Creating and Printing Table
def create_and_populate_table(key_length_list, avg_A_time, avg_B_time, avg_shared_key_time):
    table = PrettyTable()

    print(f"Computation Time: ")
    table.field_names = ["k", "A", "B", "shared key R"]
    for i in range(0, len(key_length_list)):
        table_row = []
        table_row.append(str(key_length_list[i]))
        table_row.append(str(avg_A_time[i]))
        table_row.append(str(avg_B_time[i]))
        table_row.append(str(avg_shared_key_time[i]))
        table.add_row(table_row)

    print(table)



def main():
    # Basic Key Lengths
    key_length_list = [128, 192, 256]

    # Saving Time for creating Table
    avg_A_time = []
    avg_B_time = []
    avg_shared_key_time = []

    for m in range(0, len(key_length_list)):
        key_length = key_length_list[m]
        # print(f"Key Length: {key_length}")

        # Total Number of Trials
        trials = 10
        A_generation_total = 0.0
        B_generation_total = 0.0
        shared_key_generation_total = 0.0

        for i in range(0, trials):
            # Generating p, a, b and a point
            p, a, b, x1, y1 = generate_g_a_b_p(key_length)

            # Calculating Alice Public Key
            A_start = time.time()
            alice_key = generate_private_key(p)
            alice_pub_x, alice_pub_y = calculate_public_key(x1, y1, p, a, alice_key)
            A_time = (time.time() - A_start) * 1000
            A_generation_total += A_time

            # Calculating Bob Public Key
            B_start = time.time()
            bob_key = generate_private_key(p)
            bob_pub_x, bob_pub_y = calculate_public_key(x1, y1, p, a, bob_key)
            B_time = (time.time() - B_start) * 1000
            B_generation_total += B_time

            # Calculating Shared Key for Alice
            shared_key_start = time.time()
            alice_shared_x, alice_shared_y = calculate_shared_key(bob_pub_x, bob_pub_y, p, a, alice_key)
            shared_key_time = (time.time() - shared_key_start) * 1000
            shared_key_generation_total += shared_key_time

            # Calculating Shared Key for Bob
            bob_shared_x, bob_shared_y = calculate_shared_key(alice_pub_x, alice_pub_y, p, a, bob_key)

            # print(f"Iteration {i + 1}: ")
            # print(f"Alice Shared Key: {alice_shared_x}")
            # print(f" Bob  Shared Key: {bob_shared_x}")


        # Calculating Average Time
        avg_A = A_generation_total / trials
        avg_B = B_generation_total / trials
        avg_shared_key = shared_key_generation_total / trials

        avg_A_time.append(avg_A)
        avg_B_time.append(avg_B)
        avg_shared_key_time.append(avg_shared_key)

        # print(f"A = {avg_A} ms")
        # print(f"B = {avg_B} ms")
        # print(f"Shared Key = {avg_shared_key} ms")

    # Print table
    create_and_populate_table(key_length_list, avg_A_time, avg_B_time, avg_shared_key_time)


if __name__ == "__main__":
    main()
