import framebuf


class Icon:
    # Formats
    FMT_HLSB = framebuf.MONO_HLSB
    FMT_VLSB = framebuf.MONO_VLSB

    # The Database of Icons
    # Format: 'name': (byte_data, width, height, format)
    _DATABASE = {
        # 1. Success / Checkmark
        "check": (b"\x00\x01\x03\x06\x8c\xd8\x70\x20", 8, 8, FMT_HLSB),
        # 2. Error / X
        "error": (b"\x81\x42\x24\x18\x18\x24\x42\x81", 8, 8, FMT_HLSB),
        # 3. Heart
        "heart": (b"\x00\x66\xff\xff\x7e\x3c\x18\x00", 8, 8, FMT_HLSB),
        # 4. WiFi (Signal)
        "wifi": (b"\x00\x3c\x42\x81\x3c\x42\x18\x00", 8, 8, FMT_HLSB),
        # 5. Bluetooth
        "bt": (b"\x18\x28\x48\x54\x54\x48\x28\x18", 8, 8, FMT_HLSB),
        # 6. Battery (Full)
        "battery": (b"\x00\x7e\x42\x7e\x7e\x42\x7e\x00", 8, 8, FMT_HLSB),
        # 7. Bell (Notification)
        "bell": (b"\x18\x3c\x3c\x3c\x18\x18\x5a\x24", 8, 8, FMT_HLSB),
        # 8. Lock (Locked)
        "lock": (b"\x18\x24\x24\x18\x7e\x7e\x7e\x00", 8, 8, FMT_HLSB),
        # 9. Unlock (Open)
        "unlock": (b"\x18\x24\x20\x18\x7e\x7e\x7e\x00", 8, 8, FMT_HLSB),
        # 10. Smiley Face
        "smile": (b"\x3c\x42\xa5\x81\xa5\x99\x42\x3c", 8, 8, FMT_HLSB),
        # 11. Sun (Brightness/Weather)
        "sun": (b"\x00\x24\x18\xbd\xbd\x18\x24\x00", 8, 8, FMT_HLSB),
        # 12. Music Note
        "music": (b"\x06\x06\x06\x0e\x7e\x7e\x1c\x00", 8, 8, FMT_HLSB),
        # 13. Arrow Up
        "up": (b"\x18\x3c\x7e\xff\x18\x18\x18\x18", 8, 8, FMT_HLSB),
        # 14. Arrow Down
        "down": (b"\x18\x18\x18\x18\xff\x7e\x3c\x18", 8, 8, FMT_HLSB),
        "cube": (b"\x00\x7e\x42\x42\x42\x42\x7e\x00", 8, 8, FMT_HLSB),
        "reboot": (b"\x3c\x40\x87\x84\x87\x40\x3c\x00", 8, 8, FMT_HLSB),
        "info": (b"\x3c\x42\x5a\x48\x48\x42\x3c\x00", 8, 8, FMT_HLSB),
        "settings": (b"\x36\x6c\x3c\x7e\x3c\x6c\x36\x00", 8, 8, FMT_HLSB),
        "logo": (
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            32,
            32,
            FMT_HLSB,
        ),
    }

    def __init__(self, name):
        # Check if icon exists, otherwise load 'error'
        if name in self._DATABASE:
            icon_def = self._DATABASE[name]
        else:
            print(f"Warning: Icon '{name}' not found. Using default.")
            icon_def = self._DATABASE["error"]

        self.raw_data = icon_def[0]
        self.width = icon_def[1]
        self.height = icon_def[2]
        self.format = icon_def[3]

        # Create the FrameBuffer
        self.fb = framebuf.FrameBuffer(
            bytearray(self.raw_data), self.width, self.height, self.format
        )

