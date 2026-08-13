# (©)Pyro-Senpai

import re
import hydrogram
from hydrogram.raw import types as raw_types

# 1. InlineKeyboardButton ke init ko patch kar rahe hain taaki 'style' argument accept kare
original_init = hydrogram.types.InlineKeyboardButton.init

def patched_init(self, text: str, *args, style: str = None, **kwargs):
    original_init(self, text, *args, **kwargs)
    self.style = style

hydrogram.types.InlineKeyboardButton.init = patched_init

# 2. write method ko patch kar rahe hain styling apply karne ke liye
original_write = hydrogram.types.InlineKeyboardButton.write

async def patched_write(self, client):
    style_type = getattr(self, "style", None)
    text = self.text

    # Agar text ke andar bhi tag ho, to wahan se bhi style nikal kar name clean kar dega
    if text and "#" in text:
        keywords = [
            ("#primary", "primary"),
            ("#danger", "danger"),
            ("#success", "success"),
            ("#succes", "success"),  # typo handling
        ]
        text_lower = text.lower()
        for keyword, s_type in keywords:
            if keyword in text_lower:
                if not style_type:
                    style_type = s_type
                # Button name se tag ko remove kar dega
                self.text = re.sub(re.escape(keyword), "", text, flags=re.IGNORECASE).strip()
                break

    # Original write call karke raw object lena
    res_btn = await original_write(self, client)

    # Styling apply karna
    if style_type:
        bg_primary = True if style_type == "primary" else None
        bg_danger = True if style_type == "danger" else None
        bg_success = True if style_type in ["success", "succes"] else None

        res_btn.style = raw_types.KeyboardButtonStyle(
            bg_primary=bg_primary,
            bg_danger=bg_danger,
            bg_success=bg_success,
        )

    return res_btn

hydrogram.types.InlineKeyboardButton.write = patched_write