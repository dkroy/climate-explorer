cd ../src
GOOGLE_KEYFILE=YOUR_KEYFILE
GOOGLE_PROJECT=YOUR_PROJECT
gcloud auth activate-service-account --key-file=$GOOGLE_KEYFILE
gcloud config set project $GOOGLE_PROJECT
gcloud app deploy --log-http --verbosity=debug
