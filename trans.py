"""Transform NASA data into binary"""
import struct
import logging
import matplotlib.pyplot as plt

def read_howmany_names():
    '''To read the filename and the number of DFR files that have
    to be interpreted from infos.txt'''
    with open("infos.txt", "r", encoding="UTF-8") as info_read:
        raw_file = info_read.readlines()
        read_data = []
        # Getting the name of the files so the file manager can find it
        for line in raw_file:
            read_data.append(line.strip())
        in_pos = read_data.index("filestoread")
        fin_pos= read_data.index("endfilestoread")
        name_files = []
        i = 0
        for counter in range(in_pos+1, fin_pos):
            name_files.append(read_data[counter])
            i += 1
        if i:
            return name_files, i #returns string list of files and how many of them to read
        return 'No groups to read'


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

def read_dfr(name_dfr):
    '''To read the input info from the Data Format Record (DFR)'''
    with open("infos.txt", "r", encoding="UTF-8") as info_read:
        raw_file = info_read.readlines()
        read_data = []
        types = [[]  for x in range(len(name_dfr))]
        byte_int = [[] for x in range(len(name_dfr))]
        names = [[] for x in range(len(name_dfr))]
        for line in raw_file:
            read_data.append(line.strip())  # transform the .txt into a str list w/o '\n'
        for _x, dat_names in enumerate(name_dfr): #iter. through each filename
            byte_con = []
            group_data = []
            ref = [0,0,0,0,0]
            ref[0] = read_data.index(dat_names.split('_',1)[0]) # reference to enter DFR group
            ref[1] = read_data.index("exit"+dat_names.split('_',1)[0])  # exit DFR reference
            for counter in range(ref[0]+1,ref[1]): # to get designated DFR pack info from .txt
                group_data.append(read_data[counter])
            ref[2] = group_data.index("type") # ref. mark for type list in .txt
            ref[3] = group_data.index("bytepack") # mark for byte packs list in .txt
            ref[4] = group_data.index("varnam") # mark for variable name list in .txt
            for counter in range(ref[2] + 1, ref[3]):  # to get type of data list
                types[_x].append(group_data[counter])
            for counter in range(ref[3] + 1, ref[4]):  # to get byte group length list
                byte_con.append(group_data[counter])
            for counter in range(ref[4] + 1, len(group_data)):  # to get var. names list
                names[_x].append(group_data[counter])
            byte_int[_x] = [int(x) for x in byte_con]
    return types, byte_int, names   #output in str lists

def list_for_plotting(decod,namevar,varstring):
    '''Getting a list with a specific DFR variable values'''
    pos=varstring.index(namevar)
    var_of_interest = []
    _s = pos
    while _s < len(decod):
        var_of_interest.append(decod[_s])
        _s += len(varstring) - 1
    return var_of_interest


class InvalidReturnStatement(Exception):
    '''Class to check header performance'''
    def __init__(self):
        super().__init__('End of header not found')




logging.basicConfig(filename='example.log', encoding='utf-8',filemode='w', level=logging.DEBUG)
fileNames, numFiles = read_howmany_names()
typeInfo, bytePack, varNames = read_dfr(fileNames) # getting the information to know what to read
decodPack = [[]  for x in range(numFiles)] # empty list of lists to store results
print(fileNames)
for _n in range(numFiles): # to iterate through each set of data
    with open(fileNames[_n], "rb", encoding=None) as input_file:
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
        # if IN_POS or LINE_COUNT == -1:
        #     raise InvalidReturnStatement
        # -----------------------------------------
        # To read the information to legible format
        logging.info(typeInfo, bytePack, varNames)
        logging.info("Initial position, %s",IN_POS)
        packTotal = sum(bytePack[_n])  #Total length of pack. in bytes
        logging.info("The length of a pack. is %s",packTotal)
        PACK_LENGTH = len(bytePack[_n])
        # For debugging purposes
        if len(bytePack[_n]) == len(typeInfo[_n]):
            logging.info('There is an information type for each set of bytes')
        else:
            logging.warning('There are leftover packs of data without a type of information')
        # To check if there are leftover bytes
        leftoverBytes = (len(lines)- IN_POS)%packTotal
        logging.warning('There are %s leftover bytes',leftoverBytes)
        if leftoverBytes:
            IN_POS += leftoverBytes     # So the initial position is adequate to finish in a block
        logging.warning('The initial position has been switched to %s', IN_POS)
        # To interpret the information
        while IN_POS < len(lines):      # Iterate through the read file
            IC = 0
            for byte in bytePack[_n]:   # Iterate through one data pack
                if typeInfo[_n][IC] == "int":
                    decodPack[_n].append(struct.unpack('>I',lines[IN_POS:(IN_POS+byte)]))
                elif typeInfo[_n][IC] == "chr":
                    decodPack[_n].append((lines[IN_POS:(IN_POS+byte)]).decode("ascii"))
                elif typeInfo[_n][IC] == "dp":
                    decodPack[_n].append(struct.unpack('>d',lines[IN_POS:(IN_POS+byte)]))
                elif typeInfo[_n][IC] == "uchar":
                    decodPack.append((lines[IN_POS:(IN_POS+byte)].decode("ascii")))
                IN_POS += byte
                IC += 1
#print(decodPack[0][0:160],decodPack[1][0:160])
#
#To plot some info

gps_time = list_for_plotting(decodPack[0], 'gps_time', varNames[0])
xpos = list_for_plotting(decodPack[0], 'xpos', varNames[0])
ypos = list_for_plotting(decodPack[0], 'ypos', varNames[0])
zpos = list_for_plotting(decodPack[0], 'zpos', varNames[0])
ax = plt.figure().add_subplot(projection='3d')
ax.plot(xpos,ypos,zpos,label='Trajectory of GRACE')
ax.legend()
plt.show()
