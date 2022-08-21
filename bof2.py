def main():
    import args
    import log
    from data.structures import DataArray


    from memory.memory import Memory
    memory = Memory()

    # Apply the retranslation patch
    from patch.ips import IPS
    ips = IPS("patch/bof2v1.2b/Breath of Fire 2 Retranslation (v1.2b).ips")

    # overwrite the IPS patch's first time check
    from memory.space import Reserve, Space
    import instruction.asm as asm
    Reserve(0x0fac0, 0x0facb, "First time check logic", asm.NOP(), allow_conflict = True)

    # Apply the Maeson patches
    ips = IPS("patch/BoFII Maeson 1.02a 2021/Retranslation/Breath of Fire II Maeson Retrans  A 1-02.ips", allow_conflict=True)
    ips = IPS("patch/BoFII Maeson 1.02a 2021/Retranslation/Retranslation Menu Simple Background/1 - BoF II Blue Background.ips", allow_conflict=True)

    # c55a60 - c55b95 is a table with 2 bytes per non-overworld area. If the first byte is 00 - 04, that specifies the encounter rate (dancing monster in menu).
    # If the first byte is 9#, that indicates that it's a conditional battle, such that it also checks a memory address using the lower nybble as an offset
    # Known offsets:
    # 4 = Mt. Futabi (conditional enc - at most 16)
    # A = Forest north of Collosea
    # C = Mt. Rocco Cave Entrance (no enc)
    # E, 10 = Mt. Rocco Cave (enc)
    # 20 = Witch Twr 1 (no enc)
    # 22 = Witch Twr 2
    ENC_TABLE_START = 0x055a60
    ENC_TABLE_END = 0x055b95
    ENC_TABLE_SIZE = 2
    enc_table_data = DataArray(Space.rom, ENC_TABLE_START, ENC_TABLE_END, ENC_TABLE_SIZE)

    for enc in enc_table_data:
        # set every non-zero encounter rate to 0x01 to reduce encounters
        if enc[0] != 0 and enc[0] < 0x90:
            enc[0] = 0x01

    enc_table_data.write()

    memory.write()

if __name__ == '__main__':
    main()
