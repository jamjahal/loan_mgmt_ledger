from datetime import date
import requests

base_url = "http://127.0.0.1:5000"


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

    # Originate the loan
    def originate(self):
        self.create_bucket('future-receivable-principal')
        self.create_bucket('loan-commitment-liability')
        self.make_entry("future-receivable-principal", "loan-commitment-liability", self.principal)

    # Activate the loan
    def activate(self):
        self.make_entry(creditBucketID="future-receivable-principal",
                        debitBucketID="loan-commitment-liability",
                        value=self.principal)
        self.make_entry(creditBucketID="cash",
                        debitBucketID="accounts-receivable-principal",
                        value=self.principal)

    # Make an entry pair
    def make_entry(self, creditBucketID, debitBucketID, value, createdAt=date.today().strftime("%m-%d-%Y")):
        """
        Makes an entry pair for both credit and debit.

        creditBucketID: String
            Name of the bucket for credit
        debitBucketID: string
            Name of the bucket for debit
        value: float
            value of loan or interest
        createdAt: string of date formatted as MM-DD-YYYY
            default is day of entry, but can retroactively enter dates manually with properly formatted string.

        """

        url = base_url+'/ledger/entries'
        if debitBucketID not in self.get_buckets():
            self.create_bucket(creditBucketID)
            self.create_bucket(debitBucketID)
        params = {
            "loanID": self.loan_ID,
            "createdAt": createdAt,
            "effectiveDate": self.effective_date,
            "creditBucketID": creditBucketID,
            "debitBucketID": debitBucketID,
            "value": value
        }
        res = requests.post(url=url, params=params)
        return res.text

    # view all buckets belonging to loan
    def get_buckets(self):
        url = base_url+'/ledger/buckets'
        params = {"loanId": self.loan_ID}
        res = requests.get(url=url, params=params)

        return res.text

    # Enter accrual of interest
    def enter_accrual(self, createdAt=date.today().strftime("%m-%d-%Y")):
        """
        Loan name is a variable of class Loan

        createdAt: string of date formatted as MM-DD-YYYY
            default is day of entry, but can retroactively enter dates manually with properly formatted string.

        """
        if "income-interest" not in self.get_buckets():
            self.create_bucket('accounts_receivable_interest')
            self.create_bucket('income-interest')
        url = base_url+'/ledger/entries'
        params = {
            "loanID": self.loan_ID,
            "createdAt": createdAt,
            "effectiveDate": self.effective_date,
            "creditBucketID": 'income-interest',
            "debitBucketID": "accounts-receivable-interest",
            "value": self.principal*self.daily_interest
        }
        res = requests.post(url=url, params=params)
        return res.text

    # create buckets
    def create_bucket(self, bucket_name):

        url = base_url+'/ledger/buckets'
        params = {'loanId': self.loan_ID, 'identifier': bucket_name}
        res = requests.post(url=url, params=params)
        return res.text

    # get sums
    def get_balances(self):
        url = base_url+'/ledger/buckets/sum'
        params = {"loanId": self.loan_ID,
                  "bucket_ids": self.get_buckets()}
        res = requests.get(url=url, params=params)
        return res.text


a_loan = Loan("abcd", 1100, 0.08, '03-11-2020')
print('principal', a_loan.principal)
print('ID', a_loan.loan_ID)
print('originate', a_loan.originate())
a_loan.originate()
a_loan.activate()
# print(a_loan.activate())
a_loan.create_bucket('brand_new_bucket')
print('get-buckets:', a_loan.get_buckets())
buckets = a_loan.get_buckets()
print('buckets', buckets)
