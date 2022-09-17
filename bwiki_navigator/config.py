from typing import Set, Optional, Union, List

from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    bwiki_navigator_command: Optional[str]
    bwiki_navigator_command_alias: Optional[Union[Set[str], List[str], str]]

    class Config:
        extra = "ignore"
