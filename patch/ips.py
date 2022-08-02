from memory.space import Reserve

class IPS():
    def __init__(self, filename, allow_conflict = False):
        self.filename = filename
        [regular_hunks, rle_hunks] = IPS._read_file(filename)
        self.allow_conflict = allow_conflict
        self.write_regular_hunks(regular_hunks)
        self.write_rle_hunks(rle_hunks)

    def _read_file(filename):
        ''' ref http://fileformats.archiveteam.org/wiki/IPS_(binary_patch_format)'''

        regular_hunks = []
        rle_hunks = []

        with open(filename, "rb") as file:
            # An IPS file starts with the magic number "PATCH" (50 41 54 43 48)...
            header = file.read(5)
            if(header != b'PATCH'):
                raise ValueError(f"Incorrect magic number at start of IPS: {header}")

            #... Followed by a series of hunks and an end-of-file marker "EOF" (45 4f 46)
            # Regular hunks consist of a three-byte offset followed by a two-byte length of the payload and the payload itself.
            offset_bytes = file.read(3)
            while(offset_bytes != b'EOF'): # TODO: is more error handling needed to handle improperly formated IPS files?
                offset = int.from_bytes(offset_bytes, 'big', signed=False)
                length_bytes = file.read(2)
                length = int.from_bytes(length_bytes, 'big', signed=False)
                if(length != 0):
                    # Regular hunk
                    data = file.read(length)
                    regular_hunks.append([offset, data]) # TODO: use a class to store these
                else:
                    # RLE hunks have their length field set to zero; in place of a payload there is a two-byte length of the run followed by a single byte indicating the value to be written.
                    hunk_length_bytes = file.read(2)
                    hunk_length = int.from_bytes(hunk_length_bytes, 'big', signed=False)
                    hunk_byte = file.read(1)
                    rle_hunks.append([offset, hunk_length, hunk_byte]) # TODO: use a class to store these

                # get the next one
                offset_bytes = file.read(3)
        print(f"regular hunks: {len(regular_hunks)}, rle_hunks: {len(rle_hunks)}")
        return [regular_hunks, rle_hunks]

    def write_regular_hunks(self, regular_hunks):
        for hunk in regular_hunks:
            offset = hunk[0]
            data = hunk[1]

            space = Reserve(offset, offset+(len(data)-1), f"{self.filename} IPS Hunk", allow_conflict = self.allow_conflict)
            space.write(data)

    def write_rle_hunks(self, rle_hunks):
        for hunk in rle_hunks:
            offset = hunk[0]
            hunk_length = hunk[1]
            hunk_byte = hunk[2]
            last_offset = offset + hunk_length

            space = Reserve(offset, last_offset - 1, f"{self.filename} IPS RLE Hunk", allow_conflict = self.allow_conflict)
            while(offset < last_offset):
                space.write(hunk_byte)
                offset += 1

