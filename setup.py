from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-library-web",
    install_requires=[
        "analytics-python<2.0",
        "blinker",
        "dnspython<3.0.0",
        "Flask-Caching",
        "Flask-CORS",
        "Flask-DotEnv",
        "Flask-Session",
        "Flask==2.0.2",
        "sweetrpg-web-core",
        "sweetrpg-library-objects",
        "sweetrpg-client",
        "kanka",
        "python-dateutil",
        "python-dotenv==0.21.1",
        "python-editor",
        "PyYAML==6.0",
        "redis",
        "hiredis",
        "requests",
        "sentry-sdk[flask]==1.5.0",
        "greenlet==2.0.2",
        "SQLAlchemy==1.4.44",
        "urllib3==1.26.15",
        "python-logstash-async",
        "jsonapi-client",
    ],
    extras_require={},
)
