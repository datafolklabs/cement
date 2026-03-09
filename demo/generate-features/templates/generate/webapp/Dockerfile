FROM python:{{ python_version }}-slim

WORKDIR /app

COPY . .

# Drop root: create an unprivileged user, hand it /app, switch to it.
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

CMD ["python", "app.py"]
