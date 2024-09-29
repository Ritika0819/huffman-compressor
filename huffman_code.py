import sortedcontainers as sc

# Huffman Encoding Implementation
def letter_distribution(original_string):
    '''
    This function calculates the frequency of each character in the given string.
    It iterates through each character in the string and constructs a dictionary
    where each unique character is a key and its corresponding value is the number
    of times it appears in the string.
    
    Args:
    original_string (str): The input string whose characters' frequencies are to be calculated.
    
    Returns:
    dict: A dictionary where keys are characters and values are their frequencies in the string.
    '''
    letter_occurrence = {}
    for char in original_string:
        if char in letter_occurrence:
            letter_occurrence[char] += 1  # Increment frequency if the character already exists in the dictionary
        else:
            letter_occurrence[char] = 1  # Initialize frequency for the new character
    return letter_occurrence


def node_reducer(letter_occurrence_dictionary):
    '''
    This function builds a Huffman Tree from the letter frequency dictionary. 
    It creates a sorted list where each element is a tuple consisting of the frequency of 
    the character, the character itself, and the node (either a character or a pair of nodes).
    It iteratively reduces the list by merging the two nodes with the smallest frequencies,
    thereby constructing a binary tree structure that represents the Huffman Tree.
    
    Args:
    letter_occurrence_dictionary (dict): A dictionary containing characters and their frequencies.
    
    Returns:
    list: A nested list structure representing the Huffman Tree. 
          Each node is either a character or a list of two child nodes.
    '''
    node_list = sc.SortedList()
    for char in letter_occurrence_dictionary:
        # Each node is a tuple with (frequency, character, node_structure)
        node_list.add((letter_occurrence_dictionary[char], char, char))
    
    while len(node_list) > 1:
        # Get the two smallest nodes
        a = node_list[0]
        b = node_list[1]
        # Remove them from the list
        node_list.pop(0)
        node_list.pop(0)
        # Merge them into a new node and add back to the list
        node_list.add((a[0] + b[0], a[1], [a[2], b[2]]))
    
    # The last remaining element in the list is the root of the Huffman Tree
    return node_list[0][2]


global code_dict
code_dict = {}

def code_assigner(nested_list, index):
    '''
    This recursive function traverses the Huffman Tree (represented as a nested list)
    and assigns binary codes to each character. The traversal is done in a depth-first manner.
    For every left child, a '0' is appended to the code, and for every right child, a '1' is appended.
    If the node is a leaf (i.e., a character), the current code is assigned to the character.

    Args:
    nested_list (list): The nested list representing the Huffman Tree.
    index (str): A string representing the current Huffman code as the function traverses the tree.
    
    Returns:
    dict: A dictionary where each key is a character, and the corresponding value is its Huffman code.
    '''
    if len(nested_list) == 1:
        # Base case: If the node contains only one character, assign '1' to it
        return {nested_list[0]: '1'}
    else:
        # If the left child is a list (i.e., not a leaf), recursively assign codes to its children
        if type(nested_list[0]) == list:
            code_assigner(nested_list[0], index + '0')
        else:
            # Assign the current code to the left child (which is a character)
            code_dict[nested_list[0]] = index + '0'

        # If the right child is a list, recursively assign codes to its children
        if type(nested_list[1]) == list:
            code_assigner(nested_list[1], index + '1')
        else:
            # Assign the current code to the right child (which is a character)
            code_dict[nested_list[1]] = index + '1'

        # Return the dictionary containing character-to-Huffman code mappings
        return code_dict


def huffman_code(original_string):
    '''
    This function generates the Huffman codes for each character in the input string.
    It first calculates the frequency of each character using `letter_distribution`,
    builds the Huffman Tree using `node_reducer`, and finally assigns binary codes to each character
    using the `code_assigner` function.
    
    Args:
    original_string (str): The input string for which the Huffman codes are generated.
    
    Returns:
    dict: A dictionary containing the Huffman codes for each character in the input string.
    '''
    letter_occurrence_dictionary = letter_distribution(original_string)
    node_reduced_list = node_reducer(letter_occurrence_dictionary)
    index = ""
    return code_assigner(node_reduced_list, index)


def huffman_encoding(original_string):
    '''
    This function encodes the input string using Huffman codes.
    It generates the Huffman code for each character and concatenates the codes
    to form the final encoded binary string.
    
    Args:
    original_string (str): The string to be encoded.
    
    Returns:
    str: A binary string representing the Huffman-encoded version of the input string.
    '''
    encoded_string = ""
    char_code = huffman_code(original_string)
    for char in original_string:
        # Convert each character in the string to its corresponding Huffman code
        encoded_string += char_code[char]
    return encoded_string


def bits_without_encoding(original_string):
    '''
    This function calculates the number of bits required to store the original string
    without any compression. Since each character is typically stored as an 8-bit ASCII code,
    the total bit count is the number of characters multiplied by 8.
    
    Args:
    original_string (str): The input string for which the bit count is calculated.
    
    Returns:
    str: The total number of bits required to store the original string, expressed as a string.
    '''
    return f"{len(original_string) * 8} bits"


def bits_after_encoding(original_string):
    '''
    This function calculates the total number of bits required to store the string after Huffman encoding.
    It considers the bits needed to store the Huffman tree structure and the encoded binary string.
    
    Args:
    original_string (str): The input string that has been Huffman encoded.
    
    Returns:
    str: The total number of bits required to store the Huffman-encoded string, expressed as a string.
    '''
    count = 0
    for char in huffman_code(original_string):
        count += len(huffman_code(original_string)[char])  # Sum the length of each character's Huffman code
    return f"{len(huffman_code(original_string)) * 8 + count + len(huffman_encoding(original_string))} bits"


# Huffman Decoding Implementation
def huffman_decoding(encoded_string, code_dict):
    '''
    This function decodes a Huffman-encoded string back to the original string using the provided Huffman codes.
    It first reverses the Huffman code dictionary (where keys are codes and values are characters),
    then iterates through the encoded binary string, checking if the current code matches any in the reversed dictionary.
    Once a match is found, the corresponding character is added to the decoded string.
    
    Args:
    encoded_string (str): The binary string that was encoded using Huffman codes.
    code_dict (dict): A dictionary of Huffman codes where keys are characters and values are binary codes.
    
    Returns:
    str: The decoded string, which should match the original input string.
    '''
    # Reverse the Huffman code dictionary to map binary codes to characters
    reverse_code_dict = {v: k for k, v in code_dict.items()}
    
    decoded_string = ""
    current_code = ""
    
    # Iterate through the encoded string, building the Huffman code and checking if it exists in the dictionary
    for bit in encoded_string:
        current_code += bit  # Build the current Huffman code bit by bit
        if current_code in reverse_code_dict:
            # If the code matches one in the dictionary, add the corresponding character to the decoded string
            decoded_string += reverse_code_dict[current_code]
            current_code = ""  # Reset the current code to start building the next code
    
    return decoded_string


# Test Example
if __name__ == "__main__":
    # Example string to be encoded and decoded
    original_string = "this is an example for huffman encoding"

    # Perform Huffman Encoding
    print("Original String:", original_string)
    encoded_string = huffman_encoding(original_string)
    print("Encoded String:", encoded_string)

    # Show the Huffman Codes for each character
    huff_codes = huffman_code(original_string)
    print("Huffman Codes:", huff_codes)

    # Calculate the size before and after encoding
    print("Bits without Encoding:", bits_without_encoding(original_string))
    print("Bits after Encoding:", bits_after_encoding(original_string))

    # Perform Huffman Decoding
    decoded_string = huffman_decoding(encoded_string, huff_codes)
    print("Decoded String:", decoded_string)
