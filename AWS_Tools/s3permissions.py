import boto3
import argparse
parser = argparse.ArgumentParser(description='Set Permissions on S3')

def setPermissionsReadWrite(bucket, aws_key):

    try:
        session = boto3.Session(profile_name=aws_key)
        s3 = session.resource('s3')
        bucket_name=s3.BucketAcl(str(bucket))
        response = bucket_name.put(ACL='public-read-write')
        print(response)
    except:
        print('Error: Check your bucket name or ensure you are using the correct profile with AWS')

def setPermissionsPrivate(bucket, aws_key):
    try:
        session = boto3.Session(profile_name=aws_key)
        s3 = session.resource('s3')
        bucket_name=s3.BucketAcl(str(bucket))
        response = bucket_name.put(ACL='private')
        print(response)
    except:
        print('Error: Check your bucket name or ensure you are using the correct profile with AWS')

def main():

    parser.add_argument('-rw',dest='rw',nargs='?',help="Sets bucket to Read-Write mode", type=str,const=True)
    parser.add_argument('-b', metavar='<str>',type=str, required=True, dest='bucket', help='Bucket Name')
    parser.add_argument('-p',dest='prv',nargs='?',help="Makes bucket private",type=str, const=True)
    parser.add_argument('-k',dest='aws_key',nargs='?',help="Specify you AWS key. Defaults to Default. See ~./aws/credentials file for moe info",type=str, const='default', required=True)
    args=parser.parse_args()

    read_write = args.rw
    bucket_name = args.bucket
    private = args.prv
    aws_key = str(args.aws_key)
    if bucket_name != None and read_write != None:
        setPermissionsReadWrite(bucket_name,aws_key)
    elif bucket_name != None and private != None:
        setPermissionsPrivate(bucket_name,aws_key)
    else:
        print("Error: s3.py -h or s3.py --help for usage")

if __name__ == '__main__':
    main()
