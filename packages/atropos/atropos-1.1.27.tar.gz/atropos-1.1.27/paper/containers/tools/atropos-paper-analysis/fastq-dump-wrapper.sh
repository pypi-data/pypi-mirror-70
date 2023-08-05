#!/usr/bin/env bash
set -e

# Fix ownership of output files
finish() {
    # Fix ownership of output files
    user_id=$(stat -c '%u:%g' /data)
    chown -R ${user_id} /data
}
trap finish EXIT

# Call tool with parameters
./../opt/fastq-dump/sratoolkit.2.8.2-1-ubuntu64/bin/fastq-dump "$@"
