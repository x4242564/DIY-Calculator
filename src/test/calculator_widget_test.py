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

# Maps calculator keys to correlating CTkButton objects
CALC_BTNS = {
    '0': 'btn_0', '1': 'btn_1', '2': 'btn_2', '3': 'btn_3', '4': 'btn_4',
    '5': 'btn_5', '6': 'btn_6', '7': 'btn_7', '8': 'btn_8', '9': 'btn_9',
    '+': 'btn_plus', '-': 'btn_minus', '*': 'btn_multiply', '/': 'btn_divide',
    '^': 'btn_power', '(': 'btn_lparen', ')': 'btn_rparen', '.': 'btn_point',
}


class CalculatorWidgetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # calc.py already builds one App (and its Calculator frame) at import
        # time; reuse it instead of constructing a second Tk root.
        cls.calculator = calc.app.calculator_frame

    def setUp(self):
        calc.calculation = ''
        calc.eval = ''
        calc.ans = ''
        self.calculator.delete()

    def press(self, keys):
        for key in keys:
            getattr(self.calculator, CALC_BTNS[key]).invoke()

    def display(self):
        return self.calculator.result_txt.get('1.0', 'end-1c')

    # ---- digit buttons ----

    def test_each_digit_button_appends_its_own_digit(self):
        for digit in '0123456789':
            with self.subTest(digit=digit):
                self.setUp()
                self.press(digit)
                self.assertEqual(calc.calculation, digit)
                self.assertEqual(self.display(), digit)

    def test_digit_buttons_concatenate_in_press_order(self):
        self.press('123')
        self.assertEqual(calc.calculation, '123')
        self.assertEqual(self.display(), '123')

    def test_digit_button_after_evaluation_starts_a_new_calculation(self):
        self.press('2+2')
        self.calculator.btn_eval.invoke()
        self.calculator.btn_5.invoke()
        self.assertEqual(calc.calculation, '5')
        self.assertEqual(calc.ans, '4')
        self.assertEqual(self.display(), '5')

    # ---- operator buttons ----

    def test_each_operator_button_appends_its_own_symbol(self):
        for symbol in ('+', '-', '*', '/', '^'):
            with self.subTest(symbol=symbol):
                self.setUp()
                self.press('5')
                getattr(self.calculator, CALC_BTNS[symbol]).invoke()
                self.press('3')
                expected = f'5{symbol}3'
                self.assertEqual(calc.calculation, expected)
                self.assertEqual(self.display(), expected)

    # ---- parenthesis buttons ----

    def test_parenthesis_buttons_build_a_grouped_expression(self):
        self.press('(7+3)')
        self.assertEqual(calc.calculation, '(7+3)')
        self.calculator.btn_eval.invoke()
        self.assertEqual(calc.eval, '10')
        self.assertEqual(self.display(), '10')

    # ---- decimal point button ----

    def test_point_button_builds_a_decimal_number(self):
        self.press('3.14')
        self.assertEqual(calc.calculation, '3.14')
        self.assertEqual(self.display(), '3.14')

    # ---- evaluate ("=") button ----

    def test_eval_button_computes_correct_results_through_the_real_interpreter(self):
        cases = [
            ('7+2', '9'),
            ('10-4', '6'),
            ('2*3', '6'),
            ('7/2', '3.5'),
            ('2^3', '8'),
        ]
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.setUp()
                self.press(expression)
                self.calculator.btn_eval.invoke()
                self.assertEqual(calc.eval, expected)
                self.assertEqual(self.display(), expected)

    def test_eval_button_displays_error_for_unresolvable_expressions(self):
        for expression in ('(2+3', '5/0'):
            with self.subTest(expression=expression):
                self.setUp()
                self.press(expression)
                self.calculator.btn_eval.invoke()
                self.assertEqual(self.display(), 'Error')

    # ---- Ans button ----

    def test_ans_button_inserts_the_previous_result(self):
        self.press('2+2')
        self.calculator.btn_eval.invoke()
        self.calculator.btn_clear.invoke()
        self.calculator.btn_ans.invoke()
        self.assertEqual(calc.calculation, '4')
        self.assertEqual(self.display(), '4')

    def test_ans_button_without_prior_result_adds_nothing(self):
        self.calculator.btn_ans.invoke()
        self.assertEqual(calc.calculation, '')
        self.assertEqual(self.display(), '')

    # ---- Clear ("C") button ----

    def test_clear_button_saves_the_last_result_as_ans(self):
        self.press('2+2')
        self.calculator.btn_eval.invoke()
        self.calculator.btn_clear.invoke()
        self.assertEqual(calc.calculation, '')
        self.assertEqual(calc.eval, '')
        self.assertEqual(calc.ans, '4')
        self.assertEqual(self.display(), '')

    def test_clear_button_without_a_prior_evaluation_leaves_ans_unset(self):
        self.press('42')
        self.calculator.btn_clear.invoke()
        self.assertEqual(calc.calculation, '')
        self.assertEqual(calc.ans, '')
        self.assertEqual(self.display(), '')

    # ---- Backspace ("Del") button ----

    def test_backspace_button_removes_the_last_character(self):
        self.press('12')
        self.calculator.btn_backspace.invoke()
        self.assertEqual(calc.calculation, '1')
        self.assertEqual(self.display(), '1')

    def test_backspace_button_on_an_empty_calculation_stays_empty(self):
        self.calculator.btn_backspace.invoke()
        self.assertEqual(calc.calculation, '')
        self.assertEqual(self.display(), '')

    def test_backspace_button_after_evaluation_reverts_to_the_expression(self):
        self.press('1+1')
        self.calculator.btn_eval.invoke()
        self.calculator.btn_backspace.invoke()
        self.assertEqual(calc.eval, '')
        self.assertEqual(calc.ans, '')
        self.assertEqual(calc.calculation, '1+1')
        self.assertEqual(self.display(), '1+1')


if __name__ == '__main__':
    unittest.main()
