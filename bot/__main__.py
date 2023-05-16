import sys

from .porch.run import run as porch_bot

if __name__ == '__main__':
    bot = sys.argv[1]

    if bot == 'porch':
        run = porch_bot
    else:
        raise NotImplementedError(
            "Invalid bot. \"%s\" doesn't exists." % bot
        )

    kwargs = {}

    for kwarg in sys.argv[2:]:
        try:
            k, v = kwarg.split('=')
            kwargs[k] = v
        except ValueError:
            continue

    print('Running bot "%s" with arguments "%s"' % (bot, kwargs))
    run(**kwargs)
