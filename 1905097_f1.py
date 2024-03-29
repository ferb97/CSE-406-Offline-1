from BitVector import *
import time
import random

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

Mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

InvMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

round_constant = [
    [BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="01"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="02"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="04"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="08"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="10"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="20"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="40"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="80"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="1B"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")],
    [BitVector(hexstring="36"), BitVector(hexstring="00"), BitVector(hexstring="00"), BitVector(hexstring="00")]
]

# Converting ascii to hex array
def convert_ascii_to_hex_array(plaintext, padding = False):
    hex_plaintext = plaintext.encode('utf-8').hex()
    hex_array = []
    for i in range(0, len(hex_plaintext), 2):
        hex_array.append(hex_plaintext[i:i+2])

    # padding if needed
    if padding:
        padding_length = (16 - len(hex_array) % 16) % 16
        if padding_length == 0:
            padding_length = 16

        for i in range(0, padding_length):
            hex_array.append(format(padding_length, '02x'))

    return hex_array


# Converting hex array to ascii
def convert_hex_array_to_ascii(hex_array, padding = False):
    ascii_string = ""
    for i in range(0, len(hex_array)):
        ascii_string += chr(int(hex_array[i], 16))

    # Remove padding if needed
    if padding:
        padding_length = int(hex_array[len(hex_array) - 1], 16)
        ascii_string = ascii_string[:-padding_length]

    return ascii_string


# Convert hex array to bit vector
def convert_hex_array_to_bitvector(hex_value_array):
    bit_vector1 = []

    for i in range(0, 4):
        bit_vector_row = []
        for j in range(i, len(hex_value_array), 4):
            bit_vector = BitVector(hexstring=hex_value_array[j])
            bit_vector_row.append(bit_vector)

        bit_vector1.append(bit_vector_row)

    return bit_vector1



# Convert bit vector to hex array
def convert_bitvector_to_hex_array(bit_vector1):
    hex_array = []
    for j in range(0, 4):
        for i in range(0, 4):
            hex_array.append(bit_vector1[i][j].getHexStringFromBitVector())

    return hex_array


# Adding Round key
def add_round_key(bit_vector_plaintext, bit_vector_round_key):

    for i in range(0, 4):
        for j in range(0, 4):
            bit_vector_plaintext[i][j] ^= bit_vector_round_key[i][j]

    return bit_vector_plaintext


# Substituting Bytes using Sbox
def substitute_bytes(bit_vector_plaintext):
    for i in range(0, 4):
        for j in range(0, 4):
            c = bit_vector_plaintext[i][j].intValue()
            bit_vector_plaintext[i][j] = BitVector(intVal=Sbox[c], size=8)

    return bit_vector_plaintext


# Inverse Substituting Bytes using InvSbox
def inverse_substitute_bytes(bit_vector_plaintext):
    for i in range(0, 4):
        for j in range(0, 4):
            c = bit_vector_plaintext[i][j].intValue()
            bit_vector_plaintext[i][j] = BitVector(intVal=InvSbox[c], size=8)

    return bit_vector_plaintext


# Shift Rows Left
def shift_rows(bit_vector_plaintext):
    for i in range(0, 4):
        bit_vector_plaintext[i] = bit_vector_plaintext[i][i:] + bit_vector_plaintext[i][:i]

    return bit_vector_plaintext


# Shift Rows Right
def inverse_shift_rows(bit_vector_plaintext):
    for i in range(0, 4):
        bit_vector_plaintext[i] = bit_vector_plaintext[i][4 - i:] + bit_vector_plaintext[i][:4 - i]

    return bit_vector_plaintext


# Mix Columns
def mix_columns(bit_vector_plaintext):
    result_matrix = []
    for i in range(0, 4):
        result_matrix_row = []
        for j in range(0, 4):
            tmp1 = Mixer[i][0].gf_multiply_modular(bit_vector_plaintext[0][j], AES_modulus, 8)
            tmp1 ^= Mixer[i][1].gf_multiply_modular(bit_vector_plaintext[1][j], AES_modulus, 8)
            tmp1 ^= Mixer[i][2].gf_multiply_modular(bit_vector_plaintext[2][j], AES_modulus, 8)
            tmp1 ^= Mixer[i][3].gf_multiply_modular(bit_vector_plaintext[3][j], AES_modulus, 8)
            result_matrix_row.append(tmp1)

        result_matrix.append(result_matrix_row)

    return result_matrix


# Inverse Mix Columns
def inverse_mix_columns(bit_vector_plaintext):
    result_matrix = []
    for i in range(0, 4):
        result_matrix_row = []
        for j in range(0, 4):
            tmp1 = InvMixer[i][0].gf_multiply_modular(bit_vector_plaintext[0][j], AES_modulus, 8)
            tmp1 ^= InvMixer[i][1].gf_multiply_modular(bit_vector_plaintext[1][j], AES_modulus, 8)
            tmp1 ^= InvMixer[i][2].gf_multiply_modular(bit_vector_plaintext[2][j], AES_modulus, 8)
            tmp1 ^= InvMixer[i][3].gf_multiply_modular(bit_vector_plaintext[3][j], AES_modulus, 8)
            result_matrix_row.append(tmp1)

        result_matrix.append(result_matrix_row)

    return result_matrix


# Calculating g function value
def calculate_g_function(g1_result, round_num):

    g_result = [bit_vector.deep_copy() for bit_vector in g1_result]

    # Left Shift
    g_result = g_result[1:] + g_result[:1]

    # Substitute Bytes
    for i in range(0, 4):
        c = g_result[i].intValue()
        g_result[i] = BitVector(intVal=Sbox[c], size=8)

    # Adding Round Constant
    g_result = [v1 ^ v2 for v1, v2 in zip(round_constant[round_num], g_result)]
    return g_result


def calculate_round_keys(bit_vector_round_key):
    round_keys = []

    # Appending Round 0 Key
    for i in range(0, 4):
        round_keys.append(bit_vector_round_key[i])

    # Appending other Round Keys
    for k in range(1, 11):

        tmp_vector = []
        for j in range(0, 4):
            tmp_vector_row = []
            for i in range(0, 4):
                tmp_vector_row.append(bit_vector_round_key[i][j])
            tmp_vector.append(tmp_vector_row)

        g_result = calculate_g_function(tmp_vector[3], k)

        # Calculate Next 4 Words
        tmp_vector[0] = [v1 ^ v2 for v1, v2 in zip(tmp_vector[0], g_result)]
        tmp_vector[1] = [v1 ^ v2 for v1, v2 in zip(tmp_vector[1], tmp_vector[0])]
        tmp_vector[2] = [v1 ^ v2 for v1, v2 in zip(tmp_vector[2], tmp_vector[1])]
        tmp_vector[3] = [v1 ^ v2 for v1, v2 in zip(tmp_vector[3], tmp_vector[2])]

        result = [[tmp_vector[j][i] for j in range(4)] for i in range(4)]
        for i in range(0, 4):
            round_keys.append(result[i])
        bit_vector_round_key = result

    return round_keys


# Encryption
def encrypt(hex_plaintext_array, hex_round0_key_array, initial_bit_vector):

    ciphered_hex_array_final = []

    # Key Expansion
    bit_vector_round_key = convert_hex_array_to_bitvector(hex_round0_key_array)
    key_schedule_start_time = time.time()
    round_key_vectors = calculate_round_keys(bit_vector_round_key)
    key_schedule_time = (time.time() - key_schedule_start_time) * 1000

    # Encryption for each 16 bytes
    for m in range(0, len(hex_plaintext_array), 16):
        bit_vector_plaintext = convert_hex_array_to_bitvector(hex_plaintext_array[m:m+16])

        # Adding initial bit vector or previous encrypted array
        if m != 0:
            prev_bit_vector = convert_hex_array_to_bitvector(ciphered_hex_array_final[m-16:m])
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, prev_bit_vector)
        else:
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, initial_bit_vector)

        # Add Round Key
        bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[0: 4])

        for i in range(1, 10):

            # Substitute Bytes
            bit_vector_plaintext = substitute_bytes(bit_vector_plaintext)

            # Shift Rows
            bit_vector_plaintext = shift_rows(bit_vector_plaintext)

            # Mix Columns
            bit_vector_plaintext = mix_columns(bit_vector_plaintext)

            # Adding Round Key
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[i * 4: (i + 1) * 4])

        # Substitute Bytes
        bit_vector_plaintext = substitute_bytes(bit_vector_plaintext)

        # Shift Rows
        bit_vector_plaintext = shift_rows(bit_vector_plaintext)

        # Add Round Key
        bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[40: 44])

        ciphered_hex_array = convert_bitvector_to_hex_array(bit_vector_plaintext)
        for i in range(0, len(ciphered_hex_array)):
            ciphered_hex_array_final.append(ciphered_hex_array[i])

    return ciphered_hex_array_final, key_schedule_time


# Printing Bit Vector
def print_bitvector(bit_vector_plaintext):
    for i in range(0, 4):
        for j in range(0, 4):
            print(f"{bit_vector_plaintext[i][j].getHexStringFromBitVector()} ", end='')
        print()
    print()


# Printing Hex Array
def print_hex_array(hex_array):
    for i in range(0, len(hex_array)):
        print(f"{hex_array[i]} ", end='')
    print()


# Decryption
def decrypt(ciphered_hex_array, hex_round0_key_array, initial_bit_vector):

    deciphered_hex_array_final = []

    # Key Expansion
    bit_vector_round_key = convert_hex_array_to_bitvector(hex_round0_key_array)
    round_key_vectors = calculate_round_keys(bit_vector_round_key)

    for m in range(len(ciphered_hex_array), 0, -16):
        bit_vector_plaintext = convert_hex_array_to_bitvector(ciphered_hex_array[m-16:m])

        # Add Round Key
        bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[40: 44])

        for i in range(1, 10):

            # Inverse Shift Rows
            bit_vector_plaintext = inverse_shift_rows(bit_vector_plaintext)

            # Inverse Substitute Bytes
            bit_vector_plaintext = inverse_substitute_bytes(bit_vector_plaintext)

            # Add Round Key
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[(10 - i) * 4: (11 - i) * 4])

            # Inverse Mix Columns
            bit_vector_plaintext = inverse_mix_columns(bit_vector_plaintext)

        # Inverse Shift Rows
        bit_vector_plaintext = inverse_shift_rows(bit_vector_plaintext)

        # Inverse Substitute Bytes
        bit_vector_plaintext = inverse_substitute_bytes(bit_vector_plaintext)

        # Add Round Key
        bit_vector_plaintext = add_round_key(bit_vector_plaintext, round_key_vectors[0: 4])

        # Adding initial bit vector or previous ciphertext
        if m != 16:
            prev_bit_vector = convert_hex_array_to_bitvector(ciphered_hex_array[m-32:m-16])
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, prev_bit_vector)

        else:
            bit_vector_plaintext = add_round_key(bit_vector_plaintext, initial_bit_vector)


        deciphered_hex_array = convert_bitvector_to_hex_array(bit_vector_plaintext)
        for i in range(len(deciphered_hex_array) - 1, -1, -1):
            deciphered_hex_array_final.append(deciphered_hex_array[i])


    deciphered_hex_array_final.reverse()
    return deciphered_hex_array_final


# Generate Random Bit Vector
def generate_initial_bitvector():
    bitvector = []

    for i in range(4):
        bit_vector_row = []
        for j in range(4):
            hex_value = format(random.randint(0, 255), '02X')
            bit_vector_row.append(BitVector(hexstring=hex_value))

        bitvector.append(bit_vector_row)

    return bitvector


AES_modulus = BitVector(bitstring='100011011')

def main():
    initial_bitvector = generate_initial_bitvector()

    # Input Plaintext and Round0 key
    plaintext = input("Enter Plaintext: ")
    round0_key = input("Enter Round0 key: ")

    # Converting to Hex Array
    hex_plaintext_array = convert_ascii_to_hex_array(plaintext, True)
    hex_round0_key_array = convert_ascii_to_hex_array(round0_key)

    print("Key:")
    print(f"In ASCII: {round0_key}")
    print("In HEX: ", end='')
    print_hex_array(hex_round0_key_array)
    print()

    print("Plain Text:")
    print(f"In ASCII: {plaintext}")
    print("In HEX: ", end='')
    print_hex_array(hex_plaintext_array)
    print()

    encryption_start_time = time.time()
    ciphered_hex_array, key_schedule_time = encrypt(hex_plaintext_array, hex_round0_key_array, initial_bitvector)
    encryption_time = (time.time() - encryption_start_time) * 1000
    ciphered_ascii_string = convert_hex_array_to_ascii(ciphered_hex_array)

    print("Ciphered Text:")
    print("In HEX: ", end='')
    print_hex_array(ciphered_hex_array)
    print(f"In ASCII: {ciphered_ascii_string}")
    print()

    decryption_start_time = time.time()
    deciphered_hex_array = decrypt(ciphered_hex_array, hex_round0_key_array, initial_bitvector)
    decryption_time = (time.time() - decryption_start_time) * 1000
    deciphered_ascii_string = convert_hex_array_to_ascii(deciphered_hex_array, True)

    print("Deciphered Text:")
    print("In HEX: ", end='')
    print_hex_array(deciphered_hex_array)
    print(f"In ASCII: {deciphered_ascii_string}")
    print()

    print("Execution Time Details:")
    print(f"Key Schedule Time: {key_schedule_time} ms")
    print(f"Encryption Time: {encryption_time} ms")
    print(f"Decryption Time: {decryption_time} ms")


if __name__ == "__main__":
    main()