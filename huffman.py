class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the frequency count associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def __lt__(self, other):
        return comes_before(self, other) # Allows use of Python List sorting
    def __repr__(self):
        return ('(Char:'+ str(self.char) + ' Freq:' + str(self.freq)) #+ " (Left:" + str(self.left) + " Right:" + str(self.right)+'))')

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

def comes_before(a, b):
    if a.freq<b.freq:
        return True
    if a.freq==b.freq:
        return a.char<b.char
    return False
    #Returns True if node a comes before node b, False otherwise

def combine(a, b):
    if a.char<b.char:
        c=a.char
    else:
        c=b.char
    newNode=HuffmanNode(c,a.freq+b.freq)
    newNode.left=a
    newNode.right=b
    return newNode
    #Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    #The new node's frequency value will be the sum of the a and b frequencies
    #The new node's char value will be the lesser of the a and b char ASCII values

def cnt_freq(filename):
    try:
        file=open(filename)
    except:
        raise FileNotFoundError
    line=file.read()
    f_list= [0]*256
    file.close()
    for char in line:
        f_list[ord(char)]+=1
    return f_list
    #Opens a text file with a given file name (passed as a string) and counts the
    #frequency of occurrences of all the characters within that file
    #Returns a Python List with 256 entries - counts are initialized to zero.
    #The ASCII value of the characters are used to index into this list for the frequency counts

def create_huff_tree(freq_list):
    #Sort nodes
    if freq_list==[0]*256:
        return None
    srtd=[]
    for i in range(len(freq_list)):
        if freq_list[i]!=0:
            srtd.append(HuffmanNode(i, freq_list[i]))
    srtd.sort()
    while len(srtd)!=1:
        new=combine(srtd.pop(0),srtd.pop(0))
        srtd.append(new)
        srtd.sort()
    return srtd[0]
    #"""Input is the list of frequencies (provided by cnt_freq()).
    #Create a Huffman tree for characters with non-zero frequency
    #Returns the root node of the Huffman tree. Returns None if all counts are zero."""

def create_code(node):
    codes=['']*256
    if node==None:
        return codes
    return _leaves(node,codes,'')

    #"""Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation
    #as the index into the array, with the resulting Huffman code for that character stored at that location.
    #Characters that are unused should have an empty string at that location"""

def _leaves(node,codes,nums):
    if node.left==None and node.right==None:
        codes[node.char]=nums
    if node.left!=None:
        _leaves(node.left,codes, nums+ "0")
    if node.right!=None:
        _leaves(node.right,codes, nums+ "1")
    return codes



def create_header(freq_list):
    s=''
    first=True
    for i in range(len(freq_list)):
        if freq_list[i]!=0:
            if first==False:
                s+=' '
            s+=str(i)
            s+=' '
            s+=str(freq_list[i])
            first=False

    return s
    #Input is the list of frequencies (provided by cnt_freq()).
    #Creates and returns a header for the output file
    #Example: For the frequency list associated with "aaabbbbcc", would return “97 3 98 4 99 2”

def huffman_encode(in_file, out_file):
    input=in_file
    frq=cnt_freq(input)
    items=0
    for item in frq:
        if item!=0:
            items+=1
    if items==1:
        out = open(out_file, 'w')
        hdr = create_header(frq)
        out.write(hdr)
        out.close()
    else:
        out = open(out_file, 'w')
        hdr=create_header(frq)
        out.write(hdr + '\n')
        tree=create_huff_tree(frq)
        codes=create_code(tree)
        input=open(input)
        lines=''
        for line in input:
            lines+=line
        for char in lines:
            out.write(str(codes[ord(char)]))
        input.close()
        out.close()

def parse_header(header_string):
    freq_list=[0]*256
    values=header_string.split()
    if len(values)==2:
        return (True, values)
    for i in range(0, len(values)-1,2):
        freq_list[int(values[i])]=int(values[i+1])
    return freq_list

def huffman_decode(encoded_file,decode_file):
    try:
        in_file=open(encoded_file)
        out_file=open(decode_file,'w')
    except:
        raise FileNotFoundError
    hdr=in_file.readline()
    freq_list=parse_header(hdr)
    try:
        values=freq_list[1]
        char = chr(int(values[0]))
        for i in range(int(values[1])):
            out_file.write(char)
        out_file.close()
        in_file.close()
    except:
        node=create_huff_tree(freq_list)
        s=''
        for line in in_file:
            s+=line
        final=''
        for item in s:
            if item == '1':
                node = node.right
            elif item == '0':
                node = node.left
            if node.left==None and node.right==None:
                final+=chr(node.char)
                node=create_huff_tree(freq_list)
        in_file.close()
        out_file.write(final)
        out_file.close()



huffman_encode('final.txt','finalcheck.txt')





    #Takes input file name and output file name as parameters
    #Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    #Take note of special cases - empty file and file with only one unique character