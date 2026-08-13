# (©)Pyro-Senpai

import sys
import hydrogram
from hydrogram.raw import types as raw_types

original_init = hydrogram.types.InlineKeyboardButton.__init__


def patched_init(self, *args, style=None, **kwargs):
    original_init(self, *args, **kwargs)
    self.style = style


hydrogram.types.InlineKeyboardButton.__init__ = patched_init

original_write = hydrogram.types.InlineKeyboardButton.write


async def patched_write(self, client):
    style_type = getattr(self, "style", None)
    text = self.text
    if text and "#" in text:
        for keyword, s_type in [
            ("#primary", "primary"),
            ("#danger", "danger"),
            ("#success", "success"),
            ("#succes", "success"),
        ]:
            if keyword in text.lower():
                style_type = s_type
                self.text = (
                    text.replace(keyword, "")
                    .replace(keyword.upper(), "")
                    .strip()
                )
                break

    res_btn = await original_write(self, client)

    if style_type and hasattr(res_btn, "style"):
        bg_primary = style_type == "primary"
        bg_danger = style_type == "danger"
        bg_success = style_type == "success"
        res_btn.style = raw_types.KeyboardButtonStyle(
            bg_primary=bg_primary or None,
            bg_danger=bg_danger or None,
            bg_success=bg_success or None,
        )
    return res_btn


hydrogram.types.InlineKeyboardButton.write = patched_write