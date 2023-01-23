import logging
from click.testing import CliRunner
from roku_remote.discover import main

__author__ = "gordonaspin"
__copyright__ = "gordonaspin"
__license__ = "MIT"


def test_main(caplog):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    runner = CliRunner()
    response = runner.invoke(main, ["--scope", "roku:ecp", "--log-level", "info", "--timeout", "30"])

    assert response.exit_code == 0
    assert "discovering ..." in caplog.records[0].message
    discovered = False
    for log_record in caplog.records:
        assert log_record.levelno != logging.DEBUG
        assert log_record.levelno != logging.ERROR
        assert log_record.levelno != logging.CRITICAL
        if "discovered:" in log_record.message:
            discovered = True
    assert discovered
    assert "stopping discovery thread" in caplog.records[len(caplog.records) - 1].message
