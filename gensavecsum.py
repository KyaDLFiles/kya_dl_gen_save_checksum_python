# encoding=utf-8
import os
import struct
import sys
import enum


# "Constants"
class GAME_VER(enum.Enum):
    FINAL = 1
    MAY12 = 2
MAX_BLOCKS = 4
UINT64_MAX = 0xFFFFFFFFFFFFFFFF
UINT32_MAX = 0xFFFFFFFF
UINT8_MAX = 0xFF
INT32_MAX = 0x7FFFFFFFF
CRC32_TABLE = [0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f,
               0xe963a535, 0x9e6495a3, 0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988,
               0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91, 0x1db71064, 0x6ab020f2,
               0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
               0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9,
               0xfa0f3d63, 0x8d080df5, 0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172,
               0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b, 0x35b5a8fa, 0x42b2986c,
               0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
               0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423,
               0xcfba9599, 0xb8bda50f, 0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924,
               0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d, 0x76dc4190, 0x01db7106,
               0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
               0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d,
               0x91646c97, 0xe6635c01, 0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e,
               0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457, 0x65b0d9c6, 0x12b7e950,
               0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
               0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7,
               0xa4d1c46d, 0xd3d6f4fb, 0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0,
               0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9, 0x5005713c, 0x270241aa,
               0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
               0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81,
               0xb7bd5c3b, 0xc0ba6cad, 0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a,
               0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683, 0xe3630b12, 0x94643b84,
               0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
               0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb,
               0x196c3671, 0x6e6b06e7, 0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc,
               0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5, 0xd6d6a3e8, 0xa1d1937e,
               0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
               0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55,
               0x316e8eef, 0x4669be79, 0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236,
               0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f, 0xc5ba3bbe, 0xb2bd0b28,
               0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
               0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f,
               0x72076785, 0x05005713, 0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38,
               0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21, 0x86d3d2d4, 0xf1d4e242,
               0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
               0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69,
               0x616bffd3, 0x166ccf45, 0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2,
               0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db, 0xaed16a4a, 0xd9d65adc,
               0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
               0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693,
               0x54de5729, 0x23d967bf, 0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94,
               0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d]


def compute_checksum(buf):
    size = len(buf)
    result = UINT64_MAX if size == 0 else UINT32_MAX

    for i in range(size & INT32_MAX):
        # int_var & *INTX_MAX simulates a cast (truncation of upper bytes)
        result = (result >> 8) ^ (CRC32_TABLE[(result ^ buf[i]) & UINT8_MAX])

    return result


def fix_checksum(fp, verbose=False, game_ver=GAME_VER.FINAL):
    # Elements at index 0 refer to the header
    csums = [0] * (MAX_BLOCKS + 1)
    sizes = [0] * (MAX_BLOCKS + 1)
    blocks = [b''] * (MAX_BLOCKS + 1)

    # Check if NEDE is present at the start of the file
    if fp.read(0x04) != b'\x4e\x45\x44\x45':
        sys.stderr.write("File isn't a KDL save file\n"
                         "Aborting!\n")
        return 3

    # Read header size
    fp.seek(0x08, os.SEEK_SET)
    sizes[0] = struct.unpack("<I", fp.read(4))[0]

    if game_ver == GAME_VER.FINAL:
        # Read first data block size
        fp.seek(4, os.SEEK_CUR)
        sizes[1] = struct.unpack("<I", fp.read(4))[0]

        # Read second data block size
        fp.seek(4, os.SEEK_CUR)
        sizes[2] = struct.unpack("<I", fp.read(4))[0]

        # Exit if file is smaller than reported sizes
        fp.seek(0, os.SEEK_END)
        if fp.tell() < sum(sizes):
            sys.stderr.write("Incorrect data block size(s) in header! Save file may be damaged\n"
                             "Aborting!\n")
            return 4

        # Read both data blocks
        fp.seek(sizes[0], os.SEEK_SET)
        blocks[1] = fp.read(sizes[1])
        blocks[2] = fp.read(sizes[2])

        # Compute checksums of data blocks
        if sizes[1] > 0:
            csums[1] = compute_checksum(blocks[1])
        if sizes[2] > 0:
            csums[2] = compute_checksum(blocks[2])

        # Write checksums to file
        fp.seek(0x0C, os.SEEK_SET)
        fp.write(csums[1].to_bytes(4, byteorder='little'))
        fp.seek(4, os.SEEK_CUR)
        fp.write(csums[2].to_bytes(4, byteorder='little'))
    elif game_ver == GAME_VER.MAY12:
        # Read save file sizes
        for i in range(MAX_BLOCKS):
            fp.seek(0x14 + (0x108 * i), os.SEEK_SET)
            sizes[i + 1] = struct.unpack("<I", fp.read(4))[0]

        # Exit if file is smaller 0x20530
        fp.seek(0, os.SEEK_END)
        if fp.tell() < 0x20530:
            sys.stderr.write("Save file is smaller than expected!\n"
                             "Aborting!\n")
            return 4

        # Read save files, compute checksums, and write them
        fp.seek(sizes[0], os.SEEK_SET)
        for i in range(MAX_BLOCKS):
            if sizes[i + 1] == 0:
                continue
            fp.seek(0x530 + (0x8000 * i), os.SEEK_SET)
            blocks[i + 1] = fp.read(sizes[i + 1])
            csums[i + 1] = compute_checksum(fp.read(sizes[i + 1]))
            fp.seek(0x10 + (0x108 * i), os.SEEK_SET)
            fp.write(csums[i + 1].to_bytes(4, byteorder='little'))

    # Reread header from 0x08, calculate checksum, and write it to file
    fp.seek(0x08, os.SEEK_SET)
    blocks[0] = fp.read(sizes[0] - 0x08)
    csums[0] = compute_checksum(fp.read(sizes[0] - 0x08))
    fp.seek(0x04, os.SEEK_SET)
    fp.write(csums[0].to_bytes(4, byteorder='little'))

    if verbose:
        # Tfw no f strings to support legacy OSes
        # And yes, I know this code sucks rn... but too lazy to fix
        if game_ver == GAME_VER.FINAL:
            print("Header size: h%X\n"
                  "First data block size: h%X\n"
                  "Second data block size: h%X\n\n"
                  "Header checksum: h%08X\n"
                  "First data block checksum: h%08X\n"
                  "Second data block checksum: h%08X\n\n"
                  "Keep in mind they're stored as little endian in the file!"
                  % (sizes[0], sizes[1], sizes[2], csums[0], csums[1], csums[2]))
        elif game_ver == GAME_VER.MAY12:
            print("Header size: h%X\n"
                  "First save file size: h%X\n"
                  "Second save file size: h%X\n"
                  "Third save file size: h%X\n"
                  "Fourth save file size: h%X\n\n"
                  "Header checksum: h%08X\n"
                  "First save file checksum: h%08X\n"
                  "Second save file checksum: h%08X\n"
                  "Third save file checksum: h%08X\n"
                  "Fourth save file checksum: h%08X\n\n"
                  "Keep in mind they're stored as little endian in the file!"
                  % (sizes[0], sizes[1], sizes[2], sizes[3], sizes[4], csums[0], csums[1], csums[2], csums[3], csums[4]))


def _main():
    # Initialize variables and defaults
    argc = len(sys.argv)
    verbose = False
    game_ver = GAME_VER.FINAL

    # Read and check arguments
    if argc < 2:
        sys.stderr.write("Missing argument!\n"
                         "Usage: gensavecsum.py /path/to/save/file.dat <--verbose> <--game_ver=[game version]>\n"
                         "Game versions:\n"
                         "- final (also applies to September 29 prototype) (default)\n"
                         "- may12\n\n")
        return 2
    elif argc > 2:
        for i in sys.argv[2:]:
            i = i.lower()
            if i == "--verbose":
                verbose = True
            elif i[:11] == "--game_ver=" and i[11:] == "may12":
                game_ver = GAME_VER.MAY12
            elif i[:11] == "--game_ver=" and i[11:] == "final":
                game_ver = GAME_VER.FINAL
            else:
                sys.stderr.write("Unknown argument(s)!\n")
                return 5
    try:
        with open(sys.argv[1], "rb+") as fp:
            return fix_checksum(fp, verbose, game_ver)
    except EnvironmentError as e:
        sys.stderr.write("Error opening file!\n" + str(e) + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(_main())
