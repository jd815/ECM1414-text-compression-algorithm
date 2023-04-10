import os
from bitstring import BitArray

def convert_back():
    with open('output_file.bin', 'rb') as f:
	       bitstring = BitArray(f.read())
    bitstring = str(bitstring.bin)
    bitstring = bitstring.split("100000000000000000000000001")
    letter_binary_file = get_Codes(bitstring[0])
    uncompressed_string = ""
    code=""
    for digit in bitstring[1]:
        code = code+digit
        pos = 0
        for letter in letter_binary_file:
            if (code ==letter[1]):
                uncompressed_string = uncompressed_string + letter_binary_file[pos][0]
                code=""
            pos+=1
    return uncompressed_string

def get_Codes(tree_file):
    tree_file = tree_file.split("1000000000001")
    output = []
    for i in range(0,len(tree_file)-1, 2):
        temp = ["", ""]
        temp[0] = chr(int(tree_file[i], base=2))
        temp[1] = str(tree_file[i+1])
        output.append(temp)
    return output

def compress(name):
    def combine(nodes):
        pos = 0
        newnode = []
        if (len(nodes)>1):
            nodes.sort()
            nodes[pos].append("0")
            nodes[pos+1].append("1")
            combined_node1 = (nodes[pos][0]+nodes[pos+1][0])
            combined_node2 = (nodes[pos][1]+nodes[pos+1][1])
            newnode.append(combined_node1)
            newnode.append(combined_node2)
            newnodes = []
            newnodes.append(newnode)
            newnodes = newnodes + nodes[2:]
            nodes = newnodes
            huffman_tree.append(nodes)
            combine(nodes)
        return huffman_tree
    file_name = name
    file_stats = os.stat(file_name)
    uncompressed_file_size = file_stats.st_size
    user_input = open (file_name, 'r').read()

    #go through each letter, if its not in letters, add it and the frequency
    #and add letter to only_letters
    letters = []
    only_letters = []
    for letter in user_input:
        if letter not in letters:
            freq = user_input.count(letter)
            letters.append(freq)
            letters.append(letter)
            only_letters.append(letter)

    nodes = []
    while len(letters)>0:
        nodes.append(letters[0:2])
        letters = letters[2:]
    nodes.sort()
    huffman_tree = []
    huffman_tree.append(nodes)

    newnodes = combine(nodes)
    huffman_tree.sort(reverse=True)
    print("Here is the HUffman Tree, showing the merged nodes and binary pathways")
    print("NEWNODES ", newnodes)
    print("HUFFMAN ", huffman_tree)

    #This next is just for visualising
    checklist = []
    for level in huffman_tree:
        for node in level:
            if (node not in checklist):
                checklist.append(node)
            else:
                level.remove(node)
    count = 0
    for level in huffman_tree:
        print ("Level", count, ":", level)
        count +=1


    letter_binary = []
    if (len(only_letters) ==1):
        letter_code = [only_letters[0], "0"]
        letter_binary.append(letter_code*len(user_input))
    else:
        for letter in only_letters:
            lettercode = ""
            for node in checklist:
                if (len(node)>2 and letter in node[1]):
                    lettercode = lettercode + node[2]
            letter_code = [letter, lettercode]
            letter_binary.append(letter_code)

    #outputs letters with binary codes
    print("Your binary codes are as follows:")
    letter_binary_codes=""
    for letter in letter_binary:
        print(letter[0], letter[1])
        letter_binary_codes = letter_binary_codes + str(bin(ord(letter[0]))) + "1000000000001" + str(letter[1]) + "1000000000001"
    letter_binary_codes = letter_binary_codes[:-13]
    #Adding these zero's surrounded by 1s so that I know where the middle is. If it were just a bunch
    #of zeros or ones, they could interfere with the variables before ie if the previous piece of
    #data started with a 0 and I had 15 0s it would split my data one term too soon and then my binary tree
    #would be missing a 0 and my compressed data would have an extra one. Same is done for the binary tree
    #to separate the nodes from oen another. 
    bitstring = "100000000000000000000000001"
    for character in user_input:
        for item in letter_binary:
            if character in item:
                bitstring = bitstring +item[1]
    #convert to binary
    bitstring = letter_binary_codes + bitstring
    binary = BitArray(bin=bitstring)
    with open('output_file.bin', 'wb') as f:
        binary.tofile(f)

    file_stats_compressed = os.stat('output_file.bin')
    compressed_file_size = file_stats_compressed.st_size

    print("The original file size was ", uncompressed_file_size, " bytes. The compressed file is ",compressed_file_size)
    print("The compression ratio is", uncompressed_file_size/compressed_file_size)

action= input("Hello. Welcome to the Huffman compression and decompression system. Would you like to compress or decompress?\n")
while True:
    if action == "compress":
        name = input("Please input the name of the file. You do not need to add the .txt\n")
        file_name = name + ".txt"
        compress(file_name)
        action=input("If you wish to exit press ctr + c. Otherwise would you like to compress or decompress?\n")
    elif action == "decompress":
        print("your uncompressed string from the file is", convert_back())
        action=input("If you wish to exit press ctr + c. Otherwise would you like to compress or decompress?\n")
    else:
        action = input("Your input seems to be invalid. Please try again. (compress or decompress)\n")
