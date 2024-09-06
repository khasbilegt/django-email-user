import sys

import nox


@nox.session
@nox.parametrize("django", ["4.2", "5.0", "main"])
def test(session, django):
    if django != "4.2" and not sys.version_info.minor >= 10:
        session.skip()
    else:
        if django == "main":
            session.run(
                "pip", "install", "https://github.com/django/django/archive/main.tar.gz"
            )
        else:
            session.run("pip", "install", f"django=={django}")
        session.run("python", "makemigrations.py")
        session.run("coverage", "run", "runtests.py")
        session.run("coverage", "report")
        session.run("coverage", "xml")
