from pathlib import Path
from typing import Any, Dict, Mapping, Set, Tuple

import click

import bento.orchestrator
import bento.result
from bento.context import Context
from bento.decorators import cache_opt, with_metrics
from bento.paths import list_paths
from bento.result import VIOLATIONS_KEY, Baseline, Hash
from bento.target_file_manager import TargetFileManager
from bento.util import echo_newline, echo_next_step


def __archive_help(prog_name: str, headless: bool) -> str:
    block_str = (
        "" if headless else " and will not block commits if `autorun` is enabled"
    )
    return f"""
    Suppress current findings.

    By default, only results introduced by currently staged changes will be
    added to the archive (`.bento/archive.json`). Archived findings will
    not appear in future `{prog_name} check` output{block_str}.

    Use `--all` to archive findings in all Git tracked files, not just those
    that are staged:

        $ {prog_name} archive --all [PATHS]

    Optional PATHS can be specified to archive results from specific directories
    or files.

    Archived findings are viewable in `.bento/archive.json`.
    """


@click.command()
@click.option(
    "--all",
    "all_",
    is_flag=True,
    default=False,
    help="Archive findings for all tracked files.",
)
@cache_opt
@click.argument("paths", nargs=-1, type=Path, autocompletion=list_paths)
@click.pass_obj
@with_metrics
def archive(context: Context, all_: bool, cache: bool, paths: Tuple[Path, ...]) -> None:
    context.validate_init()

    # Default to no path filter
    path_list = list(paths) if len(paths) > 0 else [context.base_path]

    if not context.is_init:
        if all_:
            click.echo(f"Running archive on all tracked files...\n", err=True)
        else:
            click.echo(f"Running archive on staged files...\n", err=True)

    if context.baseline_file_path.exists():
        with context.baseline_file_path.open() as json_file:
            old_baseline = bento.result.load_baseline(json_file)
            old_hashes = {
                h
                for findings in old_baseline.values()
                for h in findings.get(VIOLATIONS_KEY, {}).keys()
            }
    else:
        old_baseline = {}
        old_hashes = set()

    new_baseline: Dict[str, Mapping[Hash, Any]] = {}
    tools = context.tools.values()

    target_file_manager = TargetFileManager(
        context.base_path, path_list, not all_, context.ignore_file_path
    )

    baseline: Baseline = {}
    if context.baseline_file_path.exists():
        with context.baseline_file_path.open() as json_file:
            # TODO there's some deconflicting needed with old_baseline, old_hashes, baseline
            baseline = bento.result.json_to_violation_hashes(json_file)

    all_findings, elapsed = bento.orchestrator.orchestrate(
        baseline, target_file_manager, not all_, tools, use_cache=cache
    )

    n_found = 0
    n_existing = 0
    found_hashes: Set[str] = set()

    for tool_id, vv in all_findings:
        if isinstance(vv, Exception):
            raise vv
        # Remove filtered
        vv = [f for f in vv if not f.filtered]
        n_found += len(vv)
        new_baseline[tool_id] = bento.result.dump_baseline(vv)
        if tool_id in old_baseline:
            new_baseline[tool_id][VIOLATIONS_KEY].update(
                old_baseline[tool_id][VIOLATIONS_KEY]
            )
        for v in vv:
            h = v.syntactic_identifier_str()
            found_hashes.add(h)
            if h in old_hashes:
                n_existing += 1

    n_new = n_found - n_existing

    context.baseline_file_path.parent.mkdir(exist_ok=True, parents=True)
    with context.baseline_file_path.open("w") as json_file:
        bento.result.write_tool_results(json_file, new_baseline)

    finding_source_text = "in this project" if all_ else "due to staged changes"
    success_str = f"{n_new} finding(s) {finding_source_text} were archived, and will be hidden in future runs."
    if n_existing > 0:
        success_str += f"\nAlso kept {n_existing} existing finding(s)."

    click.echo(success_str, err=True)

    if not context.is_init:
        echo_newline()
        echo_next_step("To view archived results", "cat .bento/archive.json")

    if context.on_exit_exception:
        raise context.on_exit_exception


# TODO: make not monkey with globals
def make_archive(prog_name: str, headless: bool) -> click.Command:
    archive.help = __archive_help(prog_name, headless)
    return archive
