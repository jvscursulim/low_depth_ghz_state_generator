import nox

@nox.session(name="tests", python="3.9")
def tests_coverage(session):
    """ Run pytest and create coverage report."""

    session.install("pipenv")
    session.run("pipenv", "install")
    session.run("pytest", "--cov=./", "--cov-report=xml")

@nox.session(name="style")
def style_check(session):
    """ Install black and test if the linting is correct."""

    session.install("black")
    session.run("black", "--check", "--diff", "tests", "ghz_state_generator")