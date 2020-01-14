"""Utility for wavefront CLI."""


def option_to_dict(options):
    """Convert user input options into dictionary."""
    new_opts = {}

    for opt in options:
        if "=" in opt:
            splt_opt = opt.split("=")
            new_opts[splt_opt[0]] = splt_opt[1]
        else:
            new_opts[opt] = True

    return new_opts


def cskv_to_dict(option):
    """Convert kwargs into dictionary."""
    opts = {}

    option_list = option.split(',')

    for opt in option_list:
        # skip items that aren't kvs
        if len(opt.split('=')) != 2:
            continue
        key = opt.split('=')[0]
        value = opt.split('=')[1]
        opts[key] = value

    return opts
