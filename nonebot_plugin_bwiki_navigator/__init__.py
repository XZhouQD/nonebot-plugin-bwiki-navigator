from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

cmd_str = config.bwiki_navigator_command if config.bwiki_navigator_command else 'bwiki'
cmd_alias = config.bwiki_navigator_command_alias if config.bwiki_navigator_command_alias else set()
default_start = list(global_config.command_start)[0]

__plugin_meta__ = PluginMetadata(
    name='Bwiki Navigator',
    description='Bwiki助手（官方移植版）',
    usage=f'''欢迎使用Bwiki助手移植版，召唤方法如下：
{default_start}{cmd_str} bwiki子站域名 页面名(可选)
例如：{default_start}{cmd_str} clover 凯瑟琳
{default_start}{cmd_str} clover''',
    type='application',
    homepage='https://github.com/xzhouqd/nonebot-plugin-bwiki-navigator',
    extra={'version': '0.2.0'}
)

from .handler import bwiki
