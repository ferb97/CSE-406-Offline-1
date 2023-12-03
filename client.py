# Import socket module
import socket
import AES as aes
import ECC as ecc

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

msg = s.recv(1024).decode()
p, a, x1, y1, A_x, A_y = msg.split(",")

p = int(p)
a = int(a)
x1 = int(x1)
y1 = int(y1)
A_x = int(A_x)
A_y = int(A_y)

bob_key = ecc.generate_bob_key(p)
B_x, B_y = ecc.calculate_public_key(x1, y1, p, a, bob_key)
msg = str(B_x) + "," + str(B_y)
s.send(msg.encode())

s_key_x, s_key_y = ecc.calculate_public_key(A_x, A_y, p, a, bob_key)
print(f"Shared key: ({s_key_x}, {s_key_y})")

binary_string = format(s_key_x, '0128b')
binary_groups = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
key_hex_array = [format(int(group, 2), '02X') for group in binary_groups]
print("Hex Array:", key_hex_array)

msg = s.recv(1024).decode()
print(f"Ciphered Text: {msg}")
ciphered_hex_array = msg.split(",")
deciphered_hex_array = aes.decrypt(ciphered_hex_array, key_hex_array)
deciphered_text = aes.convert_hex_array_to_ascii(deciphered_hex_array)
print(f"Deciphered Text: {deciphered_text}")

# hex_key = hex(s_key_x)
# hex_key_array = []
# for i in range(0, len(hex_key)):
#     hex_key_array.append(hex_key[i: i+2])
#
# print(f"Hex Array: ", end="")
# for i in range(0, len(hex_key_array)):
#     print(f"{hex_key_array[i]} ", end="")
# print()
# receive data from the server and decoding to get the string.
# print(s.recv(1024).decode())
# close the connection
s.close()