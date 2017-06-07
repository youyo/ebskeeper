#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import boto3
import os
import datetime


class EbsKeeper():
    def __init__(self):
        self.volume_id = os.environ["VOLUME_ID"]
        self.lifecycle = int(os.environ["LIFECYCLE"])
        self.client = boto3.client('ec2')

    def create_snapshot(self):
        description = self.__build_description()
        self.snapshot_id = self.__create_snapshot(description)
        name_tag = list(self.__fetch_name_tag())
        if len(name_tag) != 0:
            self.__create_tag(name_tag[0])
        print('Create snapshot: ' + self.snapshot_id)

    def rotate_snapshots(self):
        while True:
            snapshots = self.__describe_snapshots()
            if len(snapshots) > self.lifecycle:
                snapshot_id = snapshots[0]['SnapshotId']
                self.__delete_snapshot(snapshot_id)
                print('Delete snapshot: ' + snapshot_id)
            else:
                break

    # private
    def __create_snapshot(self, description):
        snapshot_id = self.client.create_snapshot(
            VolumeId=self.volume_id,
            Description=description
        )['SnapshotId']
        return snapshot_id

    def __build_description(self):
        time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        return 'Created by EBS Keeper from %s at %s' % (self.volume_id, time)

    def __fetch_name_tag(self):
        tags = self.client.describe_tags(
            Filters=[{
                'Name': 'resource-id',
                'Values': [self.volume_id]
            }]
        )
        name_tag = map(lambda x: x['Value'], filter(lambda x: x['Key'] == 'Name', tags['Tags']))
        return name_tag

    def __create_tag(self, name_tag):
        self.client.create_tags(
            Resources=[self.snapshot_id],
            Tags=[{
                'Key': 'Name',
                'Value': name_tag,
            }]
        )

    def __describe_snapshots(self):
        snapshots = self.client.describe_snapshots(
            Filters=[{
                'Name': 'volume-id',
                'Values': [self.volume_id]
            }]
        )
        sorted_data = sorted(snapshots['Snapshots'], key=lambda x: x['StartTime'])
        return sorted_data

    def __delete_snapshot(self, snapshot_id):
        self.client.delete_snapshot(
            SnapshotId=snapshot_id
        )


def lambda_handler(event, context):
    ek = EbsKeeper()
    ek.create_snapshot()
    ek.rotate_snapshots()


if __name__ == "__main__":
    lambda_handler({}, {})
