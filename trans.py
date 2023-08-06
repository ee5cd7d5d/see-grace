<<<<<<< HEAD
"""Transform NASA data into binary"""
import struct
import logging

def find_header(counter, width):
    '''To get the position of END OF HEADER'''
    header_line = lines[0:width].decode("ascii")
    for i in range(0,len(lines)):
        header_line = lines[(i * width) :
                            ((i + 1) * width)].decode("ascii")
        logging.info(i)
        logging.info(header_line)
        if "END OF HEADER" in header_line:
            counter = i
            return width * (counter + 1), counter
    return -1, -1


logging.basicConfig(filename='example.log', encoding='utf-8',filemode='w', level=logging.DEBUG)
with open("GNV1B_2002-04-04_A_02.dat", "rb", encoding=None) as input_file:
    # To ascertain the position of the header
    lines = input_file.read()
    NEWLINE_CHAR = 0x0A  # from HEX reader for the file GNV
    header_width = lines.find(NEWLINE_CHAR)
    logging.info('Header width is %s', header_width)
    LINE_COUNT = 0
    firstline = lines[0:header_width].decode("ascii")
    print(firstline)
    IN_POS, LINE_COUNT = find_header(LINE_COUNT, header_width)
    logging.info("Position of last line, %s", LINE_COUNT)
    logging.info("%s bytes in header",IN_POS)
    if IN_POS == -1 or LINE_COUNT == -1:
        logging.error("End of header not found")

    # To read the information to legible format
    logging.info("Initial position, %s",IN_POS)
    typeInfo = ["int", "chr", "chr", "dp", "dp", "dp", "dp",     # Type of info to decode
            "dp", "dp", "dp", "dp", "dp", "dp", "dp", "dp",
            "uchar"]
    bytePack = [4, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1]  # Order of byte groups to decode
    packTotal = sum(bytePack)  #Total length of pack. in bytes
    logging.info("The length of a pack. is %s",packTotal)
    PACK_LENGTH = len(bytePack)
    # For debugging purposes
    if len(bytePack) == len(typeInfo):
        logging.info('There is an information type for each set of bytes')
    else:
        logging.warning('There are leftover packs of data without a type of information')
    decodPack = []
    # To check if there are leftover bytes
    leftoverBytes = (len(lines)- IN_POS)%packTotal
    logging.warning('There are %s leftover bytes',leftoverBytes)
    if leftoverBytes:
        IN_POS += leftoverBytes     # So the initial position is adequate to finish in a block
    logging.warning('The initial position has been switched to %s', IN_POS)
    # To interpret the information
    while IN_POS < len(lines):  # Iterate through the read file
        IC = 0
        for byte in bytePack:   # Iterate through one data pack
            if typeInfo[IC] == "int":
                decodPack.append(struct.unpack('>I',lines[IN_POS:(IN_POS+byte)]))
            elif typeInfo[IC] == "chr":
                decodPack.append((lines[IN_POS:(IN_POS+byte)]).decode("ascii"))
            elif typeInfo[IC] == "dp":
                decodPack.append(struct.unpack('>d',lines[IN_POS:(IN_POS+byte)]))
            elif typeInfo[IC] == "uchar":
                decodPack.append((lines[IN_POS:(IN_POS+byte)].decode("ascii")))
            IN_POS += byte
            IC += 1
    print(decodPack[0:160])
=======
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
>>>>>>> 9b1353e (Binconv (#3))
