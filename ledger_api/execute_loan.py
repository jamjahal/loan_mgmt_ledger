"""

You can use in-memory storage or a database (I recommend an in-memory storage as it would be quicker to iterate) so that you can start the server and then run a script that will execute the following:


- Create all relevant buckets.

- Create the loan by adding ledger entries for a new loan with the amount/principal of $1100. This would implement “Origination of Loan”.
Activate the loan by adding the ledger entries specified in “Activation of the Loan”

- Accrue daily interest (see above “Loan details for testing” for all the details) for 60 days, booking the interest daily using the above API as specified in “Daily Interest Accrual”

- Return the balance of the principal and the sum of all interest accrued using the above API.

Make sure to document the code and write functional unit tests that can show these APIs as expected.
"""
# Create loan

from datetime import date
import requests


class Loan:

    def __init__(self, loan_ID, value, interest_rate, effective_date):
        """
        loan_ID : string
            Globally unique identifier
        value: float
            Numeric value of principal amount of loanID
        interest_rate: float
            Annual interest rate as decimal.  ex: 8% is entered as 0.08
        effective_date: string
            String of effective_date, formatted as MM-DD-YYYY

        """

        self.loan_ID = loan_ID
        self.principal = value
        self.interest_rate = interest_rate
        self.daily_interest = interest_rate/365
        self.effective_date = effective_date

    def originate(self):
        self.create_bucket('future-receivable-principal')
        self.create_bucket('loan-commitment-liability')
        self.make_entry("future-receivable-principal", "loan-commitment-liability", self.principal)

    def activate(self):
        self.make_entry(creditBucketID="future-receivable-principal",
                        debitBucketID="loan-commitment-liability",
                        value=self.principal)
        self.make_entry(creditBucketID="cash",
                        debitBucketID="accounts-receivable-principal",
                        value=self.principal)

    def make_entry(self, creditBucketID, debitBucketID, value):
        url = 'localhost:5000/ledger/entries'
        if debitBucketID not in self.get_buckets():
            self.create_bucket(creditBucketID)
            self.create_bucket(debitBucketID)

        params = {
            "loanID": self.loan_ID,
            "createdAt": date.today().strftime("%m-%d-%Y"),
            "effectiveDate": self.effective_date,
            "creditBucketID": creditBucketID,
            "debitBucketID": debitBucketID,
            "value": value
        }
        res = requests.get(url=url, params=params)
        return res.text()

    # view all buckets belonging to loan
    def get_buckets(self):
        url = 'localhost:5000/ledger/buckets'
        params = {"loan_ID": self.loan_ID}
        res = requests.get(url=url, params=params)
        return res.text().get('data')

    def enter_accrual(self):
        """
        Loan name is a variable of class Loan
        """
        if "income-interest" not in self.get_buckets():
            self.create_bucket('accounts_receivable_interest')
            self.create_bucket('income-interest')
        url = 'localhost:5000/ledger/entries'
        params = {
            "loanID": self.loan_ID,
            "createdAt": date.today().strftime("%m-%d-%Y"),
            "effectiveDate": self.effective_date,
            "creditBucketID": 'income-interest',
            "debitBucketID": "accounts-receivable-interest",
            "value": self.principal*self.daily_interest
        }
        res = requests.post(url=url, params=params)
        return res.text()


# create buckets

    def create_bucket(self, bucket_name):

        url = 'localhost:5000/ledger/buckets'
        params = {'loan_ID': self.loan_ID, 'identifier': bucket_name}
        res = requests.get(url=url, params=params)
        return res.text()

    # get sums
    def get_balances(self):
        url = 'localhost:5000/ledger/buckets/sum'
        params = {
            "loan_ID": self.loan_ID,
            "bucket_ids": self.get_buckets()
        }
        res = requests.get(url=url, params=params)
        return res.text()


a_loan = Loan("jil", 1100, 0.08, '03-11-2020')
print(a_loan.originate())
print(a_loan.activate())
print(a_loan.get_buckets())
