import argparse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def s3_upload_download(file_path, bucket_name, s3_key, operation="upload"):
    """
    Function to upload or download a file from a specified S3 bucket.

    :param file_path: Local file path for upload or download.
    :param bucket_name: Name of the S3 bucket.
    :param s3_key: Key (path) in the S3 bucket.
    :param operation: Operation to perform ("upload" or "download").
    :return: None
    """
    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        if operation.lower() == "upload":
            s3.upload_file(file_path, bucket_name, s3_key)
            print(f"File {file_path} uploaded to s3://{bucket_name}/{s3_key}")

        elif operation.lower() == "download":
            s3.download_file(bucket_name, s3_key, file_path)
            print(f"File s3://{bucket_name}/{s3_key} downloaded to {file_path}")

        else:
            print("Invalid operation. Please specify 'upload' or 'download'.")

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")

    except NoCredentialsError:
        print("Error: AWS credentials not available.")

    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials configuration.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Upload or download files to/from an S3 bucket.")
    parser.add_argument("--type", required=True, choices=["upload", "download"], help="Operation type: 'upload' or 'download'.")
    parser.add_argument("--bucket_name", required=True, help="Name of the S3 bucket.")
    parser.add_argument("--file_path", required=True, help="Local file path for upload or download.")
    parser.add_argument("--s3_key", required=True, help="Key (path) in the S3 bucket.")

    args = parser.parse_args()

    # Perform the specified operation
    s3_upload_download(file_path=args.file_path, 
                       bucket_name=args.bucket_name, 
                       s3_key=args.s3_key, 
                       operation=args.type)
