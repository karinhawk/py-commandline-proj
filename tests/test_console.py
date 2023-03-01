import click.testing
import pytest

from py_commandline_proj import console

#test fixtures are used as a template for all tests in the file
#here we are creating an instance of the commandline interface for all tests
#arrange!!
@pytest.fixture
def runner():
    #clirunner invokes the command line interface in the test file
    return click.testing.CliRunner()

#must pass runner as a parameter for it to be used in the test case
def test_main_succeeds(runner):
    #calling a specific function from a file (file is console)
    #act!!
    result = runner.invoke(console.main)
    #assert!!
    assert result.exit_code == 0

