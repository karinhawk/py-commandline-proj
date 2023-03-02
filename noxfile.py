import nox
import tempfile

# if nox is run without arguments, it will only run lint and tests
nox.options.sessions = "lint", "safety", "tests"

# wrapper to install specific versions of dependencies
def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
    session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.8", "3.7", "3.9"])
def tests(session):
    # excludes e2e tests from automated testing
    # (not is keyword and e2e tests are marked as e2e)
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
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
    # import-order orders import statements by google std
    # bugbear finds bugs/design problems
    install_with_constraints(
        session,
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order"
    )
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
    install_with_constraints(session, "black")
    session.run("black", *args)

# uses poetry export to convert poetry lock file to a requirements file
@nox.session(python="3.8")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")

