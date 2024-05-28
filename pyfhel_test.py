from Pyfhel import Pyfhel
import numpy as np

he = Pyfhel()
ckks_params = {
    'scheme': 'CKKS',   # can also be 'ckks'
    'n': 2**14,         # Polynomial modulus degree. For CKKS, n/2 values can be
                        #  encoded in a single ciphertext.
                        #  Typ. 2^D for D in [10, 15]
    'scale': 2**30,     # All the encodings will use it for float->fixed point
                        #  conversion: x_fix = round(x_float * scale)
                        #  You can use this as default scale or use a different
                        #  scale on each operation (set in HE.encryptFrac)
    'qi_sizes': [60, 30, 30, 30, 60] # Number of bits of each prime in the chain.
                        # Intermediate values should be  close to log2(scale)
                        # for each operation, to have small rounding errors.
}
he.contextGen(**ckks_params)  # Generate context for ckks scheme
he.keyGen()             # Key Generation: generates a pair of public/secret keys

value1 = he.encryptFrac(np.array([10], dtype=np.float64))
value2 = he.encryptFrac(np.array([34], dtype=np.float64))
value3 = he.encryptFrac(np.array([56], dtype=np.float64))
value4 = he.encryptFrac(np.array([1/3],dtype=np.float64))

result = (value1 + value2 + value3) * value4

# Não permite divisão
# result = result / 3

print(list(he.decryptFrac(result))[0])
