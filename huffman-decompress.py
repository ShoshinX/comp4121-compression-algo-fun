import sys
import huffmancoding

def main(args):
    if len(args) != 2:
        sys.exit("Usage: python huffman-decompress.py InputFile OutputFile")
    inputfile, outputfile = args
    with open(inputfile,"rb") as inp, open(outputfile, "wb") as out:
        bitin = huffmancoding.BitInputStream(inp)
        canoncode = read_code_len_table(bitin)
        code = canoncode.to_code_tree()
        decompress(code, bitin, out)

def read_code_len_table(bitin):
    def read_int(n):
        result = 0
        for _ in range(n):
            result = (result << 1) | bitin.read_no_eof() # big Endian
        return result
    codelengths = [read_int(8) for _ in range(257)]
    return huffmancoding.CanonicalCode(codelengths=codelengths)

def decompress(code, bitin, out):
    dec = huffmancoding.HuffmanDecoder(bitin)
    dec.codetree = code
    while True:
        symbol = dec.read()
        if symbol == 256: #EOF
            break
        out.write(bytes((symbol,)))

if __name__ == "__main__":
    main(sys.argv[1:])
