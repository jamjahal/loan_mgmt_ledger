import unittest
import json
from execute_loan import Loan


class TestExecuteLoan(unittest.TestCase):

    def test_init(self):
        test_loan = Loan('test_loan', 100, 0.02, '04-01-2020')
        self.assertEqual(test_loan.loan_ID, 'test_loan')
        self.assertEqual(test_loan.principal, 100)
        self.assertEqual(test_loan.interest_rate, 0.02)
        self.assertEqual(test_loan.effective_date, '04-01-2020')
        self.assertEqual(test_loan.daily_interest, 0.02/365)


if __name__ == '__main__':
    unittest.main()
