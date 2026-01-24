Took the example from: https://github.com/subconscious-systems/subconscious?tab=readme-ov-file#subconscous-python-sdk

Seems to call the wrong endpoint. Stacktrace: 

```bash
Traceback (most recent call last):
  File "/Users/michael/.local/share/uv/python/cpython-3.10.18-macos-aarch64-none/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/Users/michael/.local/share/uv/python/cpython-3.10.18-macos-aarch64-none/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher/../../debugpy/__main__.py", line 71, in <module>
    cli.main()
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher/../../debugpy/../debugpy/server/cli.py", line 508, in main
    run()
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher/../../debugpy/../debugpy/server/cli.py", line 358, in run_file
    runpy.run_path(target, run_name="__main__")
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 310, in run_path
    return _run_module_code(code, init_globals, run_name, pkg_name=pkg_name, script_name=fname)
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 127, in _run_module_code
    _run_code(code, mod_globals, init_globals, mod_name, mod_spec, pkg_name, script_name)
  File "/Users/michael/.cursor/extensions/ms-python.debugpy-2025.18.0-darwin-arm64/bundled/libs/debugpy/_vendored/pydevd/_pydevd_bundle/pydevd_runpy.py", line 118, in _run_code
    exec(code, run_globals)
  File "/Users/michael/Desktop/subconcious/calc.py", line 51, in <module>
    response = client.agent.run(messages, agent_name="math_agent")
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/subconscious/client.py", line 82, in run
    return tim_streaming(
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/subconscious/tim_api.py", line 86, in tim_streaming
    response = openai_client.chat.completions.create(
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/openai/_utils/_utils.py", line 286, in wrapper
    return func(*args, **kwargs)
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/openai/resources/chat/completions/completions.py", line 1192, in create
    return self._post(
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/openai/_base_client.py", line 1259, in post
    return cast(ResponseT, self.request(cast_to, opts, stream=stream, stream_cls=stream_cls))
  File "/Users/michael/Desktop/subconcious/.venv/lib/python3.10/site-packages/openai/_base_client.py", line 1047, in request
    raise self._make_status_error_from_response(err.response) from None
openai.NotFoundError: <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Error</title>
</head>
<body>
<pre>Cannot POST /v1/chat/completions</pre>
</body>
</html>

```