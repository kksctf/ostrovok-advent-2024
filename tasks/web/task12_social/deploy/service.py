import base64
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FLAG: str = "flag{test_0123456789ABCD}"

    FLAG_ENC_KEY: str
    FLAG_SALT: str

    BOT_USERNAME: str


settings = Settings()  # type: ignore
app = FastAPI()

app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")

SEC_TMPL = """
Contact: https://t.me/{bot}?start={start}
Expires: 2024-08-31T21:00:00.000Z
Preferred-Languages: ru
"""

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=settings.FLAG_SALT.encode(),
    iterations=480000,
)
key = kdf.derive(settings.FLAG_ENC_KEY.encode())


def prepare_flag(flag: str) -> str:
    assert flag.endswith("}") and "_" in flag

    flag_body = flag.split("{")[1][:-1]
    flag_sign = flag_body.rsplit("_", maxsplit=1)[-1]

    assert len(flag_sign) == 14

    nonce = os.urandom(12)
    chacha = ChaCha20Poly1305(key)

    encrypted = chacha.encrypt(nonce, flag_sign.encode(), None)

    # nonce_encoded = base64.urlsafe_b64encode(nonce).rstrip(b"=").decode()
    # flag_encoded = base64.urlsafe_b64encode(encrypted).rstrip(b"=").decode()
    encoded = base64.urlsafe_b64encode(nonce + encrypted).decode()

    print(f"{encoded = }, {nonce = }, {encrypted = }, {flag_sign = }")

    return encoded


@app.get("/.well-known/security.txt")
@app.get("/security.txt")
async def get_security() -> PlainTextResponse:
    encoded_flag = prepare_flag(settings.FLAG)

    if len(encoded_flag) >= 64:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="please contact organizer, task is broken",
        )

    return PlainTextResponse(SEC_TMPL.format(bot=settings.BOT_USERNAME, start=encoded_flag))


@app.get("/index")
@app.get("/")
async def index(req: Request) -> HTMLResponse:
    img = req.url_for("static", path="img.png")
    return HTMLResponse(
        f"""<body style="margin: 0; background-image: url('{img}'); background-size: cover;"> </body>"""
    )
