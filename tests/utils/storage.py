def build_blob_name(bucket_dir_name, blob_basename):
    return f'{bucket_dir_name}/{blob_basename}'


def upload_file_to_gs(bucket, bucket_dir_name, blob_basename, local_file_path):
    blob_name = build_blob_name(bucket_dir_name, blob_basename)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file_path)


def upload_string_to_gs(bucket, bucket_dir_name, blob_basename, string):
    blob_name = build_blob_name(bucket_dir_name, blob_basename)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(string)
