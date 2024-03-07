import re
import logging
from enum import Enum
from typing import Tuple
from typing import Union

import semantic_release as sr
from git.objects.commit import Commit
from pydantic.dataclasses import dataclass
from semantic_release.commit_parser.util import breaking_re
from semantic_release.commit_parser.util import parse_paragraphs

log = logging.getLogger(__name__)


def _logged_parse_error(commit: Commit, error: str) -> sr.ParseError:
    """Log a parse error"""
    log.debug(error)
    return sr.ParseError(commit, error=error)


class CommitTags(str, Enum):
    """Tag enum for allowed tags with Ocarinow Commit Parser"""

    ADD = "[ADD]"
    BREAK = "[BREAK]"
    BREAKING = "[BREAKING]"
    CI = "[CI]"
    CONFIG = "[CONFIG]"
    DEBUG = "[DEBUG]"
    DEV = "[DEV]"
    DOC = "[DOC]"
    FEAT = "[FEAT]"
    FIX = "[FIX]"
    PERF = "[PERF]"
    REFACTO = "[REFACTO]"
    RM = "[RM]"
    TEST = "[TEST]"
    STYLE = "[STYLE]"


LONG_TYPE_NAMES = {
    CommitTags.ADD: "diff",
    CommitTags.BREAK: "breaking",
    CommitTags.BREAKING: "breaking",
    CommitTags.CI: "CICD",
    CommitTags.CONFIG: "configuration",
    CommitTags.DEBUG: "diff",
    CommitTags.DEV: "diff",
    CommitTags.DOC: "documentation",
    CommitTags.FEAT: "feature",
    CommitTags.FIX: "fix",
    CommitTags.PERF: "performance",
    CommitTags.REFACTO: "refactor",
    CommitTags.RM: "diff",
    CommitTags.TEST: "test",
    CommitTags.STYLE: "style",
}


@dataclass
class OcarinowParserOptions(sr.ParserOptions):
    """Options dataclass for OcarinowCommitParser"""

    allowed_tags: Tuple[str, ...] = (
        CommitTags.ADD,
        CommitTags.BREAK,
        CommitTags.BREAKING,
        CommitTags.CI,
        CommitTags.CONFIG,
        CommitTags.DEBUG,
        CommitTags.DEV,
        CommitTags.DOC,
        CommitTags.FEAT,
        CommitTags.FIX,
        CommitTags.REFACTO,
        CommitTags.RM,
        CommitTags.TEST,
        CommitTags.STYLE,
    )
    minor_tags: Tuple[str, ...] = (CommitTags.FEAT,)
    patch_tags: Tuple[str, ...] = (CommitTags.FIX, CommitTags.PERF)
    default_bump_level: sr.LevelBump = sr.LevelBump.NO_RELEASE

    @property
    def TAGS_FOR_REGEX(self):
        """Replace allowed tags with correct regex syntax"""
        return [tag.value.replace("[", "\[").replace("]", "\]") for tag in CommitTags]


class OcarinowCommitParser(sr.CommitParser[sr.ParseResult, OcarinowParserOptions]):
    """A commit parser for Ocarinow projects"""

    parser_options = OcarinowParserOptions

    def __init__(self, options: OcarinowParserOptions) -> None:
        super().__init__(options)
        self.re_parser = re.compile(
            r"(?P<type>" + "|".join(options.TAGS_FOR_REGEX) + ")+"
            r"(?:\((?P<scope>[^\n]+)\))?"
            r"(?P<break>!)? "
            r"(?P<subject>[^\n]+)"
            r"(:?\n\n(?P<text>.+))?",
            re.DOTALL,
        )

    def parse(self, commit: Commit) -> Union[sr.ParsedCommit, sr.ParseError]:
        """Parse a git commit message"""
        message = str(commit.message)
        parsed = self.re_parser.match(message)
        if not parsed:
            return _logged_parse_error(
                commit, f"Unable to parse commit message: {message}"
            )

        parsed_break = parsed.group("break")
        parsed_scope = parsed.group("scope")
        parsed_subject = parsed.group("subject")
        parsed_text = parsed.group("text")
        parsed_type = parsed.group("type")

        descriptions = parse_paragraphs(parsed_text) if parsed_text else []

        descriptions.insert(0, parsed_subject)

        breaking_descriptions = [
            match.group(1)
            for match in (breaking_re.match(p) for p in descriptions[1:])
            if match
        ]

        if parsed_break or breaking_descriptions:
            level_bump = sr.LevelBump.MAJOR
        elif parsed_type in self.options.minor_tags:
            level_bump = sr.LevelBump.MINOR
        elif parsed_type in self.options.patch_tags:
            level_bump = sr.LevelBump.PATCH
        else:
            level_bump = self.options.default_bump_level
            log.debug(
                "commit %s introduces a level bump of %s due to the default_bump_level",
                commit.hexsha,
                level_bump,
            )
        log.debug("commit %s introduces a %s level_bump", commit.hexsha, level_bump)

        return sr.ParsedCommit(
            bump=level_bump,
            type=LONG_TYPE_NAMES.get(parsed_type, parsed_type),
            scope=parsed_scope,
            descriptions=descriptions,
            breaking_descriptions=breaking_descriptions,
            commit=commit,
        )
