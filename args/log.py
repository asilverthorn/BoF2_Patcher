import args

def _log_tab(tab_name, left_groups, right_groups):
    lcolumn = []
    for lgroup in left_groups:
        lcolumn.append("")
        lcolumn.extend(args.group_modules[lgroup].log(args))

    rcolumn = []
    for rgroup in right_groups:
        rcolumn.append("")
        rcolumn.extend(args.group_modules[rgroup].log(args))

    import log
    log.section(tab_name, lcolumn, rcolumn)

def log():
    pass