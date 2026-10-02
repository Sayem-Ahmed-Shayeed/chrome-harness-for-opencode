def test_state_subcommand_works_with_non_tty_stdin(monkeypatch, capsys):
    from chrome_harness import cli
    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(cli.connection, "connection_state", lambda: "no-debug-port")
    assert cli.main(["state"]) == 0
    assert capsys.readouterr().out.strip() == "no-debug-port"
