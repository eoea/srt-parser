""" Module Parser handles the parsing of SRT files.
    Contains the following classes:
        - `Tokens`: This is a private Class.
        - `Subtitle`: This is a private Class.
        - `Parser`: This is a public Class.

    Created by Emile O. E. Antat (eoea) <eoea754@gmail.com>
"""
import re
import yaml
from dataclasses import dataclass
from typing import List, Dict


class Tokens:
    """Tokens: handles the loading of the srt_subtitle_token_specification.yml
    (Private Class)."""

    token_path: str = "config/srt_subtitle_token_specification.yml"

    def __enter__(self):
        self.yaml_file = open(self.token_path, "r", encoding="utf-8")
        return self

    def _load(self):
        return yaml.safe_load(self.yaml_file)

    def __exit__(self, *args, **kwargs):
        self.yaml_file.close()


@dataclass
class Subtitle:
    """Struct for the Subtitle in SRT format (Private Class):
    - `offset`: a numeric counter identifying each sequential subtitle.
    - `start_timestamp`: when the subtitle should appear.
    - `end_timestamp`: when the subtitle should disappear.
    - `dialogue`: the subtitle text."""

    offset: int
    start_timestamp: str
    end_timestamp: str
    dialogue: str


class Parser:
    """Handles the SRT parser. This class accepts one argument `filepath` which
    is the file path to the SRT file you want to parse.

    Methods:
        - `parse`:  Takes no argument and returns a list of `Subtitle`(s)
    """

    tokens: Dict = {}
    tokenized_subtitles: List[Subtitle] = []
    subtitle = Subtitle(0, "", "", "")

    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse(self) -> List[Subtitle]:
        """Parses the SRT file and returns the contents as a list of `Subtitle`(s)."""

        with Tokens() as tok:
            self.tokens = tok._load()["SRT_SUBTITLE_TOKEN_SPECIFICATION"]

        with open(self.filepath) as file:
            dialogue = ""
            for line in file:
                if re.fullmatch(self.tokens["OFFSET"], line):
                    self.subtitle.offset = re.search(self.tokens["OFFSET"], line)[0]
                elif bool(re.search(self.tokens["TIMECODE"], line)):
                    (
                        self.subtitle.start_timestamp,
                        self.subtitle.end_timestamp,
                    ) = re.split(self.tokens["TIMECODE"], line)
                elif re.fullmatch(self.tokens["BLANKLINE"], line):
                    self.subtitle.dialogue = dialogue
                    self.tokenized_subtitles.append(self.subtitle)
                    # Reset:
                    dialogue = ""
                    self.subtitle = Subtitle(0, "", "", "")
                else:
                    dialogue += line
            # Reached EOF, append the last subtitle chunk:
            self.subtitle.dialogue = dialogue
            self.tokenized_subtitles.append(self.subtitle)

        return self.tokenized_subtitles
