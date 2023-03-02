import click.testing
import pytest
import requests

from py_commandline_proj import console

# test fixtures are used as a template for all tests in the file
# here we are creating an instance of the commandline interface for all tests
# arrange!!


@pytest.fixture
def runner():
    # clirunner invokes the command line interface in the test file
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("py_commandline_proj.wikipedia.random_page")


def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    runner.invoke(console.main, ["language=pl"])
    mock_wikipedia_random_page.assert_called_with(Language="pl")


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    # setting json response that would you theoretically get
    # the long string of dotted notation is
    # the object returned from an api call
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet"
    }
    return mock

# must pass runner as a parameter for it to be used in the test case


def test_main_succeeds(runner, mock_requests_get):
    # calling a specific function from a file (file is console)
    # act!!
    result = runner.invoke(console.main)
    # assert!!
    assert result.exit_code == 0

# that was not a fast, isolated, and repeatable test though!
# because its sending an actual request out - we should mock data instead!
# Use mocker.patch to replace the requests.get function by a mock object.


def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner, mock_requests_get):
    runner.invoke(console.main)
    assert mock_requests_get.called

# call_args allows you to check what was passed to the function
# in this case the first parameter is the url fetched ([0])
# which will include wikipedia


def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]

# asserting an exception using side_effect
# anything but exit code 0 is an error


def test_main_fails_on_requests_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1

# raising exception if something goes wrong, but using mock!


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
