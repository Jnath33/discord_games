import asyncio


def timeout(msg, check_func, timeout=45, *args):
    on_click = msg.create_click_listener(timeout=timeout)

    out = [None]

    end = asyncio.Event()

    @on_click.no_checks()
    def click(inter):
        if check_func(inter):
            end.set()
            out[0] = inter
            await inter.reply(content="t", type=6)

    @on_click.timeout()
    def time_out():
        end.set()

    await end.wait()

    return out[0]
