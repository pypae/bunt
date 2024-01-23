from bunt.constants import SHUFFLE_PERMUTATION, REVERSE_PERMUTATION


def _shuffle_bits(number: int, permutation: list[int]) -> int:
    # Convert the number to a string of bits
    bits_str = f"{number:028b}"

    # Apply the permutation and join the shuffled bits
    shuffled_bits_str = ''.join(bits_str[i] for i in permutation)

    # Convert the shuffled bits back to an integer
    shuffled_number = int(shuffled_bits_str, 2)

    return shuffled_number


def _shuffle(number: int) -> int:
    return _shuffle_bits(number, SHUFFLE_PERMUTATION)


def _unshuffle(number: int) -> int:
    return _shuffle_bits(number, REVERSE_PERMUTATION)


def _compute_crc(data: int, polynomial: int) -> int:
    """Compute the CRC value for given data using the specified polynomial.
    See https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Computation for details.
    """
    polynomial_degree = polynomial.bit_length() - 1
    while data.bit_length() > polynomial_degree:
        # Find the most significant bit in the data.
        shift = data.bit_length() - polynomial.bit_length()
        # XOR the polynomial with the data shifted to align with the polynomial.
        data ^= polynomial << shift

    return data


def generate_crc(data: int, polynomial: int) -> int:
    """Generate a CRC for the given data using the specified polynomial."""
    polynomial_degree = polynomial.bit_length() - 1
    data <<= polynomial_degree  # Pad data with zeros.
    return _compute_crc(data, polynomial) & (
        (1 << polynomial_degree) - 1
    )  # Mask the CRC value.


def sign(data: int, polynomial: int = 0b1011, shuffle: bool = True) -> int:
    """Generate a signature for the given message using the specified polynomial."""
    crc = generate_crc(data, polynomial)
    data = (data << polynomial.bit_length() - 1) | crc
    if shuffle:
        data = _shuffle(data)
    return data


def verify(received_data: int, polynomial: int = 0b1011) -> bool:
    """Check if the received data has a correct CRC."""
    return _compute_crc(received_data, polynomial) == 0


def get_message(received_data: int, polynomial: int = 0b1011, shuffle: bool = True) -> int:
    """Verify the recieved data and get the original message without the CRC."""
    if shuffle:
        received_data = _unshuffle(received_data)
    polynomial_degree = polynomial.bit_length() - 1
    if not verify(received_data, polynomial):
        raise ValueError("The received data is not valid.")
    data = received_data >> polynomial_degree
    return data


if __name__ == "__main__":
    # Example usage.
    # Test-data from https://github.com/boonepeter/boonepeter.github.io-code/blob/main/spotify-codes-part-2/src/crc.py

    polynomial = 0b100000111  # Example polynomial
    original_data = 0b0010001011110111100011110110101100001101  # Example data

    # Generate CRC for the original data
    crc = generate_crc(original_data, polynomial)
    print(f"CRC for original data: {crc:b}")

    check = 0b11001100
    assert crc == check

    # Combine the original data with its CRC
    transmitted_data = (original_data << polynomial.bit_length() - 1) | crc
    print(f"Transmitted data: {transmitted_data:b}")

    # Check the CRC of the received (transmitted) data
    is_valid = verify(transmitted_data, polynomial)
    print(f"Is the received data valid? {'Yes' if is_valid else 'No'}")
