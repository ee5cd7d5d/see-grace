"""Transform NASA data into binary"""
import struct
import logging


def find_header(lines, counter, width):
    """To get the position of END OF HEADER"""
    header_line = lines[0:width].decode("ascii")
    for i in range(0, len(lines)):
        header_line = lines[(i * width) : ((i + 1) * width)].decode("ascii")
        logging.info(i)
        logging.info(header_line)
        if "END OF HEADER" in header_line:
            counter = i
            return width * (counter + 1), counter
    return -1, -1


def read_pack(name_dfr):
    """To read the input info from the Data Format Record"""
    with open("infos.txt", "r", encoding="UTF-8") as info_read:
        raw_file = info_read.readlines()
        read_data = []
        for line in raw_file:
            read_data.append(
                line.strip()
            )  # transform the .txt into a str list w/o '\n'
        in_pos = read_data.index(
            name_dfr
        )  # reference name input  of the Data Format Record group
        fin_pos = read_data.index("exit" + name_dfr)  # reference to exit the DFR group
        group_data = []
        for counter in range(
            in_pos + 1, fin_pos
        ):  # to get whole designated DFR pack info from .txt
            group_data.append(read_data[counter])
        ref = [0, 0, 0]
        ref[0] = group_data.index("type")  # ref. mark for type list in .txt
        ref[1] = group_data.index("byte_pack")  # mark for byte packs list in .txt
        ref[2] = group_data.index("varnam")  # mark for variable name list in .txt
        types = []
        byte_con = []
        names = []
        for counter in range(ref[0] + 1, ref[1]):  # to get type of data list
            types.append(group_data[counter])
        for counter in range(ref[1] + 1, ref[2]):  # to get byte group length list
            byte_con.append(group_data[counter])
        for counter in range(ref[2] + 1, len(group_data)):  # to get var. names list
            names.append(group_data[counter])
        byte_int = [int(x) for x in byte_con]
        return types, byte_int, names  # output in str lists


NEWLINE_CHAR = 0x0A  # from HEX reader for the file GNV


def get_header_width(binary_data: bytearray) -> int:
    "Returns header width with a fixed separator defined globally"
    header_width = binary_data.find(NEWLINE_CHAR)
    return header_width


logging.basicConfig(
    filename="example.log", encoding="utf-8", filemode="w", level=logging.DEBUG
)


def main():
    "Main function"
    with open("GNV1B_2002-04-04_A_02.dat", "rb", encoding=None) as input_file:
        # To ascertain the position of the header
        lines = input_file.read()
        header_width = get_header_width(lines)
        logging.info("Header width is %s", header_width)
        line_count = 0
        firstline = lines[0:header_width].decode("ascii")
        print(firstline)
        in_pos, line_count = find_header(lines, line_count, header_width)
        logging.info("Position of last line, %s", line_count)
        logging.info("%s bytes in header", in_pos)
        if in_pos == -1 or line_count == -1:
            logging.error("End of header not found")

        # To read the information to legible format
        type_info, byte_pack, var_names = read_pack("GNV1B")
        logging.info(type_info, byte_pack, var_names)
        logging.info("Initial position, %s", in_pos)
        pack_total = sum(byte_pack)  # Total length of pack. in bytes
        logging.info("The length of a pack. is %s", pack_total)
        # For debugging purposes
        if len(byte_pack) == len(type_info):
            logging.info("There is an information type for each set of bytes")
        else:
            logging.warning(
                "There are leftover packs of data without a type of information"
            )
        # To check if there are leftover bytes
        leftover_bytes = (len(lines) - in_pos) % pack_total
        logging.warning("There are %s leftover bytes", leftover_bytes)
        if leftover_bytes:
            in_pos += leftover_bytes  # So the initial position is adequate to finish in a block
        logging.warning("The initial position has been switched to %s", in_pos)
        # To interpret the information
        decode_pack = []
        while in_pos < len(lines):  # Iterate through the read file
            i = 0
            for byte in byte_pack:  # Iterate through one data pack
                if type_info[i] == "int":
                    decode_pack.append(
                        struct.unpack(">I", lines[in_pos : (in_pos + byte)])
                    )
                elif type_info[i] == "chr":
                    decode_pack.append(
                        (lines[in_pos : (in_pos + byte)]).decode("ascii")
                    )
                elif type_info[i] == "dp":
                    decode_pack.append(
                        struct.unpack(">d", lines[in_pos : (in_pos + byte)])
                    )
                elif type_info[i] == "uchar":
                    decode_pack.append(
                        (lines[in_pos : (in_pos + byte)].decode("ascii"))
                    )
                in_pos += byte
                i += 1
        print(decode_pack[0:160])


if __name__ == "__main__":
    main()
