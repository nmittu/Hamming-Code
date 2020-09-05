from typing import List, Optional
from functools import reduce
import operator as op
import random

def hamming_dec(bits: List[bool]) -> Optional[List[bool]]:
    pos = reduce(op.xor, [i for i, x in enumerate(bits) if x])
    parity = reduce(op.add, [1 for x in bits if x]) % 2

    if pos != 0 and parity == 0:
        return None # Multiple bits changed
    else:
        bits[pos] = not bits[pos]
        return [bool(x) for i, x in enumerate(bits) if i > 0 and (i & (i-1) != 0)]

def hamming_enc(bits: List[bool]) -> List[bool]:
    bits = bits[:]

    bits.insert(0, False)

    i = 0
    while 2**i < len(bits):
        bits.insert(2**i, False)
        i+=1
    
    parities = reduce(op.xor, [i for i, x in enumerate(bits) if x])

    i = 0
    while 2**i <= parities:
        if parities & (1 << i):
            bits[2**i] = not bits[2**i]
        i+=1

    parity = reduce(op.add, [1 for x in bits if x]) % 2
    if parity != 0:
        bits[0] = not bits[0]

    return bits
    


# Tests
if __name__ == "__main__":
    # No Change
    for _ in range(10):
        bits = [bool(random.getrandbits(1)) for _ in range(11)]
        assert bits == hamming_dec(hamming_enc(bits))

    # One change
    for _ in range(10):
        bits = [bool(random.getrandbits(1)) for _ in range(11)]
        enc = hamming_enc(bits)
        i = random.randint(0, len(enc) -1) 
        enc[i] = not enc[i]
        assert bits == hamming_dec(enc)

    # Two changes
    for _ in range(10):
        bits = [bool(random.getrandbits(1)) for _ in range(11)]
        enc = hamming_enc(bits)
        idxs = random.sample(range(len(enc)), 2)
        for i in idxs:
            enc[i] = not enc[i]
        assert hamming_dec(enc) is None
