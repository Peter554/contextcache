# type: ignore

import subprocess

import shrtcodes

shortcodes = shrtcodes.Shrtcodes()


@shortcodes.register_inline("embed_file")
def handle_embed_file(file_path, syntax="", comment_char="#"):
    with open(file_path) as f:
        return f"""```{syntax}
{comment_char} {file_path}
{f.read().strip()}
```"""


@shortcodes.register_inline("execute_python")
def handle_execute_python(*python_args):
    cmd = subprocess.run(["poetry", "run", "python", *python_args], capture_output=True)
    return f"""```sh
python {' '.join(python_args)}
```

```
{cmd.stdout.decode().strip()}
```"""


shortcodes.create_cli()
