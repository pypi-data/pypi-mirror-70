# uniform

Uniform - dress your form processing endpoints📋

[![PyPI: uniform](https://img.shields.io/pypi/v/uniform)](https://pypi.org/project/uniform/)
[![Code Style: Black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/ambv/black)

Install: `pip install uniform`

## What this package can do:
- Extract and validate form data against `typesystem.Schema`
- Return 400 Bad Request with validation problems explained

Example:

```python
import uvicorn

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from typesystem import Schema, Boolean

from uniform import Uniform, validate

app = Starlette()


class TestSchema(Schema):
    test = Boolean()


@app.route("/")
@validate(Uniform(TestSchema))
async def home(request: Request) -> PlainTextResponse:
    return JSONResponse(
        content={"ok": True, "description": None, "result": dict(request.state.data)}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

Send POST request to `http://127.0.0.1:8080/` with `application/json`
or `application/x-www-form-urlencoded` data and it will be validated.
