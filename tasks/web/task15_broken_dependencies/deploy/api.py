#!/usr/bin/env python3

from fastapi import FastAPI
from starlette.responses import RedirectResponse
import subprocess

app = FastAPI()


@app.get("/")
async def index():
    return RedirectResponse(url="/docs")


@app.get("/run-script")
async def run_script():
    try:
        # Run the Bash script
        result = subprocess.run(
            ["/bin/bash", "/app/script.sh"],
            capture_output=True,
            text=True,
            check=True,
            timeout=20,
        )
        return {"status": "success", "output": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}
