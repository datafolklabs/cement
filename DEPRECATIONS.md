# Cement Deprecations

This document mirrors the canonical GitBook narrative at
[docs.builtoncement.com/release-information/deprecations](https://docs.builtoncement.com/release-information/deprecations)
for in-repo discoverability. Each deprecation has an H2 section with
its registry ID. New IDs append at the bottom under their
since-version section.

For runtime behavior, the `cement.core.deprecations.deprecate()`
helper emits a `DeprecationWarning` whose message includes a
back-link to the corresponding GitBook anchor.

## 3.0.8-1

**Surface:** Environment variable `CEMENT_FRAMEWORK_LOGGING`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Use `CEMENT_LOG` instead. Single-pass migration:

```bash
# Before
export CEMENT_FRAMEWORK_LOGGING=true

# After
export CEMENT_LOG=true
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-1)

## 3.0.8-2

**Surface:** `App.Meta.framework_logging`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Will be changed or removed. Migrate to the `CEMENT_LOG` environment
variable surface (see `3.0.8-1`).

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-2)

## 3.0.10-1

**Surface:** `cement.ext.ext_logging.LoggingLogHandler.fatal()` /
`set_level('FATAL')`
**Since:** Cement 3.0.10
**Removal:** Cement v3.2.0

Use `critical()` / `set_level('CRITICAL')` instead.

```python
# Before
app.log.fatal('something broke')
app.log.set_level('FATAL')

# After
app.log.critical('something broke')
app.log.set_level('CRITICAL')
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.10-1)

## 3.0.16-1

**Surface:** `cement.ext.ext_smtp.SMTPMailHandler.send()` return type
**Since:** Cement 3.0.16
**Removal:** Cement v3.2.0

The `bool` return value is deprecated; in v3.2.0 the method will
return the `smtplib` senderrs `dict`.

```python
# Before (3.0.x)
ok = app.mail.send('hello')
if not ok:
    handle_error()

# After (3.2.0+)
errs = app.mail.send('hello')
if errs:
    handle_error_per_recipient(errs)
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.16-1)
