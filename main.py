# (©)Pyro-Senpai

import re
import hydrogram
from hydrogram.types import Message, InlineKeyboardButton
from hydrogram.raw import types as raw_types

# ==========================================
# 1. INLINE BUTTON COLOR/STYLE PATCH
# ==========================================

# Direct style parameter support ke liye init patch
original_btn_init = InlineKeyboardButton.__init__

def patched_btn_init(self, *args, style=None, **kwargs):
    original_btn_init(self, *args, **kwargs)
    self.style = style

InlineKeyboardButton.__init__ = patched_btn_init

# Styles apply karne aur raw attributes assign karne ke liye write patch
original_btn_write = InlineKeyboardButton.write

async def patched_btn_write(self, client):
    style_type = getattr(self, "style", None)
    text = self.text

    # Direct style="primary" ya text ke sath tag support (agar typo bhi ho)
    if text and "#" in text:
        keywords = [
            ("#primary", "primary"),
            ("#danger", "danger"),
            ("#success", "success"),
            ("#succes", "success"),
        ]
        text_lower = text.lower()
        for keyword, s_type in keywords:
            if keyword in text_lower:
                if not style_type:
                    style_type = s_type
                self.text = re.sub(re.escape(keyword), "", text, flags=re.IGNORECASE).strip()
                break

    res_btn = await original_btn_write(self, client)

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

InlineKeyboardButton.write = patched_btn_write


# ==========================================
# 2. MESSAGE EFFECT ID REPLIES PATCH
# ==========================================

def patch_reply_method(method_name: str):
    if not hasattr(Message, method_name):
        return

    original_method = getattr(Message, method_name)

    async def patched_method(self, *args, message_effect_id=None, **kwargs):
        if message_effect_id is not None:
            self._client._current_message_effect_id = message_effect_id
        try:
            return await original_method(self, *args, **kwargs)
        finally:
            if message_effect_id is not None:
                self._client._current_message_effect_id = None

    setattr(Message, method_name, patched_method)

# Safe patching for all common reply methods
reply_methods = [
    "reply", 
    "reply_text", 
    "reply_photo", 
    "reply_video", 
    "reply_document", 
    "reply_sticker", 
    "reply_animation"
]

for method in reply_methods:
    patch_reply_method(method)