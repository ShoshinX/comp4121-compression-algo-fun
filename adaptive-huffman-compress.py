
import contextlib, sys
import huffmancoding

def main(args):
    if len(args) != 2:
        sys.exit("Usage: python adaptive-huffman-compress.py InputFile OutputFile")
    inputfile, outputfile = args
    with open(inputfile, "rb") as inp, contextlib.closing(huffmancoding.BitOutputStream(open(outputfile,"wb"))) as bitout:
        compress(inp,bitout)

def compress(inp, bitout):
    initfreqs = [1] * 257
    freqs = huffmancoding.FrequencyTable(initfreqs)
    enc = huffmancoding.HuffmanEncoder(bitout)
    enc.codetree = freqs.build_code_tree()
    count = 0
    while True:
        symbol = inp.read(1)
        if len(symbol) == 0:
            break
        enc.write(symbol[0])
        count += 1
        freqs.increment(symbol[0])
        if (count < 262144 and is_power_of_2(count)) or count % 262144 == 0:
            enc.codetree = freqs.build_code_tree()
        if count % 262144 == 0:
            freqs = huffmancoding.FrequencyTable(initfreqs)
    enc.write(256) #EOF

def is_power_of_2(x):
    return x > 0 and x & (x - 1) == 0

if __name__ == "__main__":
    main(sys.argv[1:])
