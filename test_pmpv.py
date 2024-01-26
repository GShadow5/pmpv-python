import unittest
from io import StringIO
from unittest.mock import patch
from pmpv import Variables, evaluate_tokens, tokenize, main

class TestVariables(unittest.TestCase):
    def setUp(self):
        self.variables = Variables.get_instance()

    def tearDown(self):
        self.variables.clear()

    def test_get_set(self):
        self.variables.set('name', 'John')
        self.assertEqual(self.variables.get('name'), 'John')

    def test_get_nonexistent(self):
        self.assertIsNone(self.variables.get('age'))

    def test_contains(self):
        self.variables.set('name', 'John')
        self.assertTrue(self.variables.contains('name'))
        self.assertFalse(self.variables.contains('age'))

    def test_clear(self):
        self.variables.set('name', 'John')
        self.variables.clear()
        self.assertIsNone(self.variables.get('name'))

    def test_str_representation(self):
        self.variables.set('name', 'John')
        self.assertEqual(str(self.variables), "{'name': 'John'}")

    def test_repr_representation(self):
        self.variables.set('name', 'John')
        self.assertEqual(repr(self.variables), "{'name': 'John'}")

class TestTokenize(unittest.TestCase):
    def test_valid_input(self):
        userInput = "x = 5 + (4 - 2)"
        expected_tokens = ['x', '=', 5, '+', '(', 4, '-', 2, ')']
        self.assertEqual(tokenize(userInput), expected_tokens)

    def test_invalid_parentheses(self):
        userInput = "x = (5 + 2"
        self.assertIsNone(tokenize(userInput))

    def test_invalid_assignment(self):
        userInput = "x = 5 = 10"
        self.assertIsNone(tokenize(userInput))

    def test_variable_not_defined(self):
        userInput = "x = y"
        self.assertIsNone(tokenize(userInput))

    def test_convert_numbers(self):
        userInput = "x = 10 + 5.5"
        expected_tokens = ['x', '=', 10, '+', 5, 5]
        self.assertEqual(tokenize(userInput), expected_tokens)

class TestEvaluateTokens(unittest.TestCase):
    def setUp(self):
        self.variables = Variables.get_instance()

    def tearDown(self):
        self.variables.clear()

    def test_empty_expression(self):
        tokens = []
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

    def test_single_value_expression(self):
        tokens = [5]
        result = evaluate_tokens(tokens)
        self.assertEqual(result, 5)

    def test_variable_assignment(self):
        tokens = ['x', '=', 5]
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)
        self.assertEqual(self.variables.get('x'), 5)

    def test_invalid_syntax(self):
        tokens = ['-', '+']
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

    def test_parenthesized_expression(self):
        tokens = ['(', 5, '+', 2, ')']
        result = evaluate_tokens(tokens)
        self.assertEqual(result, 7)

    def test_invalid_parentheses(self):
        tokens = ['(', 5, '+', 2]
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

    def test_invalid_assignment(self):
        tokens = ['x', '=', 5, '=', 10]
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

    def test_invalid_token(self):
        tokens = ['x', '=', 'y']
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

    def test_valid_expression(self):
        tokens = ['x', '=', 5, '+', '(', 4, '-', 2, ')']
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)
        self.assertEqual(self.variables.get('x'), 7)

    def test_invalid_operator(self):
        tokens = [5, '*', 2]
        result = evaluate_tokens(tokens)
        self.assertIsNone(result)

class TestMain(unittest.TestCase):
    def setUp(self):
        self.variables = Variables.get_instance()

    def tearDown(self):
        self.variables.clear()

    def test_integration(self):
        inputs = [
            "3 + 5 - -2 - 2",
            "x = 3 + 5 - -2 - 2",
            "y = x - (x - 2)",
            "y",
            "ans = (17 - (5 - 20)) - (1 - 11)",
            "ans",
            "",
            "ans = ans - (-42 - ans)",
            "ans",
            "(17-(5-20))-(1-11)"
        ]
        expected_outputs = [
            "8",
            "",
            "",
            "2",
            "",
            "42",
            "",
            "126",
            "42"
        ]

        with patch('builtins.input', side_effect=inputs), patch('sys.stdout', new=StringIO()) as fake_output:
            main()

            output_lines = fake_output.getvalue().strip().split('\n')
            self.assertEqual(len(output_lines), len(expected_outputs))

            for i in range(len(output_lines)):
                self.assertEqual(output_lines[i], expected_outputs[i])

if __name__ == '__main__':
    unittest.main()