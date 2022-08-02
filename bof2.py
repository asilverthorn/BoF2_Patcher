def main():
    import args
    import log

    from memory.memory import Memory
    memory = Memory()

    from patch.ips import IPS
    ips = IPS("patch/bof2v1.2b/Breath of Fire 2 Retranslation (v1.2b).ips")

    # overwrite the IPS patches first time check
    from memory.space import Reserve
    import instruction.asm as asm
    Reserve(0x0fac0, 0x0facb, "First time check logic", asm.NOP(), allow_conflict = True)

    ips = IPS("patch/BoFII Maeson 1.02a 2021/Retranslation/Breath of Fire II Maeson Retrans  A 1-02.ips", allow_conflict=True)
    ips = IPS("patch/BoFII Maeson 1.02a 2021/Retranslation/Retranslation Menu Simple Background/1 - BoF II Blue Background.ips", allow_conflict=True)

    memory.write()

if __name__ == '__main__':
    main()
