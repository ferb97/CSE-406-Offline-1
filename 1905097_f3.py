import socket
import AES as aes
import ECC as ecc

# Creating Socket
s = socket.socket()
print("Socket successfully created")

# Binding Socket
port = 12345
s.bind(('', port))
print("socket binded to %s" % (port))

# Listening to Port
s.listen(5)
print("socket is listening")

while True:

    # Connection from Client
    c, addr = s.accept()
    print('Got connection from', addr)

    # Generating Alice Public Key
    key_length = 128
    p, a, b, x1, y1 = ecc.generate_g_a_b_p(key_length)
    alice_key = ecc.generate_private_key(p)
    A_x, A_y = ecc.calculate_public_key(x1, y1, p, a, alice_key)

    # Sending Message
    msg = str(p) + "," + str(a) + "," + str(x1) + "," + str(y1) + "," + str(A_x) + "," + str(A_y)
    c.send(msg.encode())

    # Generating Shared Key
    msg = c.recv(1024).decode()
    B_x, B_y = msg.split(",")
    B_x = int(B_x)
    B_y = int(B_y)

    s_key_x, s_key_y = ecc.calculate_shared_key(B_x, B_y, p, a, alice_key)
    print(f"Shared key: {s_key_x}")

    # Generating Key for Round 0
    binary_string = format(s_key_x, '0128b')
    binary_groups = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    key_hex_array = [format(int(group, 2), '02X') for group in binary_groups]

    # Generating Initial Bit Vector
    initial_bitvector = aes.generate_initial_bitvector()
    initial_vector_hex_array = aes.convert_bitvector_to_hex_array(initial_bitvector)

    # Sending Initial Bit Vector
    msg = ""
    for i in range(0, len(initial_vector_hex_array) - 1):
        msg += str(initial_vector_hex_array[i]) + ","

    msg += str(initial_vector_hex_array[len(initial_vector_hex_array) - 1])
    c.send(msg.encode())

    # Input the Plaintext
    plaintext = input("Enter Plaintext: ")
    print(f"Sent Message: {plaintext}")
    hex_plaintext = aes.convert_ascii_to_hex_array(plaintext, True)

    # Cipher Text
    ciphered_hex_array, t = aes.encrypt(hex_plaintext, key_hex_array, initial_bitvector)

    # Sending Cipher Message
    msg = ""
    for i in range(0, len(ciphered_hex_array) - 1):
        msg += str(ciphered_hex_array[i]) + ","

    msg += str(ciphered_hex_array[len(ciphered_hex_array) - 1])
    c.send(msg.encode())

    # Closing Connection
    c.close()

    break