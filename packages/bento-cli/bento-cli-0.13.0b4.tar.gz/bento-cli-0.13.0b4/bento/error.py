from pathlib import Path
from typing import List, Optional

from bento.constants import SUPPORT_EMAIL_ADDRESS


class BentoException(Exception):
    """
    Parent class of all exceptions we anticipate in Bento commands.

    All BentoExceptions are caught and their error messages are printed to the console.
    Inherit from this class to override the message and error code. Make sure to call super().__init__() in the child constructor
    """

    def __init__(self) -> None:
        self.msg: Optional[str] = None
        self.code = 3


class OutdatedPythonException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "Bento requires Python 3.6+. Please ensure you have Python 3.6+ and installed Bento via `pip3 install bento-cli`."


class InvalidRegistrationException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "Could not verify the user's registration."


class NoConfigurationException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "No Bento configuration found. Please run `bento init`."


class NoIgnoreFileException(BentoException):
    def __init__(self, path: Path) -> None:
        super().__init__()
        self.msg = f"No ignore file found (looked in {path}). Please run `bento init`."


class NotAGitRepoException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "Not a git repository."


class ExistingGitHookException(BentoException):
    def __init__(self, hook_path: str) -> None:
        super().__init__()
        self.msg = f"Autorun could not be configured: A legacy pre-commit hook exists. Please remove {hook_path}.pre-bento to continue."


class ToolRunException(BentoException):
    def __init__(self, message: str = "") -> None:
        super().__init__()
        self.msg = f"Bento failed while running a tool: {message}"


class NonInteractiveTerminalException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "Bento can't run this command in a non-interactive terminal."


class InvalidVersionException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = (
            "Bento detected an invalid version in your global configuration file."
        )


class InvalidToolException(BentoException):
    def __init__(self, tool: str, all_tools: str) -> None:
        super().__init__()
        self.msg = f"No tool named '{tool}'. Configured tools are {all_tools}"


class EnabledToolNotFoundException(BentoException):
    def __init__(self, tool: str) -> None:
        super().__init__()
        self.msg = (
            f"Bento didn't recognize the tool named '{tool}', "
            "even though it's enabled in your project configuration.\n"
            "Try updating Bento with `pip install --upgrade bento-cli`."
        )


class UnsupportedGitStateException(BentoException):
    def __init__(self, extra: str = "") -> None:
        super().__init__()
        self.msg = f"Cannot complete running command in this git state. {extra}"


class DockerFailureException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = "Failed to run docker. Please confirm docker is installed and its daemon is running in user mode."


class NoToolsConfiguredException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = f"Please specify a tool with `--tool TOOL_NAME`."


class UnsupportedCIProviderException(BentoException):
    def __init__(self) -> None:
        super().__init__()
        self.msg = (
            "Automated CI installation is avaiable only for GitHub Actions currently, "
            "but your project does not seem to be using GitHub.\n"
            f"Please contact {SUPPORT_EMAIL_ADDRESS} if this is incorrect."
        )


class NodeError(Exception):
    """
    Node not found or node version not supported by ESLint 6
    """


class IncompatibleParametersException(BentoException):
    def __init__(self, parameters: List[str]) -> None:
        super().__init__()
        self.msg = f"Parameters {parameters} can not be used together."


class MultipleErrorsException(BentoException):
    def __init__(self, errors: List[BentoException]) -> None:
        super().__init__()
        messages = "\n\n".join(
            error.msg if error.msg else str(error) for error in errors
        )
        self.msg = f"The following errors occurred during execution:\n\n{messages}"
