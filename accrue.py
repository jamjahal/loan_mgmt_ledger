from execute_loan import Loan
from datetime import date, timedelta

# Istantiate, originate, and activate a loan effective 60 days ago
a_loan = Loan("XXXX", 1100, 0.08, '03-11-2020')
a_loan.originate()
a_loan.activate()
a_loan.get_buckets()

# the effective date of the loan
start = datetime.strptime(a_loan.effective_date, "%m-%d-%Y")
end = datetime(2020, 5, 11)
delta = end-start
for i in range(delta.days+1):
    day = start + timedelta(days=i)
    a_loan.enter_accrual(createdAt=day.strftime("%m-%d-%Y"))
