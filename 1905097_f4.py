import socket
import importlib
aes = importlib.import_module('1905097_f1')
ecc = importlib.import_module('1905097_f2')

# Creating Socket
s = socket.socket()

# Connecting to Port
port = 12345
s.connect(('127.0.0.1', port))

# Receiving message for getting the values of a, b, p and the point G
msg = s.recv(1024).decode()
p, a, x1, y1, A_x, A_y = msg.split(",")

p = int(p)
a = int(a)
x1 = int(x1)
y1 = int(y1)
A_x = int(A_x)
A_y = int(A_y)

# Calculating Bob Public Key
bob_key = ecc.generate_private_key(p)
B_x, B_y = ecc.calculate_public_key(x1, y1, p, a, bob_key)

# Sending Bob Public Key
msg = str(B_x) + "," + str(B_y)
s.send(msg.encode())

# Calculating Shared Key
s_key_x, s_key_y = ecc.calculate_shared_key(A_x, A_y, p, a, bob_key)
print(f"Shared key: {s_key_x}")

# Calculating Round 0 Key
binary_string = format(s_key_x, '0128b')
binary_groups = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]
key_hex_array = [format(int(group, 2), '02X') for group in binary_groups]

# Receiving Initial Bit Vector
msg = s.recv(1024).decode()
initial_vector_hex_array = msg.split(",")
initial_bit_vector = aes.convert_hex_array_to_bitvector(initial_vector_hex_array)

# Receiving Cipher Text
msg = s.recv(1024).decode()
ciphered_hex_array = msg.split(",")

# Deciphering Message
deciphered_hex_array = aes.decrypt(ciphered_hex_array, key_hex_array, initial_bit_vector)
deciphered_text = aes.convert_hex_array_to_ascii(deciphered_hex_array, True)
print(f"Deciphered Text: {deciphered_text}")

# Close Connection
s.close()