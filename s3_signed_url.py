#!/usr/bin/env python

"""
A script to generate a pre-signed URL for an object in a private S3 bucket.
"""

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
import ConfigParser
import argparse
import sys
from os.path import expanduser


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-b', '--bucket', help="The bucket name", required=True)
    parser.add_argument('-o', '--object', help="The object URI", required=True)
    parser.add_argument('-e', '--expires-in', type=int, nargs='?', dest="expires_in", help="How long the signed URL will be valid")
    parser.add_argument('-a', '--access-key', nargs='?', dest="access_key", default=None)
    parser.add_argument('-s', '--secret-key', nargs='?', dest="secret_key", default=None)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    bucket = args.bucket
    key = args.object
    if args.expires_in:
        seconds = args.expires_in
    else:
        seconds = 60*60

    if args.access_key and args.secret_key:
        access_key = args.access_key
        secret_key = args.secret_key
    elif len([x for x in (args.access_key, args.secret_key) if x is not None]) == 1:
        parser.error('--access-key and --secret-key must be given together')
    else:
        config = ConfigParser.ConfigParser()
        config.read(expanduser("~/.boto"))
        if config.has_option('Credentials', 'aws_access_key_id') and config.has_option('Credentials', 'aws_secret_access_key'):
            access_key = config.get('Credentials', 'aws_access_key_id')
            secret_key = config.get('Credentials', 'aws_secret_access_key')
        else:
            config.read(expanduser("~/.s3cfg"))
            if config.has_option('default', 'access_key') and config.has_option('default', 'secret_key'):
                access_key = config.get('default', 'access_key')
                secret_key = config.get('default', 'secret_key')
            else:
                print("You have to specify access_key and secret_key on the command line or in the ~/.boto, ~/.s3cfg.")
                sys.exit(1)

    conn = S3Connection(aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    try:
        buckets = conn.get_all_buckets()
    except S3ResponseError as e:
        print(e.message)
        sys.exit(1)

    if conn.lookup(bucket) is None:
        print('No such bucket!')
        sys.exit(1)
    else:
        if conn.get_bucket(bucket).get_key(key) is None:
            print('The key "{0}" does not exist'.format(key))
            sys.exit(1)
        else:
            print conn.generate_url(
                    seconds,
                    'GET',
                    bucket,
                    key,
                    response_headers = {
                        'response-content-type': 'application/octet-stream'
                    })


if __name__ == "__main__":
    main()
