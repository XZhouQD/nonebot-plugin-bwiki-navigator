<div align="center">

# nonebot-plugin-bwiki-navigator
### BWiki助手Nonebot2插件移植版

<a href="https://raw.githubusercontent.com/xzhouqd/nonebot-plugin-bwiki-navigator/main/LICENSE">
    <img src="https://img.shields.io/github/license/xzhouqd/nonebot-plugin-help?style=for-the-badge" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-bwiki-navigator">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-bwiki-navigator?color=green&style=for-the-badge" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-^3.8-blue?style=for-the-badge" alt="python">
<br />
<img src="https://img.shields.io/badge/tested_python-3.10.4-blue?style=for-the-badge" alt="python">
<img src="https://img.shields.io/static/v1?label=tested+env&message=go-cqhttp+1.0.0&color=blue&style=for-the-badge" alt="python">
<br />
<a href="https://github.com/botuniverse/onebot/blob/master/README.md">
    <img src="https://img.shields.io/badge/Onebot-v11-brightgreen?style=for-the-badge" alt="onebot">
</a>
<a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/static/v1?label=Nonebot&message=^2.0.0&color=red&style=for-the-badge" alt="nonebot">
</a>
<a href="https://pypi.org/project/nonebot-adapter-cqhttp/">
    <img src="https://img.shields.io/static/v1?label=Nonebot-adapters-onebot&message=^2.0.0%2Dbeta.1&color=red&style=for-the-badge" alt="nonebot-adapters-cqhttp">
</a>
</div>

## 简介
本插件是针对BWIKI助手解析的非官方Nonebot2插件移植版

关于BWiki助手解析接入方式，请参阅 [BWIKI - WIKI助手文档](https://wiki.biligame.com/wiki/WIKI%E5%8A%A9%E6%89%8B%E6%96%87%E6%A1%A3)

### 可配置项（可选）
```
BWIKI_NAVIGATOR_COMMAND="bwiki"                 // 本插件的主查询命令名
BWIKI_NAVIGATOR_COMMAND_ALIAS=["wiki"]         // 本插件的查询命令别名列表
```

### 使用方法
```
/bwiki bwiki子站域名 页面名(可选)
```

### 示例
```
/bwiki clover

四叶草剧场WIKI https://wiki.biligame.com/clover


/bwiki clover 沙盒

四叶草剧场WIKI 沙盒
https://wiki.biligame.com/clover/?curid=19
在这里测试你的代码！
隐藏的wiki bot转换语句
[图片]
[图片]
```

### 已完整接入帮助菜单
[nonebot-plugin-help](https://github.com/xzhouqd/nonebot-plugin-help) ([PyPI](https://pypi.python.org/pypi/nonebot-plugin-help))