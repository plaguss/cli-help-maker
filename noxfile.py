import nox

@nox.session
def install(session):
    session.run("flit", "install", "--deps", "production")

@nox.session
def tests(session):
    # session.install('pytest')
    session.run("pytest", "tests/integration")


@nox.session
def lint(session):
    # session.install('flake8')
    session.run("isort", "cli_help_maker", "examples")
    session.run("black", "cli_help_maker", "examples")
