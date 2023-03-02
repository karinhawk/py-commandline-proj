import nox

@nox.session(python=["3.8", "3.7", "3.9"])
def tests(session):
    #excludes e2e tests from automated testing (not is keyword and e2e tests are marked as e2e)
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)