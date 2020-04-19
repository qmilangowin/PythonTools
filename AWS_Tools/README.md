## Repository of Useful tools ##

A collection of some useful tools. Provide description here.


### s3permissions.py ###

Command-line python utility to set the permissions on a specific S3 bucket in
order to enable upload/download.

<em>Usage</em>: 

`s3perms.py -rw -b <bucket-name> -k <AWS-profile>`

where `-rw` specifes to set permissions to read-write, `-b` is the S3 bucket
name and `-k` is the AWS profile as defined in `~/.aws/credentials`. `-k` defaults
to the `default` profile

To disable access and return bucket to private do as above but with following:

`s3perms.py -p -b <bucket-name> -k <AWS-profile>`

<em>Example:</em>

`s3perms.py -rw -b foo -k` will set the bucket `foo` to read-write 
using the default AWS profile whereas:

`s3perms.py -rw -b foo -k bar` will over-write the default setting and set the 
bucket bar to read-write in AWS account linked to the `bar` profile in 
`~/.aws/credentials

---