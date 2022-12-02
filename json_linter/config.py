""" Linter configuration """
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict

NamingStyle = Enum("NamingStyle", [
    "CAMEL_CASE",
    "SNAKE_CASE",
    "KEBAB_CASE",
])


@dataclass
class LinterConfig:
    """ Configuration for the linter/fixer """
    indent: int
    naming_style: Optional[NamingStyle]
    encoding: str

    def set_values(self, values: Dict[str, str]):
        """ Set config values by dict, also does some validation """
        naming_styles = [naming_style.name for naming_style in NamingStyle]

        for key in values.keys():
            value = values[key]

            if key == "indent":
                self.indent = int(value)
                continue
            if key == "naming_style":
                if value not in naming_styles:
                    styles_str = ", ".join(naming_styles)
                    raise ValueError(
                        f"Unknown naming style '{value}', "
                        f"options are: {styles_str}"
                    )
                self.naming_style = NamingStyle[value]
                continue

            setattr(self, key, value)
