# from flask.cli import with_appcontext
import markdown
import os
import shelve

# Import the framework
from flask import Flask, g, current_app
from flask_restful import Resource, Api, reqparse


# Create an instance of Flask
app = Flask(__name__)

# Create the Api
api = Api(app)

# Create database


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("ledger.db")
    return db

# Close db after use
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Show documentation
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
        # parse Arguments
        parser = reqparse.RequestParser()
        parser.add_argument('loanId', required=True)
        args = parser.parse_args()
        loanId = args['loanId']

        shelf = get_db()
        print('shelf', shelf)
        print('-'*22)
        keys = list(filter(lambda loan: loan['loanId'] == loanId, shelf)
        print('keys', keys)
        print('-'*22)


        buckets=[]

        for key in keys:
            print('key', key)
            print('-'*22)
            buckets.append(key.identifier)
        return {'message': 'Success', 'data': buckets}, 200

    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('loanId', required=True)
        parser.add_argument('identifier', required=True)

        # Parse the objects into an object
        args=parser.parse_args()
        loanId=args['loanId']
        shelf=get_db()
        buckets=list(filter(lambda loan: loan['loanId'] == loanId, shelf))
        buckets[args['identifier']]=args

        return{'message': 'Bucket registered', 'data': args}, 201


class Sum(Resource):
    def get(self, loanId, bucket_ids):
        shelf=get_db()

        parser=reqparse.RequestParser()
        parser.add_argument('loanID', required=True)
        parser.add_argument('bucket_ids', required=True)
        buckets={}
        # If the bucket_id does not exist in the data store, return a 404 error
        for bucket_id in bucket_ids:
            if not(bucket_id in shelf):
                return {'message': 'Bucket not found', 'data': {}}, 404

            buckets[bucket_id]=sum([x.get('value')
                                      for x in shelf[loanId] if x.get('bucket_id') == bucket_id])

        return {'message': 'Buckets found', 'data': buckets}, 200


class Entry(Resource):
    def post(self):
        credit={}
        debit={}
        parser=reqparse()
        parser.add_argument('loanId', required=True)
        parser.add_argument('createdAt', required=True,
                            help="Effective date should be in format: MM-DD-YYYY")
        parser.add_argument('effectiveDate', required=True,
                            help="Effective date should be in format: MM-DD-YYYY")
        parser.add_argument('creditBucketID', required=True)
        parser.add_argument('value', type=float, required=True)
        parser.add_argument('debitBucketID', required=True)

        args=parser.parse_args()
        credit['createdAt']=args['createdAt']
        credit['effectiveDate']=args['effectiveDate']
        credit['bucket_id']=args['credit_bucketId']
        credit['value']=args['value']

        debit['createdAt']=args['createdAt']
        debit['effectiveDate']=args['effectiveDate']
        debit['bucket_id']=args['debit_bucketId']
        debit['value']=-args['value']

        shelf=get_db()
        shelf[loanId]['entries']=[credit, debit]

        return{'message': 'Entry pair registered', 'data': [credit, debit]}, 201


api.add_resource(BucketList, '/ledger/buckets')
api.add_resource(Sum, '/ledger/buckets/sum')
api.add_resource(Entry, '/ledger/entries')
