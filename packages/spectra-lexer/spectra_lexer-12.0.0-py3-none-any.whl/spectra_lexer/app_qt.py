""" Main module for the standalone Qt GUI application. """

import sys

from PyQt5.QtWidgets import QApplication

from spectra_lexer import SpectraOptions
from spectra_lexer.gui_qt import build_app, GUILayerExtended


def main() -> int:
    """ In standalone mode, we must create a QApplication before building any of the GUI. """
    q_app = QApplication(sys.argv)
    opts = SpectraOptions("Run Spectra as a standalone GUI application.")
    spectra = opts.compile()
    translations_paths = opts.translations_paths()
    index_path = opts.index_path()
    cfg_path = opts.config_path()
    gui = GUILayerExtended(spectra.translations_io, index_path, cfg_path,
                           spectra.search_engine, spectra.analyzer, spectra.graph_engine, spectra.board_engine)
    app = build_app(gui, spectra.log)
    app.run_async(gui.load_translations, *translations_paths)
    app.load_user_files()
    # After everything is loaded, start a GUI event loop and run it indefinitely.
    return q_app.exec_()


if __name__ == '__main__':
    sys.exit(main())
