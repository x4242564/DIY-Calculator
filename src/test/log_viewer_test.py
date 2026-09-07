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
finally:
    sys.argv = _original_argv

logger.isLogging = False


class LogViewerTest(unittest.TestCase): # Tests LogViewer's ANSI to Tk-tag translation.

    def setUp(self):
        self.log_viewer = calc.LogViewer(calc.app)

    def text(self):
        return self.log_viewer.log_txt.get('1.0', 'end-1c')

    def tagged_segments(self, tag):
        text_widget = self.log_viewer.log_txt._textbox
        ranges = text_widget.tag_ranges(tag)
        return [text_widget.get(ranges[i], ranges[i + 1]) for i in range(0, len(ranges), 2)]

    def test_plain_text_is_inserted_with_no_color_tag(self):
        self.log_viewer.add_log('plain line\n')
        self.assertEqual(self.text(), 'plain line\n')
        for code in self.log_viewer.ansi_colors:
            self.assertEqual(self.tagged_segments(code), [])

    def test_add_log_appends_rather_than_replacing_prior_lines(self):
        self.log_viewer.add_log('first\n')
        self.log_viewer.add_log('second\n')
        self.assertEqual(self.text(), 'first\nsecond\n')

    def test_recognized_ansi_code_tags_only_the_text_that_follows_it(self):
        red = logger.ansi['RED']
        reset = logger.ansi['RESET']
        self.log_viewer.add_log(f'{red}red text{reset} and plain\n')
        self.assertEqual(self.text(), 'red text and plain\n')
        self.assertEqual(self.tagged_segments('31'), ['red text'])
        self.assertEqual(self.tagged_segments('32'), [])

    def test_each_ansi_color_code_maps_to_its_own_tag(self):
        green = logger.ansi['GREEN']
        blue = logger.ansi['BLUE']
        reset = logger.ansi['RESET']
        self.log_viewer.add_log(f'{green}green{reset} then {blue}blue{reset} end\n')
        self.assertEqual(self.tagged_segments('32'), ['green'])
        self.assertEqual(self.tagged_segments('34'), ['blue'])
        self.assertEqual(self.tagged_segments('31'), [])
        self.assertEqual(self.tagged_segments('33'), [])

    def test_reset_code_clears_the_active_tag(self):
        yellow = logger.ansi['YELLOW']
        reset = logger.ansi['RESET']
        self.log_viewer.add_log(f'{yellow}warned{reset}unwarned\n')
        # only the segment before RESET should carry the tag
        self.assertEqual(self.tagged_segments('33'), ['warned'])

    def test_unrecognized_ansi_code_leaves_text_untagged(self):
        unmapped_code = '\033[99m'
        self.log_viewer.add_log(f'{unmapped_code}mystery\n')
        self.assertEqual(self.text(), 'mystery\n')
        for code in self.log_viewer.ansi_colors:
            self.assertEqual(self.tagged_segments(code), [])

    def test_log_textbox_stays_disabled_after_add_log(self):
        self.log_viewer.add_log('line\n')
        self.assertEqual(self.log_viewer.log_txt.cget('state'), 'disabled')


if __name__ == '__main__':
    unittest.main()
