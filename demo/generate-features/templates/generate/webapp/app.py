"""{{ project_name }} - main application."""


def main():
    print("Hello from {{ project_name }}!")
{% if docker %}
    # docker is a top-level boolean, so the conditional above works directly.
    print("Container build: enabled")
{% endif %}
{% if web_framework == "flask" %}
    print("Web framework: Flask {{ framework_version }}")
{% elif web_framework == "fastapi" %}
    print("Web framework: FastAPI {{ framework_version }}")
{% else %}
    print("Web framework: none")
{% endif %}


if __name__ == "__main__":
    main()
