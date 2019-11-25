__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
appserver.py
- creates an application instance and runs the dev server
"""

if __name__ == '__main__':
    from application.main import create_app
    app = create_app()
    app.run()
