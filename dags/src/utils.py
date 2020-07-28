import boto3
from datetime import datetime, timezone
from src.authorization import AWSClient
import requests


def download_s3_file(bucketname, filename, output_path):
    client_obj = AWSClient()
    aws_session = client_obj.aws_session
    s3 = aws_session.resource('s3')
    obj = s3.Object(bucketname, filename)
    body = obj.get()['Body'].read()
    body = body.decode('utf-8')
    with open(output_path, 'w') as f:
        f.writelines(str(body))

    f.close()


def save_to_s3(data, s3_bucket_name, filepath, data_name=None,
               for_quicksight=False):
    try:
        if for_quicksight:
            path = 's3://'+s3_bucket_name+'/'+filepath
            data.coalesce(1).write.csv(path, header=True, mode='overwrite')
        else:
            now = datetime.now(
                timezone.utc)  # Timezone-aware datetime.utcnow()
            today = datetime(now.year, now.month, now.day,
                             tzinfo=timezone.utc).strftime('%Y-%m-%d')
            path = filepath + data_name + "-" + str(today) + ".xlsx"
            s3 = boto3.resource('s3')
            fileobj = s3.Object(s3_bucket_name, path)
            fileobj.put(Body=data)
            print(data_name + " saved to: " + path)
        return path
    except Exception as e:
        print("Error occurred while saving EIA data to S3: " + str(e))
        return None


def get_eia_production(s3_bucket_name, filepath):
    """
    read the data into dataframe and save each to an excel file on S3
    return the summary dataframe
    """
    aws_client = AWSClient()
    aws_session = aws_client.aws_session
    s3_filepaths = []
    for stream in ['oil', 'gas']:
        url = "https://www.eia.gov/petroleum/production/xls/comp-stat-" + stream + ".xlsx"
        print("Fetching excel file from: " + url)
        now = datetime.now(timezone.utc)  # Timezone-aware datetime.utcnow()
        today = datetime(now.year, now.month, now.day,
                         tzinfo=timezone.utc).strftime('%Y-%m-%d')
        path = filepath + "eia-" + stream + "-" + str(today) + ".xlsx"

        request = requests.get(url)
        if request.status_code == 200:
            excel_file = request.content
        else:
            print("Unable to fetch EIA file from URL: " + url)
            return None, None

        try:
            s3 = aws_session.resource('s3')
            fileobj = s3.Object(s3_bucket_name, path)
            fileobj.put(Body=excel_file)
            print("EIA Data saved to: " + path)
        except Exception as e:
            print("Error occurred while saving EIA data to S3: " + str(e))
        s3_filepaths.append(path)
    return s3_filepaths
