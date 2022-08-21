from memory.space import BANK_SIZE, Free

spaces = [

]

def free():
    for space in spaces:
        Free(space[0], space[1])

    # expanded rom free space
    for bank in range(0x30, 0x40):
        start = bank * BANK_SIZE
        end = start + BANK_SIZE - 1
        Free(start, end)
