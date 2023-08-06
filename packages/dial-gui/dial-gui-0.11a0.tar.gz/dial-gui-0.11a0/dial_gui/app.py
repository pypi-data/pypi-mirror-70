# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Starting point for the application GUI.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from dial_core.utils import log
from PySide2.QtWidgets import QApplication

from dial_gui.main_window import MainWindowFactory

if TYPE_CHECKING:
    import argparse

LOGGER = log.get_logger(__name__)


def run(args: "argparse.Namespace"):
    """
    Show the main window and start the application.

    Warning:
        The system must be initialized before calling this function.

    See Also:
        `dial_core.initialization.initialize_application`
    """

    main_window = MainWindowFactory()
    main_window.show()

    LOGGER.debug("Command Line Arguments: %s", args)
    LOGGER.info("Dial.")
    LOGGER.info("Started on %s", datetime.now().ctime())

    return QApplication.exec_()
