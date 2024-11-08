import heapq as hq
import os

class Node:
    def __init__(self, value, char, left=None, right=None):

        self.value = value
        self.char = char
        self.left = left
        self.right = right
        
        self.huffCode = ""

    def __lt__(self, other):
        return self.value < other.value
    

def scan_book(filename):
    charDict = {}       # make a dictionary to store all character frequencies

    with open(filename, "r", encoding="utf-8") as book:   # open the book
        for line in book:
            for char in line:
                if char not in charDict:    # if the character is not in the dictionary, make a new entry
                    charDict[char] = 1
                else:                       # if already in dictionary, add one to the frequency
                    charDict[char] += 1

    charList = [(frequency, char) for char, frequency in charDict.items()]   # convert the dictionary to a list of tuples for heapq module             # make the list a heap

    return charList


def build_code(node):

    codeDict = {}

    def recursive_bin(node, code):
            
            if node is None:
                return
            
            if node.char is not None:
                codeDict[node.char] = code
                return
    
            if node.left:
                recursive_bin(node.left, code + "0")
            if node.right:
                recursive_bin(node.right, code + "1")
                

    recursive_bin(node, "")

    return codeDict


def text_to_bin(filename, binCodes):
    
    binText = ""

    with open(filename, "r", encoding="utf-8") as book:
        for line in book:
            for char in line:
                if char in binCodes:
                    binText += binCodes[char]

    padding = (8 - (len(binText) % 8)) % 8

    binText += "0" * padding

    byteText = int(binText, 2).to_bytes(len(binText) // 8, byteorder="big")

    with open(filename + ".bin", "wb") as binFile:
        binFile.write(bytes([padding]))
        binFile.write(byteText)


def bin_to_text(binFile, codeDict):

    reversedCodeDict = {v: k for k, v in codeDict.items()}

    with open(binFile, "rb") as bin:
        padding = int.from_bytes(bin.read(1), byteorder="big")
        binText = bin.read()

    byteText = ''.join(format(byte, "08b") for byte in binText)

    if padding > 0:
        byteText = byteText[:-padding]

    decodedText = ""
    binToDecode = ""

    for bit in byteText:

        binToDecode += bit
        
        if binToDecode in reversedCodeDict:
            decodedText += reversedCodeDict[binToDecode]
            binToDecode = ""

    with open(binFile + ".decoded.txt", "w", encoding="utf-8") as decoded:
        decoded.write(decodedText)
                    

def build_tree(heap):

    while len(heap) > 1:

        left = hq.heappop(heap)
        right = hq.heappop(heap)

        newNode = Node(left.value + right.value, None, left, right)

        hq.heappush(heap, newNode)

    return hq.heappop(heap)


def build_heap(list):

    nodeList = []

    for x in range(len(list)):
        hq.heappush(nodeList, Node(list[x][0], list[x][1]))

    hq.heapify(nodeList)

    return nodeList


def compression_ratio(original, compressed):
    
    compressedSize = os.path.getsize(compressed)
    numSymbols = 0
    with open(original, "r", encoding="utf-8") as book:
        for line in book:
            for char in line:
                numSymbols += 1

    return compressedSize / numSymbols     

inputFiles = [
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book1.txt",
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book2.txt",
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book3.txt",
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book4.txt",
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book5.txt",
    "C:\\Users\\brada\\projects\\helloworld\\Data Structures\\HuffmanEncoding\\book6.txt"
]

for book in inputFiles:
    bookToRead = book
    book = scan_book(bookToRead)
    book = build_heap(book)
    book = build_tree(book)
    codeDict = build_code(book)
    text_to_bin(bookToRead, codeDict)
    bin_to_text(bookToRead + ".bin", codeDict)

    book_compression = compression_ratio(bookToRead, bookToRead + ".bin")

    print(f"Compression ratio for {bookToRead}: {book_compression:.2f}")
    print("\n")