import sys
import unittest

# calc.py builds an argparse.ArgumentParser and calls parse_args() at import
# time, using whatever is in sys.argv. Hide the test runner's own arguments
# from it so importing calc here doesn't blow up with "unrecognized arguments".
_original_argv = sys.argv
sys.argv = sys.argv[:1]
try:
    import calc
    import logger
    import customtkinter as ctk
finally:
    sys.argv = _original_argv

logger.isLogging = False


class DebugMenuTest(unittest.TestCase):

    def setUp(self):
        # DebugMenu wires its "Fetch Window Size" button straight to
        # master.get_window_size, so give it a real Tk parent carrying a
        # spy in place of that method rather than a bare mock (DebugMenu
        # is a CTkScrollableFrame and needs a genuine Tk widget as master).
        self.parent = ctk.CTkFrame(calc.app)
        self.window_size_calls = []
        self.parent.get_window_size = lambda: self.window_size_calls.append(True)
        logger.isVerbose = True

    def make_menu(self, title='Debug Menu'):
        return calc.DebugMenu(self.parent, title=title)

    def test_fetch_window_size_button_calls_masters_get_window_size(self):
        menu = self.make_menu()
        menu.btn_dim.invoke()
        self.assertEqual(len(self.window_size_calls), 1)
        menu.btn_dim.invoke()
        self.assertEqual(len(self.window_size_calls), 2)

    def test_verbose_checkbox_starts_checked_when_logger_is_verbose(self):
        logger.isVerbose = True
        menu = self.make_menu()
        self.assertEqual(menu.v_var.get(), 1)

    def test_verbose_checkbox_starts_unchecked_when_logger_is_not_verbose(self):
        logger.isVerbose = False
        menu = self.make_menu()
        self.assertEqual(menu.v_var.get(), 0)

    def test_toggling_verbose_checkbox_off_clears_logger_isVerbose(self):
        logger.isVerbose = True
        menu = self.make_menu()
        menu.v_log.toggle()
        self.assertEqual(menu.v_var.get(), 0)
        self.assertFalse(logger.isVerbose)

    def test_toggling_verbose_checkbox_back_on_sets_logger_isVerbose(self):
        logger.isVerbose = False
        menu = self.make_menu()
        menu.v_log.toggle()
        self.assertEqual(menu.v_var.get(), 1)
        self.assertTrue(logger.isVerbose)

    def test_two_toggles_return_logger_isVerbose_to_its_original_value(self):
        logger.isVerbose = True
        menu = self.make_menu()
        menu.v_log.toggle()
        menu.v_log.toggle()
        self.assertTrue(logger.isVerbose)
        self.assertEqual(menu.v_var.get(), 1)


if __name__ == '__main__':
    unittest.main()
