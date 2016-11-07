

# Detect python
PYTHON_PATH=$(which python)
echo $PYTHON_PATH

if [ -z "$PYTHON_PATH" ]; then
    echo "ERROR: Python is not installed. Please install python before running this script."
    exit 1
fi

# Detect pip
PIP_PATH=$(which pip)
if [ -z "$PIP_PATH" ]; then
    echo "Pip is not installed, installing Pip."
    curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
    $PYTHON_PATH /tmp/get-pip.py
fi

# Install Wavefront CLI
pip install wavefront-cli --no-cache


cli_args=""
for arg in "$@"
do
   cli_args="$cli_args $arg"
done

echo $cli_args

# Run Cli installation process
/usr/local/bin/wave oli $cli_args

