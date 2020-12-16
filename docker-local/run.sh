#!/usr/bin/env bash

export JSON_KEY="/src/keys/nimellaa-test.json"
export RAW_DATA_PROJECT_GCP_KEY=$JSON_KEY
export LOG_FILES_PROJECT_GCP_KEY=$JSON_KEY
export GOOGLE_CLOUD_PROJECT_KEY=$JSON_KEY

# Mount serice account key to a location, which has been set as environment variables above.
docker run -v /Users/nancyirisarri/workspaces/pyladies-amsterdam-etl/keys/nimellaa-test.json:/src/keys/nimellaa-test.json \
 -e RAW_DATA_PROJECT_GCP_KEY -e LOG_FILES_PROJECT_GCP_KEY -e GOOGLE_CLOUD_PROJECT_KEY \
 --env-file ./env.list -it pyladies-amsterdam-etl