# from flask.cli import with_appcontext
import markdown
import os


import shelve


# Import the framework
from flask import Flask, g, current_app, request
from flask_restful import Resource, Api, reqparse


# Create an instance of Flask
app = Flask(__name__)

# Create the Api
api = Api(app)

# Create database


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("ledger.db", writeback=True)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Present Documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the markdown_file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class BucketList(Resource):
    def get(self):
        loanId = request.args['loanId']
        shelf = get_db()
        buckets = []
        keys = list(shelf[loanId])

        print("-"*30)
        print(" ")
        print("LoanID", loanId)
        print("keys", keys)

        for key in keys:
            print('key', key)
            print('shelf[key]', shelf[loanId][key])
            print('='*5)
            print(" ")
            buckets.append(shelf[loanId][key])

        return {'message': 'Success', 'data': buckets}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('loanId', required=True)
        parser.add_argument('identifier', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()
        loanId = args['loanId']
        shelf = get_db()

        if loanId in shelf:
            # temp = shelf[loanId]['buckets']
            # temp.append({"identifier": args['identifier']})
            # shelf[loanId]['buckets'] = temp
            shelf[loanId]['buckets'].append({"identifier": args['identifier']})
        else:
            shelf[loanId] = {'buckets': [], 'balances': {}, 'entries': []}
            # temp = shelf[loanId]['buckets']
            # temp.append({"identifier": args['identifier']})
            # shelf[loanId]['buckets'] = temp
            shelf[loanId]['buckets'].append({"identifier": args['identifier']})
        return{'message': 'Bucket registered',
               'data': shelf[loanId]['buckets']}, 201


class Sum(Resource):
    def get(self, loanId, bucket_ids):
        shelf = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument('loanId', required=True)
        parser.add_argument('bucket_ids', required=True)
        args = parser.parse_args()
        loanId = args['loanId']
        bucket_ids = args['bucket_ids']
        buckets = {}
        # If the bucket_id does not exist in the data store, return a 404 error
        for bucket in bucket_ids:
            if not(bucket in shelf[loanId]['buckets'].values()):
                return {'message': 'Bucket not found', 'data': {}}, 404
            buckets[bucket] = shelf[loanId]['balances'][bucket]
            # buckets[bucket] = sum([x.get('value')
            #                        for x in shelf[loanId] if x.get('bucket_id') == bucket_id])

        return {'message': 'Buckets found', 'data': buckets}, 200


class Entry(Resource):
    def post(self):
        credit = {}
        debit = {}
        parser = reqparse.RequestParser()
        parser.add_argument('loanID', required=True)
        parser.add_argument('createdAt', required=True,
                            help="Effective date should be in format: MM-DD-YYYY")
        parser.add_argument('effectiveDate', required=True,
                            help="Effective date should be in format: MM-DD-YYYY")
        parser.add_argument('creditBucketID', required=True)
        parser.add_argument('value', type=float, required=True)
        parser.add_argument('debitBucketID', required=True)

        args = parser.parse_args()
        credit['createdAt'] = args['createdAt']
        credit['effectiveDate'] = args['effectiveDate']
        credit['bucket_id'] = args['creditBucketID']
        credit['value'] = args['value']

        debit['createdAt'] = args['createdAt']
        debit['effectiveDate'] = args['effectiveDate']
        debit['bucket_id'] = args['debitBucketID']
        debit['value'] = -args['value']

        loanId = args['loanID']
        shelf = get_db()
        shelf[loanId]['entries'] = [credit, debit]

        # If Balance hasn't been created yet, create it
        if shelf[loanId].get('balances') is None:
            shelf[loanId]['balances'] = {
                args['creditBucketID']: args['value'],
                args['debitBucketID']: -args['value']
            }

        # If balance has been created, but not these buckets yet, add them
        elif shelf[loanId]['balances'].get([args['creditBucketID']]) is None:
            shelf[loanId]['balances'][args['creditBucketID']] = args['value']
            shelf[loanId]['balances'][args['debitBucketID']] = -args['value']

        # If these buckets exist, credit/debit the value
        else:
            shelf[loanId]['balances'][args['creditBucketID']] += args['value']
            shelf[loanId]['balances'][args['debitBucketID']] -= args['value']

        return{'message': 'Entry pair registered',
               'data': [credit, debit]}, 201


api.add_resource(BucketList, '/ledger/buckets')
api.add_resource(Sum, '/ledger/buckets/sum')
api.add_resource(Entry, '/ledger/entries')
