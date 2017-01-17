

def option_to_dict(options):

    new_opts = {}

    for opt in options:
        if "=" in opt:
            splt_opt = opt.split("=")
            new_opts[splt_opt[0]] = splt_opt[1]
        else:
            new_opts[opt] = True

    return new_opts

def cskv_to_dict(option):

    opts = {}

    list = option.split(',')

    for opt in list:
        #skip items that aren't kvs
        if len(opt.split('=')) != 2:
            continue
        else:
            k = opt.split('=')[0]
            v = opt.split('=')[1]
            opts[k] = v

    return opts
