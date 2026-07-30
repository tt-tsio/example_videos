#!/usr/bin/env python3
"""Minimal Hunyuan image client: hair-test-2 + Afro."""

import base64
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def data_uri(path: Path) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


payload = {
    "prompt": (
        "Realistically change the hairstyle in the input image to an Afro. "
        "It is crucial that you do not alter the person's facial features, "
        "face shape, skin tone, or expression. Preserve the original hair "
        "color and tones exactly. The new hairstyle should only change the "
        "texture and shape of the hair, and it must blend naturally with the "
        "person's head and the image background."
    ),
    "images": [
        data_uri(HERE / "hair-test-2.png"),
        data_uri(HERE / "afro.png"),
    ],
    "seed": 44,
    "bot_task": "image",
}

req = urllib.request.Request(
    "http://127.0.0.1:8000/v1/ts-runtime/run",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=7200) as resp:
    result = json.load(resp)

header, b64 = result["image"].split(",", 1)
ext = "jpg" if "jpeg" in header else "png"
out_path = HERE / f"out.{ext}"
out_path.write_bytes(base64.b64decode(b64))
print(f"wrote {out_path} ({result['width']}x{result['height']})")
print(f"latency_ms={result.get('latency_ms')}")
