#!/bin/bash

echo 'Removing previous distributions...'
rm -r mah 2> /dev/null
echo 'Packaging...'
python setup.py sdist > /dev/null
dist_file=$(ls dist)
echo 'Uploading'
curl -F package=@dist/$dist_file https://PoFnWtvqSTuH2U4FG1wX@push.fury.io/dpalmisano/

