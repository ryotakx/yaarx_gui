parameter_dict = {
    'xdp-add': ['da', 'db', 'dc'],
    'max-xdp-add': ['da', 'db'],
    'adp-xor': ['da', 'db', 'dc'],
    'max-adp-xor': ['da', 'db'],
    'adp-lsh': ['r', 'da', 'db'],
    'adp-rsh': ['r', 'da', 'db'],
    'adp-xor-fi': ['a', 'db', 'dc'],
    'max-adp-xor-fi': ['a', 'db'],
    'adp-xor3': ['da', 'db', 'dc', 'dd'],
    'max-adp-xor3': ['da', 'db', 'dc'],
    'eadp-tea-f': ['dx', 'dy'],
    'max-eadp-tea-f': ['dx'],
}

description = {
    'xdp-add': 'The XOR differential probability (XDP) of modular addition.',
    'max-xdp-add': 'The maximum XOR differential probability of modular addition.',
    'adp-xor': 'The modular addition differential probability (ADP) of XOR.',
    'max-adp-xor': 'The maximum modular addition differential probability of XOR.',
    'adp-lsh': 'The modular addition differential probability of left shift (LSH).',
    'adp-rsh': 'The modular addition differential probability of right shift (RSH).',
    'adp-xor-fi': 'The modular addition differential probability of XOR with one fixed input. ',
    'max-adp-xor-fi': 'The maximum modular addition differential probability of XOR with one fixed input.',
    'adp-xor3': 'The modular addition differential probability of XOR with three inputs.',
    'max-adp-xor3': 'The maximum modular addition differential probability of XOR with three inputs:',
    'eadp-tea-f': 'The expected additive DP (EADP) of the F-function of TEA, averaged over all round keys and constants.',
    'max-eadp-tea-f': 'The maximum expected additive DP (EADP) of the F-function of TEA, averaged over all round keys and constants.',
}

choice_list = list(parameter_dict.keys())  # adjust the order of options

input_types = ['hex', 'decimal', 'binary']