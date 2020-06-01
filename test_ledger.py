import unittest
import json
from execute_loan import Loan


class TestExecuteLoan(unittest.TestCase):

    def setUp(self):
        self.loan_1 = Loan('test_loan_1', 100, 0.02, '04-01-2020')
        self.loan_2 = Loan('test_loan_2', 200, 0.03, '05-01-2020')

    def tearDown(self):
        pass

    def test_init(self):
        self.assertEqual(self.loan_1.loan_ID, 'test_loan_1')
        self.assertEqual(self.loan_2.loan_ID, 'test_loan_2')
        self.assertEqual(self.loan_1.principal, 100)
        self.assertEqual(self.loan_2.principal, 200)
        self.assertEqual(self.loan_1.interest_rate, 0.02)
        self.assertEqual(self.loan_2.interest_rate, 0.03)
        self.assertEqual(self.loan_1.effective_date, '04-01-2020')
        self.assertEqual(self.loan_2.effective_date, '05-01-2020')
        self.assertEqual(self.loan_1.daily_interest, 0.02/365)
        self.assertEqual(self.loan_2.daily_interest, 0.03/365)

    def test_create_bucket(self):
        with mock.patch('execute_loan.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = 'Success'

            bucket = self.loan_1.create_bucket('test_bucket')
            mocked_get.assert_called_with(
                'http://127.0.0.1:5000/ledger/buckets/?loanId=test_loan_1&identifier=test_bucket')
            self.assertEqual(bucket, 'Success')

            mocked_get.return_value.ok = False

            bucket = self.loan_2.create_bucket('test_bucket_2')
            mocked_get.assert_called_with(
                'http://127.0.0.1:5000/ledger/buckets/?loanId=test_loan_1&identifier=test_bucket_2')
            self.assertEqual(bucket, 'Bad Response!')


if __name__ == '__main__':
    unittest.main()
