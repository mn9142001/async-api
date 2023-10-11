import typing
import re

PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")



def compile_path(path: str) -> typing.Pattern:
    
    is_host = not path.startswith("/")

    path_regex = "^"
    duplicated_params = set()

    idx = 0
    param_convertors = {}
    for match in PARAM_REGEX.finditer(path):
        param_name = match.groups("str")[0]
        path_regex += re.escape(path[idx : match.start()])
        path_regex += f"(?P<{param_name}>.*)"

        if param_name in param_convertors:
            duplicated_params.add(param_name)

        idx = match.end()

    if duplicated_params:
        names = ", ".join(sorted(duplicated_params))
        ending = "s" if len(duplicated_params) > 1 else ""
        raise ValueError(f"Duplicated param name{ending} {names} at path {path}")

    if is_host:
        # Align with `Host.matches()` behavior, which ignores port.
        hostname = path[idx:].split(":")[0]
        path_regex += re.escape(hostname) + "$"
    else:
        path_regex += re.escape(path[idx:]) + "$"


    return re.compile(path_regex)
