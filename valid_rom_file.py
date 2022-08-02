FILE_SIZE = 3145728

HEADER_SIZE = 0x200
HEADER_FILE_SIZE = FILE_SIZE + HEADER_SIZE

def get_sha256_hex(file_path):
    import hashlib
    BUFFER_SIZE = 65536

    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as rom_file:
        data = rom_file.read(BUFFER_SIZE)
        while data:
            sha256.update(data)
            data = rom_file.read(BUFFER_SIZE)

    return sha256.hexdigest()

def valid_rom_file(file_path):
    expected_sha256 = "fede9d4aec8c35ed11e2868c3c517bce53ee3e6af724085c92500e99e43e63de"
    sha256 = get_sha256_hex(file_path)
    print(sha256)
    return sha256 == expected_sha256
