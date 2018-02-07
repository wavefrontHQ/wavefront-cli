#!/bin/bash

INSTALL_LOG=`mktemp /tmp/install_wavefront_XXXXXXXXXX.log`

function check_if_root_or_die() {
    echo "Checking installation privileges"
    echo -e "\nid -u" >>${INSTALL_LOG}
    SCRIPT_UID=$(id -u)
    if [ "$SCRIPT_UID" != 0 ]; then
        echo  "Installer should be run as root"
        exit 1
    fi
}

function exit_with_message() {
    echo
    echo $1
    echo -e "\n$1" >>  ${INSTALL_LOG}
    if [[ $INSTALL_LOG && "$2" -eq 1 ]]; then
        echo "For additional information, check the Wavefront install log: $INSTALL_LOG"
    fi
    echo
    exit 1
}

function echo_right() {
    TEXT=$1
    echo
    tput cuu1
    tput cuf $(tput cols)
    tput cub ${#TEXT}
    echo $TEXT
}

function echo_failure() {
    tput setaf 1  # 1 = red
    echo_right "[ FAILED ]"
    tput sgr0  # reset terminal
}

function exit_with_failure() {
    echo_failure
    exit_with_message "FAILURE: $1" 1
}

function detect_operating_system() {

    echo "Detecting operating system:"
    if [ -f /etc/debian_version ]; then
        echo -e "\ntest -f /etc/debian_version" >> ${INSTALL_LOG}
        echo "Debian/Ubuntu"
        OPERATING_SYSTEM="DEBIAN"
    elif [ -f /etc/redhat-release ] || [ -f /etc/system-release-cpe ]; then
        echo -e "\ntest -f /etc/redhat-release || test -f /etc/system-release-cpe" >> ${INSTALL_LOG}
        echo "RedHat/CentOS"
        OPERATING_SYSTEM="REDHAT"
    elif [ "$(uname)" == "Darwin" ]; then
        OPERATING_SYSTEM="MAC"
        echo "Mac is not yet supported!"
        exit 1
    elif [ -f /etc/SUSE-brand ]; then
        echo -e "\ntest -f /etc/SUSE-brand" >> ${INSTALL_LOG}
        echo "OpenSUSE/SLE"
        OPERATING_SYSTEM=`head -1 /etc/SUSE-brand`
    else
        echo -e "\ntest -f /etc/debian_version" >> "/tmp/wavefront_install.log"
        echo -e "\ntest -f /etc/redhat-release || test -f /etc/system-release-cpe" >> ${INSTALL_LOG}
        echo "Unsupported operating system"
        exit 1
    fi
    export OPERATING_SYSTEM
}

function install_python() {

    if [ $OPERATING_SYSTEM == "DEBIAN" ]; then
        echo "Installing Python using apt-get"
        apt-get update >> ${INSTALL_LOG} 2>&1
        apt-get install python -y >> ${INSTALL_LOG} 2>&1
    elif [ $OPERATING_SYSTEM == "REDHAT" ]; then
        echo "Installing Python using yum"
        yum install python -y >> ${INSTALL_LOG} 2>&1
    elif [ $OPERATING_SYSTEM == "openSUSE" ] || [ $OPERATING_SYSTEM == "SLE" ]; then
        echo "Installing Python using zypper"
        zypper install python >> ${INSTALL_LOG} 2>&1
    fi

    if [ $? -ne 0 ]; then
            exit_with_failure "Failed to install Python"
    fi

}

function remove_python() {

    # wavefront cli
    pip uninstall wavefront-cli -y
    # pip
    pip uninstall pip -y

    # python
    if [ $OPERATING_SYSTEM == "DEBIAN" ]; then
        echo "Uninstalling Python using apt-get"
        apt-get remove python -y &> ${INSTALL_LOG}
        apt-get autoremove -y &> ${INSTALL_LOG}
    elif [ $OPERATING_SYSTEM == "REDHAT" ]; then
        echo "Uninstalling Python using yum"
        yum remove python -y &> ${INSTALL_LOG}
    elif [ $OPERATING_SYSTEM == "openSUSE" ] || [ $OPERATING_SYSTEM == "SLE" ]; then
        echo "Uninstalling Python using zypper"
        zypper remove python &> ${INSTALL_LOG}
    fi

}


function install_pip() {
    $PYTHON_PATH=$(which python) 2> /dev/null
    if [ $OPERATING_SYSTEM == "openSUSE" ]; then
       $PYTHON_PATH=$(which python2.7) 2>/dev/null
    fi
    curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py >> ${INSTALL_LOG} 2>&1
    if [ $? -ne 0 ]; then
            exit_with_failure "Failed to download Pip"
    fi
    $PYTHON_PATH /tmp/get-pip.py >> ${INSTALL_LOG} 2>&1
    if [ $? -ne 0 ]; then
            exit_with_failure "Failed to install Pip"
    fi

    rm -f /tmp/get-pip.py 2> /dev/null
}

function install_wavecli() {
    PIP_PATH=$(which pip)
    $PIP_PATH uninstall wavefront-cli -y >> ${INSTALL_LOG} 2>&1
    $PIP_PATH install wavefront-cli >> ${INSTALL_LOG} 2>&1
    if [ $? -ne 0 ]; then
            exit_with_failure "Failed to install Wavefront CLI"
    fi

    # Find where it was installed
    WAVE_PATH="/usr/local/bin/wave"
    if [ -f "$WAVE_PATH" ]; then
        echo "Wavefront CLI detected in $WAVE_PATH"
    elif [ -f "/usr/bin/wave" ]; then
        echo "Wavefront CLI detected in /usr/bin/wave"
        WAVE_PATH="/usr/bin/wave"
    else
        exit_with_failure "Wavefront CLI not found."
    fi
    export WAVE_PATH

}


# main()

detect_operating_system
check_if_root_or_die

# Detect python
PYTHON_PATH=$(which python)
# If python was not installed before this script runs, uninstall it at the end.
PYTHON_INSTALLED=false

if [ -z "$PYTHON_PATH" ]; then
    echo "Python is not installed. Installing Python."
    echo "Python will be uninstalled automatically after installation finishes."
    PYTHON_INSTALLED=false
    install_python
    PYTHON_PATH=$(which python)
else
    PYTHON_INSTALLED=true
    echo "Python detected in ${PYTHON_PATH}"
fi

# Detect pip
PIP_PATH=$(which pip)
if [ -z "$PIP_PATH" ]; then
    echo "Pip is not installed, installing Pip."
    install_pip
fi

if [ $OPERATING_SYSTEM == "openSUSE" ]; then
    echo "Checking pip version"
    pip_version=`pip --version`
    pip_python_version="python 3"

    if [[ $pip_version == *$pip_python_version* ]]; then
       install_pip
    fi
fi
# Make sure Wavefront CLI is installed. This function will export WAVE_PATH - holds the location of the wavefront cli binary
install_wavecli

# Capture command line args passed to shell script in a string
cli_args=""
for arg in "$@"
do
   cli_args="$cli_args $arg"
done

# Run Cli installation process
$WAVE_PATH $cli_args

# Python was not installed before running this script, so remove it.
if [ $PYTHON_INSTALLED == false ]; then
    remove_python
fi
