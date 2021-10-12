import asyncio


async def new_menu(msg, menu, timeout=None, functions=None, member=None):

    if functions is None:
        functions = {}

    await msg.edit(content=msg.content, components=menu[0])

    if timeout is not None:
        on_click = msg.create_click_listener(timeout=timeout)
    else:
        on_click = msg.create_click_listener()

    info = [0, None]

    end = asyncio.Event()

    @on_click.no_checks()
    async def click(inter):
        if inter.message.id == msg.id and (member is None or inter.author.id in member.id):
            if inter.clicked_button.custom_id == "<":
                info[0] += -1
                await msg.edit(content=msg.content, components=menu[info[0]])
            elif inter.clicked_button.custom_id == ">":
                info[0] += 1
                await msg.edit(content=msg.content, components=menu[info[0]])
            elif inter.clicked_button.custom_id in functions.keys():
                functions[inter](inter, info)
            else:
                end.set()
                info[1] = inter
            await inter.reply(content="t", type=6)

    if timeout is not None:
        @on_click.timeout()
        async def time_out():
            end.set()

    await end.wait()
    if timeout is None:
        on_click.kill()

    return info[1]
