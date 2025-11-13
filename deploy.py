# /// script
# dependencies = [
#   "boto3"
# ]
# ///

from pathlib import Path
import uuid
import boto3
import mimetypes

BUCKET = "releases.wagtail.io"
CLOUDFRONT_DISTRIBUTION_ID = "E283SZ5CB4MDM0"

PUBLISH_DIR = Path(__file__).parent / "nightly"


def main():
    s3_client = boto3.client("s3")

    publish_files = list(PUBLISH_DIR.rglob("*.*"))

    uploaded_paths = []

    for file in publish_files:
        path = "nightly/" + str(file.relative_to(PUBLISH_DIR))

        mime_type, _encoding = mimetypes.guess_type(file)

        print("Uploading", path)
        s3_client.upload_file(
            str(file),
            BUCKET,
            path,
            ExtraArgs={"ACL": "public-read", "ContentType": mime_type},
        )
        uploaded_paths.append(path)

    print("Clearing cache")
    boto3.client("cloudfront").create_invalidation(
        DistributionId=CLOUDFRONT_DISTRIBUTION_ID,
        InvalidationBatch={
            "Paths": {
                "Quantity": len(publish_files),
                "Items": [f"/{path}" for path in uploaded_paths],
            },
            "CallerReference": str(uuid.uuid4()),
        },
    )


if __name__ == "__main__":
    main()
