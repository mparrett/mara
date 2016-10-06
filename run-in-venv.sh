#!/bin/bash

# Allow script to be run from any directory
DIR="$( cd "$( dirname $(readlink -f "${BASH_SOURCE[0]}") )" && pwd -P )"

if [ ! -e "$DIR/$1/bin/activate" ]; then
	echo "Virtual env $DIR/$1 does not exist"
	exit 1
fi

# Import environment variables
if [ -e "$DIR/.env" ]; then
	echo "Loading environment $DIR/.env"
	source $DIR/.env
else
	echo "WARNING: Environment not loaded. This is likely going to cause problems!"
fi

# Activate the virtualenv
source $DIR/$1/bin/activate

shift

echo "Running $@"
echo ""

$@

# Deactivate the virtualenv
deactivate
