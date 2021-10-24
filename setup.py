from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-library-model",
    install_requires=[
        "Authlib",
        "blinker",
        "dnspython<2.0.0",
        "Flask-Caching",
        "Flask-Cors",
        "Flask-DotEnv",
        "Flask-REST-JSONAPI",
        "Flask-Session",
        "Flask>=2.0",
        "Flask-Migrate",
        "Flask-MongoEngine",
        "gunicorn",
        "kanka",
        "python-dateutil",
        "python-dotenv",
        "python-editor",
        "PyYAML",
        "redis",
        "requests",
        "sentry-sdk",
        "analytics-python<2.0",
        "sweetrpg-db",
        "sweetrpg-model-core",
        "sweetrpg-api-core",
        "sweetrpg-library-model",
    ],
    extras_require={},
)
