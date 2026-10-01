import pytest

from spotdl.utils.arguments import parse_arguments


def test_parse_arguments(monkeypatch):
    monkeypatch.setattr("sys.argv", ["spotdl", "--invalid-flag-12345"])
    with pytest.raises(SystemExit):
        vars(parse_arguments())


def test_parse_use_official_api(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "spotdl",
            "download",
            "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
            "--use-official-api",
        ],
    )

    arguments = parse_arguments()

    assert arguments.use_official_api is True


def test_parse_audio_providers_alias(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "spotdl",
            "download",
            "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
            "--audio-providers",
            "youtube-music",
            "youtube",
        ],
    )
    arguments = parse_arguments()
    assert arguments.audio_providers == ["youtube-music", "youtube"]


def test_parse_fallback_audio_provider(monkeypatch):
    from spotdl.utils.config import create_settings

    monkeypatch.setattr(
        "sys.argv",
        [
            "spotdl",
            "download",
            "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
            "--audio",
            "youtube-music",
            "--fallback-audio",
            "youtube",
        ],
    )
    arguments = parse_arguments()
    assert arguments.audio_providers == ["youtube-music"]
    assert arguments.fallback_audio_provider == "youtube"

    _, downloader_settings, _ = create_settings(arguments)
    assert downloader_settings["audio_providers"] == ["youtube-music", "youtube"]


@pytest.mark.parametrize(
    "extra, expected",
    [
        ([], []),
        (
            ["https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"],
            ["https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"],
        ),
    ],
)
def test_parse_interactive_query_is_optional(monkeypatch, extra, expected):
    monkeypatch.setattr("sys.argv", ["spotdl", "interactive", *extra])

    arguments = parse_arguments()

    assert arguments.operation == "interactive"
    assert arguments.query == expected
