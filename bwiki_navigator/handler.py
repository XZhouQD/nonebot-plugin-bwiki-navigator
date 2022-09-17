import re
from typing import Dict

import httpx
from nonebot import on_command, get_driver
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg

from . import cmd_str, cmd_alias, default_start
from .parser import SimpleInnerParser

bwiki = on_command(cmd_str, priority=1, aliases=cmd_alias)
bwiki.__help_name__ = cmd_str
bwiki.__help_info__ = f'''{default_start}{cmd_str} bwiki子站域名 页面名(可选)
例如：{default_start}{cmd_str} clover 凯瑟琳
{default_start}{cmd_str} clover'''


@bwiki.handle()
async def handle_first_receive(event: Event, matcher: Matcher, args: Message = CommandArg()):
    if args:
        matcher.set_arg("content", args)
    else:
        await matcher.finish(Message(MessageSegment.at(event.get_user_id()) + bwiki.__help_info__))


@bwiki.got("content")
async def get_result(event: Event, matcher: Matcher, content: Message = Arg()):
    at = MessageSegment.at(event.get_user_id())
    args = content.extract_plain_text().strip().split()[:2]
    if not args:
        await matcher.finish(Message(at + bwiki.__help_info__))
    site, sitename = await parse_sitename(args, at, matcher)
    if len(args) == 1:
        await matcher.finish(Message(at + f"{sitename} https://wiki.biligame.com/{site}"))

    page, page_part, result = await parse_page(args, at, matcher, site, sitename)
    if re.match("^(文件|file|File):.*\.(jpg|png|gif|jpeg)$", page):
        await parse_file_page(at, matcher, page, page_part, site)
    img_part, text_part = await parse_wikibot(result)
    await matcher.finish(Message(at + page_part + text_part + img_part))


async def parse_wikibot(result):
    to_feed = result["parse"]["text"]["*"]
    wikibot_parser = SimpleInnerParser("", ("class", "wiki-bot"))
    wikibot_parser.feed(to_feed)
    wikibot_parser.close()
    wikibot = '\n'.join(wikibot_parser.output)
    text_part = MessageSegment.text(wikibot)
    wikibot_img_parser = SimpleInnerParser("img", [("class", "wiki-bot-img"), ("src", None)], False)
    wikibot_img_parser.feed(to_feed)
    wikibot_img_parser.close()
    img_part = [MessageSegment.image(image_url) for image_url in wikibot_img_parser.output]
    return img_part, text_part


async def parse_file_page(at, matcher, page, page_part, site):
    async with httpx.AsyncClient(http2=True,
                                 base_url=f"https://wiki.biligame.com/{site}",
                                 follow_redirects=False) as client:
        response = await client.get("/api.php", params={"action": "parse", "format": "json",
                                                        "disablelimitreport": False, "text": f"[[{page}|link=]]"})
    img_parser = SimpleInnerParser("img", "src", False)
    img_parser.feed(response.json()["parse"]["text"]["*"])
    img_parser.close()
    img_part = MessageSegment.image(img_parser.output[0])
    await matcher.finish(Message(at + page_part + img_part))


async def parse_page(args, at, matcher, site, sitename):
    page = args[1]
    async with httpx.AsyncClient(http2=True,
                                 base_url=f"https://wiki.biligame.com/{site}",
                                 follow_redirects=False) as client:
        response = await client.get("/api.php", params={"action": "parse", "format": "json",
                                                        "disablelimitreport": False, "redirects": True,
                                                        "disableeditsection": True, "page": page})
    if response.status_code != 200:
        await matcher.finish(Message(at + f'解析站点 {site} 页面 {page} 失败'))
    result: Dict = response.json()
    if error := result.get("error", None):
        if error_code := error["code"] == "missingtitle":
            await matcher.finish(Message(at + f'解析站点 {site} 页面 {page} 失败：页面未找到'))
        else:
            await matcher.finish(Message(at + f'解析站点 {site} 页面 {page} 失败：{error_code}'))
    page = result["parse"]["title"]
    page_id = result["parse"]["pageid"]
    page_part = MessageSegment.text(f'{sitename} {page}\nhttps://wiki.biligame.com/{site}/?curid={page_id}\n')
    return page, page_part, result


async def parse_sitename(args, at, matcher):
    if site := args[0]:
        async with httpx.AsyncClient(http2=True,
                                     base_url=f"https://wiki.biligame.com/{site}",
                                     follow_redirects=False) as client:
            response = await client.get("/api.php", params={"action": "parse", "format": "json",
                                                            "disablelimitreport": False, "text": r"{{SITENAME}}"})
            if response.status_code != 200:
                await matcher.finish(Message(at + f'未找到站点 {site}，站点不存在或Bot解析失败'))
    sitename_parser = SimpleInnerParser("p")
    sitename_parser.feed(response.json()["parse"]["text"]["*"])
    sitename_parser.close()
    sitename = sitename_parser.output[0].strip().split('_')[0] if sitename_parser.output else site
    sitename = sitename if sitename else site
    return site, sitename
