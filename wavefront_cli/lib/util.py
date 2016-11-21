

def options_to_dict(options):

    new_opts = {}

    for opt in options:
        if "=" in opt:
            splt_opt = opt.split("=")
            new_opts[splt_opt[0]] = splt_opt[1]
        else:
            new_opts[opt] = True

    return new_opts