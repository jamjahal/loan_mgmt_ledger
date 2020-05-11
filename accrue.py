from execute_loan import Loan
from datetime import date, timedelta


a_loan = Loan("XXXX", 1100, 0.08, '03-11-2020')
print(a_loan.originate())
print(a_loan.activate())
print(a_loan.get_buckets())


effective_date = date(2020, 3, 11)
end_date = date(2020, 5, 11)

delta = end_date-effective_date

for day in range(delta.days + 1):
    a_loan.enter_accrual(createdAt=day)
    print(a_loan.get_balances())
