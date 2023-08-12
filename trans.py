'''Transform NASA data into binary'''

with open('GNV1B_2002-04-04_A_02.dat', 'rb', encoding=None) as input_file:
    lines = input_file.read()
    res = []                    # empty array
    for byte in lines:
        binary_rep = bin(byte)  # convert to binary representation
        res.append(binary_rep)  # add to list
    #print(res)

with open('convertedres.dat','x', encoding='UTF-8') as create_file:
    for line in res:
        create_file.write(" ".join(line) + "\n")
