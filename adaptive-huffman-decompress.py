import sys
import huffmancoding

def main(args):
    if len(args) != 2:
        sys.exit("Usage: python adaptive-huffman-decompress.py InputFile OutputFile")
    inputfile, outputfile = args
    with open(inputfile, "rb") as inp, open(outputfile, "wb") as out:
        decompress(huffmancoding.BitInputStream(inp), out)

def decompress(bitin, out):
    initfreqs = [1] * 257
    freqs = huffmancoding.FrequencyTable(initfreqs)
    dec = huffmancoding.HuffmanDecoder(bitin)
    dec.codetree = freqs.build_code_tree()
    count = 0
    while True:
        symbol = dec.read()
        if symbol == 256:
            break
        out.write(bytes((symbol,)))
        count += 1
        freqs.increment(symbol)
        if (count < 262144 and is_power_of_2(count)) or count % 262144 == 0:
            dec.codetree = freqs.build_code_tree()
        if count % 262144 == 0:
            freqs = huffmancoding.FrequencyTable(initfreqs)

def is_power_of_2(x):
    return x > 0 and x & (x-1) == 0

if __name__ == "__main__":
    main(sys.argv[1:])
