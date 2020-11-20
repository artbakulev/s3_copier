import os
from configparser import ConfigParser
import glob
from pathlib import Path

import boto3


def upload(config: ConfigParser):
    session = boto3.session.Session()

    client = session.client(
        service_name='s3',
        aws_access_key_id=config['destination'].get('access_key'),
        aws_secret_access_key=config['destination'].get('secret_access_key'),
        region_name=config['destination'].get('region_name'),
        endpoint_url=config['destination'].get('endpoint_url'),
    )

    bucket_name = config['destination'].get('bucket_name')
    files = glob.iglob(config['default'].get('data_folder_name') + '**/**',
                       recursive=True)
    files = [Path(filename) for filename in files]
    files = list(filter(lambda x: x.is_file(), files))
    for i, path in enumerate(files):
        print(f'{i+1}/{len(files)} files uploaded')
        bucket_filename = os.path.join(*path.parts[1:])
        path = str(path)
        client.upload_file(path, bucket_name, bucket_filename)
