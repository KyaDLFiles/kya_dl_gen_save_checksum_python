import gensavecsum

if __name__ == "__main__":
    tested = 0
    errors = 0
    with open("tests/test_file.dat", "rb") as fp_test:
        with open("tests/checksums.txt", "r") as fp_csums:
            buf = fp_test.read()
            for i in range(len(buf)):
                for j in range(len(buf) - i):
                    csum = "%08X" % (gensavecsum.compute_checksum(buf[i:j + i]) & 0xFFFFFFFF)
                    correct = fp_csums.readline().split(";")[1].rstrip()
                    tested += 1
                    if csum != correct:
                        print("WRONG CHECKSUM AT h%08X:h%08X!!" % (i, j + i))
                        errors += 1
    print("Tested %d checksums with %d mismatch(es)" % (tested, errors))
