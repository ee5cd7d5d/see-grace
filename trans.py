"""Transform NASA data into binary"""
import struct

with open("GNV1B_2002-04-04_A_02.dat", "rb", encoding=None) as input_file:
    # To ascertain the position of the header
    lines = input_file.read()
    NEWLINE_CHAR = 0x0A
    header_width = lines.find(NEWLINE_CHAR)
    print(header_width)
    LINE_COUNT = 0
    header_line = lines[0:header_width].decode("ascii")
    print(header_line)
    while not "END OF HEADER" in header_line:
        header_line = lines[(LINE_COUNT * header_width) :
                            ((LINE_COUNT + 1) * header_width)].decode("ascii")
        print(header_line)
        print(LINE_COUNT)
        LINE_COUNT += 1
    print(f"{(header_width * (LINE_COUNT + 1))} bytes in header")

    # To read the information to legible format
    IN_POS = header_width * (LINE_COUNT + 1)
    # Type of info to decode
    typeInfo = ["int", "chr", "chr", "dp", "dp", "dp", "dp",
            "dp", "dp", "dp", "dp", "dp", "dp", "dp", "dp",
            "uchar"]
    # Order of byte groups to decode
    bytePack = [4, 1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1]
    packTotal = sum(bytePack)  #Total length of pack. in bytes
    PACK_LENGTH = len(bytePack)
    if len(bytePack) == len(typeInfo):  # For debugging purposes
        print(True)
    decodPack = []
    leftoverBytes = (len(lines)- IN_POS)%packTotal
    print(leftoverBytes)        # To check if there are leftover bytes
    IN_POS += leftoverBytes     # So the initial position is adequate to finish in a block
    while IN_POS < len(lines):  # Iterate through the read file
        IC = 0
        for byte in bytePack:   # Iterate through one data pack
            if typeInfo[IC] == "int":
                decodPack.append(struct.unpack('>I',lines[IN_POS:(IN_POS+byte)]))
            if typeInfo[IC] == "chr":
                decodPack.append((lines[IN_POS:(IN_POS+byte)]).decode("ascii"))
            if typeInfo[IC] == "dp":
                decodPack.append(struct.unpack('>d',lines[IN_POS:(IN_POS+byte)]))
            if typeInfo[IC] == "uchar":
                decodPack.append((lines[IN_POS:(IN_POS+byte)].decode("ascii")))
            IN_POS += byte
            IC += 1
    print(decodPack)
