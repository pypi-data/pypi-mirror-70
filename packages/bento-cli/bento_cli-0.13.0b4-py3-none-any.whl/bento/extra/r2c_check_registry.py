from typing import Type

from bento.extra.base_semgrep import BaseSemgrepParser, BaseSemgrepTool
from bento.parser import Parser


class R2cCheckRegistryParser(BaseSemgrepParser):
    @classmethod
    def tool_id(cls) -> str:
        return R2cCheckRegistryTool.tool_id()


class R2cCheckRegistryTool(BaseSemgrepTool):
    TOOL_ID = "r2c.registry.latest"
    CONFIG = "https://r2c.dev/default-r2c-checks"
    PARSER = R2cCheckRegistryParser

    @classmethod
    def tool_id(cls) -> str:
        return cls.TOOL_ID

    @property
    def config_str(self) -> str:
        return self.CONFIG

    @property
    def parser_type(self) -> Type[Parser]:
        return self.PARSER
