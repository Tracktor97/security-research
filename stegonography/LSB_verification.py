'''Used for Pre-validation for LSB steganography capacity'''


def stego_lsb():
    '''This is the main function to run'''
    #  Here we identify the data and file we will use
    #  NOTE: Implement dynamic entry of file data and files
    DEBUG = False
    file_data = "afk.jpg"
    carrier_file = "Data Breach.jpg"
    capacity_verification(file_data, carrier_file, DEBUG)
    embed_lsb(file_data, carrier_file)
    extract_lsb(carrier_file)


def capacity_verification(hidden_data, file, debug):
    '''
    This function determines the capacity of the files we have chosen
    and whether or not we are capable of LSB steganography. If this
    verification succeeds, we can proceed with the program to hiding
    the data within our image.
    '''
    #  Creating two empty arrays to store our bit and byte
    #  representations of the files we have chosen
    array_1 = []
    array_2 = []
    #  Opening the image in raw bits mode as hid_1
    with open(hidden_data, 'rb') as hid_1:
        #  For each value produced, we will convert to bits and store
        #  the corresponding string in variable "k" to be appended to the
        #  array.
        for b in hid_1.read():
            k = f'{b:08b}'
            for x in str(k):
                array_1.append(x)
    #  Here we open the second file in raw bits mode as the variable img.
    #  We then use a for loop to iterate through the bytes and add them
    #  to the second array for capacity comparison.
    with open(file, 'rb') as img:
        for b in img.read():
            array_2.append(str(b))
    #  Storing the lengths of arrays and difference in capacity
    if debug:
        print(array_1)
        print(array_2)
    num_bits = len(array_1)
    bit_capacity = len(array_2)
    diff = bit_capacity-num_bits
    print(f'The number of bytes in this file:  {bit_capacity}')
    print(f'The number of bits in the file to hide: {num_bits}')
    print(f'Capacity difference: {diff}')
    #  Condition to verify if capacity is exceeded or not
    if diff > 0:
        print('Carrier image has sufficient capacity for LSB embedding.')
    else:
        #  If capacity is exceeded, present the number of bits which
        #  would need to be trimmed off to succeed
        print(f'Hidden file exceeds capacity by {abs(diff)} bits.')
        print('The hid_1 file cannot be steganographically hidden '
              'within the img file requested.')


def embed_lsb(hidden_data, file):
    '''
    This function will be used to store the embed logic for LSB
    implementation.
    '''
    pass


def extract_lsb(lsb_file):
    '''
    This function will be used to extract the LSB data previously
    embedded.
    '''
    pass


if __name__ == "__main__":
    stego_lsb()
