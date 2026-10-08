from main import main


def test_main_returns_message(capsys):
    result = main()
    captured = capsys.readouterr()
    assert "Snowflake" in captured.out
    assert result == "Deployed successfully to Snowflake.. hurray!"
