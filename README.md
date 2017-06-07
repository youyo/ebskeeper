# EBS Keeper

- Source zip file is here.

```
https://s3-ap-northeast-1.amazonaws.com/ebskeeper/ebskeeper.zip
```

- Environment variable must be specified, `VOLUME_ID` and `LIFECYCLE` .

```
VOLUME_ID=vol-xxxxxxxxxxxxx
LIFECYCLE=3
```

- Required permission.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:CreateTags",
                "ec2:DescribeTags",
                "ec2:DeleteSnapshot",
                "ec2:DescribeSnapshots",
                "ec2:DescribeInstances"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
