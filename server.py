# first of all import the socket library
import socket
import AES as aes
import ECC as ecc


# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()
    print('Got connection from', addr)

    p, a, b, x1, y1 = ecc.generate_g_a_b_p()
    alice_key = ecc.generate_alice_key(p)
    A_x, A_y = ecc.calculate_public_key(x1, y1, p, a, alice_key)

    msg = str(p) + "," + str(a) + "," + str(x1) + "," + str(y1) + "," + str(A_x) + "," + str(A_y)
    c.send(msg.encode())
    msg = c.recv(1024).decode()
    print(msg)
    B_x, B_y = msg.split(",")
    B_x = int(B_x)
    B_y = int(B_y)

    s_key_x, s_key_y = ecc.calculate_public_key(B_x, B_y, p, a, alice_key)
    print(f"Shared key: ({s_key_x}, {s_key_y})")

    # hex_key = hex(s_key_x)
    # hex_key_array = []
    # for i in range(0, len(hex_key)):
    #     hex_key_array.append(hex_key[i: i + 2])
    #
    # print(f"Hex Array: ", end="")
    # for i in range(0, len(hex_key_array)):
    #     print(f"{hex_key_array[i]} ", end="")
    # print()

    binary_string = format(s_key_x, '0128b')
    binary_groups = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
    key_hex_array = [format(int(group, 2), '02X') for group in binary_groups]
    print("Hex Array:", key_hex_array)

    plaintext = "Two One Nine Two"
    hex_plaintext = aes.convert_ascii_to_hex_array(plaintext)
    ciphered_hex_array, t = aes.encrypt(hex_plaintext, key_hex_array)
    msg = ""
    for i in range(0, len(ciphered_hex_array) - 1):
        msg += str(ciphered_hex_array[i]) + ","

    msg += str(ciphered_hex_array[len(ciphered_hex_array) - 1])
    # ciphered_text = aes.convert_hex_array_to_ascii(ciphered_hex_array)
    # print(f"Ciphered Text: {ciphered_text}")

    c.send(msg.encode())

    # deciphered_hex_array = aes.decrypt(ciphered_hex_array, hex_array)
    # deciphered_text = aes.convert_hex_array_to_ascii(deciphered_hex_array)
    # print(f"Deciphered Text: {deciphered_text}")
    # ciphered_hex_array = aes.convert_ascii_to_hex_array(msg)
    # deciphered_hex_array = aes.decrypt(ciphered_hex_array, key_hex_array)
    # deciphered_text = aes.convert_hex_array_to_ascii(deciphered_hex_array)
    # print(f"Deciphered Text: {deciphered_text}")

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break