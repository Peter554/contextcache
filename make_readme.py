import subprocess

import shrtcodes

shortcodes = shrtcodes.Shrtcodes()


@shortcodes.register_inline("embed_file")
def handle_embed_file(file_path: str, syntax: str = "") -> str:
    with open(file_path) as f:
        return f"""```sh
cat {file_path}     
```
        
```{syntax}
{f.read().strip()}
```"""


@shortcodes.register_inline("execute_python")
def handle_execute_python(*python_args: str) -> str:
    cmd = subprocess.run(["poetry", "run", "python", *python_args], capture_output=True)
    return f"""```sh
python {' '.join(python_args)}
```

```
{cmd.stdout.decode().strip()}
```"""


shortcodes.create_cli()
