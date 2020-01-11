"""
Derived From : Piotr Czapla
StackOverflow : https://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
Edited by : Ubaidullah Effendi-Emjedi
LinkedIn :

This is a mediocre File Hashing Program. Feel free to edit it and make it better.

There are 2 main Hash Functions: checksum_black2b and checksum.

1. checksum_blake2b uses the Blake2b hash algorithm.
2. checksum can use MD5, SHA256, SHA3 etc Hashing algorithms by specifying the hash_type parameter.

There are 2 additional Hash Functions: size_cap_checksum_blake2b and size_cap_checksum.

1. size_cap_checksum_blake2b uses the Blake2b hash algorithm.
Files bigger than the size_cap_in_mb will not be processed.

2. size_cap_checksum can use MD5, SHA256, SHA3 etc Hashing algorithms by specifying the hash_type parameter.
Files bigger than the size_cap_in_mb will not be processed.
"""

import os
import hashlib
import json

# Program Files Paths in os.environ
PROGRAMFILES = "PROGRAMFILES"

PROGRAMFILES_X86 = "PROGRAMFILES(X86)"

# Processor Architecture Version
PROCESSOR_ARCHITECTURE = "PROCESSOR_ARCHITECTURE"


def is_64_bit_os():
    """
    Try and Identify if the Operating System is 64bit
    :return: True or False
    """
    try:
        if PROGRAMFILES_X86 in os.environ[PROGRAMFILES]:
            return True
        if os.environ[PROCESSOR_ARCHITECTURE].endswith("64"):
            return True
        return False
    except Exception as exception:
        print(exception)


def get_path_to_all_files(absolute_path = os.getcwd(), ignore_files = []):
    """
    Get valid file paths to all files in the parent folder and all sub directories.
    :param absolute_path: Parent folder
    :return: List of Files paths.
    """
    list_of_files = list()
    for (directory_path, directory_names, filenames) in os.walk(absolute_path):
        list_of_files += [os.path.join(directory_path, file) for file in filenames if file not in ignore_files]
    return list_of_files


def checksum_blake2(file_path, chunk_num_blocks = 128, digest_size = 64):
    """
    Compute the Blake2B or Blake2S Checksum of the give File.
    :param file_path: File to Read
    :param chunk_num_blocks: Chunk Number of Blocks
    :param digest_size: Length of Digest Output.
    :return: Hexadecimal Checksum of the file.
    """

    # Enforce that Digest Size is within the Given Bounds X is an Element of [16, 64].
    if digest_size < 16:
        digest_size = 16
    elif digest_size > 64:
        digest_size = 64

    # Use Blake2B Hash Method
    hash_type = hashlib.blake2b(digest_size = digest_size) if is_64_bit_os() else hashlib.blake2s(
        digest_size = digest_size)
    with open(file_path, "rb") as file:
        # Read and Iterate over the Data a step at a time until an Empty Line is received.
        for chunk in iter(lambda: file.read(chunk_num_blocks * hash_type.block_size), b""):
            hash_type.update(chunk)

    return hash_type.hexdigest()


def size_cap_checksum_blake2(file_path, chunk_num_blocks = 128, digest_size = 64, size_cap_in_mb = 250.0):
    """
    Compute the Blake2B Checksum of the give File.
    :param file_path: File to Read
    :param chunk_num_blocks: Chunk Number of Blocks
    :param digest_size: Length of Digest Output.
    :param size_cap_in_mb: Size Cap of a file in Megabytes that should not be exceeded.
    :return: Hexadecimal Checksum of the file.
    """
    size_in_bytes = os.stat(file_path).st_size
    size_in_megabytes = size_in_bytes / 1024.0 ** 2

    print(f"{os.path.basename(file_path)} = Size in MB {size_in_megabytes}")

    if size_in_megabytes > size_cap_in_mb:
        print(f"The File {os.path.basename(file_path)} is to big to process." \
              f"\nOnly files smaller than {size_cap_in_mb} will be processed!")
    else:
        return checksum_blake2(file_path, chunk_num_blocks, digest_size)


def checksum(file_path, hash_type = hashlib.sha256, chunk_num_blocks = 128):
    """
    Compute a hash Checksum of the given File. Default Hash Method is MD5
    :param file_path: Path of the File.
    :param hash_type: Specify which Hash Algorithm to use (mdf5, sha256, sha3, etc).
    :param chunk_num_blocks:
    :return: Hexadecimal Checksum of the File.
    """
    hash_to_use = None
    hash_to_use = hash_type
    with open(file_path, "rb") as file:
        # Read and Iterate over the Data a step at a time until an Empty Line is received.
        for chunk in iter(lambda: file.read(chunk_num_blocks * hash_to_use.block_size), b""):
            hash_to_use.update(chunk)
    return hash_to_use.hexdigest()


def checksum_sha(file_path, chunk_num_blocks = 128):
    """
    Compute a hash Checksum of the given File. Default Hash Method is MD5
    :param file_path: Path of the File.
    :param chunk_num_blocks:
    :return: Hexadecimal Checksum of the File.
    """
    hash_to_use = hashlib.sha3_512()
    with open(file_path, "rb") as file:
        # Read and Iterate over the Data a step at a time until an Empty Line is received.
        for chunk in iter(lambda: file.read(chunk_num_blocks * hash_to_use.block_size), b""):
            hash_to_use.update(chunk)
    return hash_to_use.hexdigest()


def size_cap_checksum(file_path, hash_type = hashlib.sha256, chunk_num_blocks = 128, size_cap_in_mb = 250):
    """
    Compute the Checksum of the given file smaller than the given size cap in Megabytes. Default Hash Method is MD5
    :param file_path: Path of the File.
    :param hash_type: Specify which Hash Algorithm to use (mdf5, sha256, sha3, etc).
    :param chunk_num_blocks:
    :param size_cap_in_mb: Size Cap of a file in Megabytes that should not be exceeded.
    :return: Hexadecimal Checksum of the File.
    """
    size_in_bytes = os.stat(file_path).st_size
    size_in_megabytes = size_in_bytes / 1024.0 ** 2

    print(f"{os.path.basename(file_path)} = Size in MB {size_in_megabytes}")

    if size_in_megabytes > size_cap_in_mb:
        print(f"The File {os.path.basename(file_path)} is to big to process." \
              f"\nOnly files smaller than {size_cap_in_mb} will be processed!")
    else:
        return checksum(file_path, hash_type, chunk_num_blocks)


def write_checksum_to_json(checksum_data = [], path = os.path.join(os.getcwd())):
    """
    Convert a Checksum List of Data to a JSON File.
    :param checksum_data: List of Checksum data. Each element is a Tuple (file_path, hash_code).
    :param path: Path of the File.
    :return:
    """
    file_name = os.path.basename(path)
    if "checksum" not in file_name.lower():
        path = path.replace(file_name, f"{file_name}-checksum")

    checksum_dictionary = {}
    for file_path, hash_value in checksum_data:
        checksum_dictionary[file_path] = hash_value

    json.dump(checksum_dictionary, open(path, mode = "w"), indent = 4, ensure_ascii = False)


def compare(checksum_data = [], checksum_file_path = os.path.join(os.getcwd()), extension = ".json"):
    """
    Compare the new Computed Hash Values with the Existing Backup to check if any files were altered or newly found.
    :param checksum_data: List of Checksum data. Each element is a Tuple (file_path, hash_code)
    :param checksum_file_path: Path of the Backup Checksum File
    :param extension: The Extension of the Backup File. Default is .json, however, any type can be specified.
    :return:
    """
    path = os.path.join(checksum_file_path, f"checksum{extension}")
    checksum_dictionary = json.load(open(path, mode = "r"))

    for file_path, hash in checksum_data:
        if file_path in checksum_dictionary.keys():
            file_name = os.path.basename(file_path)
            if hash.lower() == checksum_dictionary[file_path].lower():
                print(f"[Match]\n{file_path}\n{file_name} : {hash} \n")
            else:
                print(f"[This is an altered File!]\n{file_path}\n{file_name} : {hash} \n")
        else:
            print(f"[This is a new File!]\n{file_path}\n{file_name} : {hash} \n")


def stringify_checksum_data_array(checksum_data = []):
    string_checksum_data = ""

    for file_path, hash_value in checksum_data:
        if hash_value != None:
            string_checksum_data += f"{os.path.basename(file_path)} : {hash_value}\n"
        else:
            continue

    return string_checksum_data


def stringify_checksum_data_dictionary(checksum_data = {}):
    string_checksum_data = ""
    for key, value in checksum_data.items():
        if value != None:
            string_checksum_data += f"{os.path.basename(key)} : {value}\n"
        else:
            continue

    return string_checksum_data


def checksum_data_dict_to_array(checksum_data = {}):
    checksum_data_array = []
    for key, value in checksum_data.items():
        if value != None:
            checksum_data_array.append((key, value))
        else:
            continue
    return checksum_data_array


if __name__ == "__main__":
    # Pretty Print Lambda
    pretty_print = lambda array: print(*array, sep = "\n")

    from timeit import default_timer as timer

    start = timer()

    # Get Paths to all the Files in the Folder and Sub Folders.
    paths = get_path_to_all_files()

    # Print the file Paths.
    # print("File Paths:")
    # pretty_print(paths)
    print()

    # Calculate the Checksum
    hashed_data = [(path, checksum_sha(path)) for path in paths]

    # Pretty Print the Checksum
    print("Blake2b Checksum:")
    pretty_print(hashed_data)
    print()

    hashed_data = [(path, checksum_sha(path)) for path in paths]

    print("Blake2b Checksum:")
    pretty_print(hashed_data)
    print()
    # Write the Data to a file.
    # write_checksum_to_json(hashed_data_blake2b)

    # Compare Check.
    # compare(hashed_data_blake2b)
    #
    # print(is_64_bit_os())

    end = timer()
    print(end - start)  # Time in seconds, e.g. 5.38091952400282

    os.system("pause")
