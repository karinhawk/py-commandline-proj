import nox

# if nox is run without arguments, it will only run lint and tests
nox.options.sessions = "lint", "tests"


@nox.session(python=["3.8", "3.7", "3.9"])
def tests(session):
    # excludes e2e tests from automated testing
    # (not is keyword and e2e tests are marked as e2e)
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    # Use *args when you have a variable number of arguments
    session.run("pytest", *args)


# run linting(flake8) on three locations automatically for coverage
# but can override this
# override using -- which separates the option from nox's options
locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.8", "3.7", "3.9"])
def lint(session):
    args = session.posargs or locations
    # installs flake8 via pip into the virtual environment
    # the second argument here is to enable flake8 warnings
    # the warnings will trigger if black is going to reformat a src file
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


# flake8 glues together different tools - which discover different errors
# these are prefixed by specific letters which group the errors into
# VIOLATION CLASSES

# F - reported by pyflakes (invalid python code in source files)
# W / E - warnings and errors reported by pycodestyle (style conventions)
# C - reported by mccabe (checks code complexity against configured limit)
# set this limit in .flake8 file!!! - gitignored :))


@nox.session(python="3.8")
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
