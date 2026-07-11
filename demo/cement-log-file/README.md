# cement-log-file

Demonstrates `CEMENT_FRAMEWORK_LOG_FILE` ([issue #593]) — routing Cement's
internal **framework** debug log to a file, in addition to the console.

This is the framework's own `minimal_logger` output (setup/run/close internals),
separate from your application's log handler.

## Run

```bash
./run.sh
```

You'll see Cement's framework debug lines on the console, and the same lines
captured in `./framework.log`.

## How it works

Framework logging is toggled by the usual switches — `CEMENT_LOG=1`,
`debug=True`, `--debug`, or the deprecated `CEMENT_FRAMEWORK_LOGGING`. When it's
enabled **and** `CEMENT_FRAMEWORK_LOG_FILE` points at a path, that output is
*also* written to the file:

```bash
CEMENT_LOG=1 CEMENT_FRAMEWORK_LOG_FILE=./framework.log python app.py
```

## Behavior notes

- **Additive only.** `CEMENT_FRAMEWORK_LOG_FILE` alone does **not** enable
  logging — with only `CEMENT_LOG=1` (and no file var) you get console output
  and no file, exactly as before.
- **No phantom file.** The file is created lazily, on the first log write —
  setting the var while logging is off leaves no empty file behind.
- **Never crashes the host app.** An invalid/unwritable path is silently
  ignored; the console handler is unaffected.

[issue #593]: https://github.com/datafolklabs/cement/issues/593
