# {{ project_name }} — {{ web_framework }} {{ framework_version }} entrypoint.
from app import app

if __name__ == "__main__":
    app.run()
