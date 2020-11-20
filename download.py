import configparser
import os
from pathlib import Path

import boto3


def download(config: configparser.ConfigParser):
    session = boto3.session.Session()

    client = session.client(
        service_name='s3',
        aws_access_key_id=config['source'].get('access_key'),
        aws_secret_access_key=config['source'].get('secret_access_key'),
        region_name=config['source'].get('region_name'),
        endpoint_url=config['source'].get('endpoint_url'),
    )

    paginator = client.get_paginator("list_objects_v2")
    bucket_name = config['source']['bucket_name']
    pages = paginator.paginate(
        Bucket=bucket_name
    )

    default_data_folder = config['default']['data_folder_name']
    for page in pages:
        for i, obj in enumerate(page["Contents"]):
            print(f'{i+1}/{len(page["Contents"])} files downloaded')
            file_key = obj["Key"]
            path = Path(file_key)
            directory = os.path.join(default_data_folder, path.parent)
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = os.path.join(default_data_folder, file_key)
            with open(filename, 'w'):
                client.download_file(bucket_name, file_key, filename)
