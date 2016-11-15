#!/bin/bash

INSTALL_LOG="/tmp/wavefront_install.log"

function check_if_root_or_die() {
    echo "Checking installation privileges"
    echo -e "\nid -u" >>${INSTALL_LOG}
    SCRIPT_UID=$(id -u)
    if [ "$SCRIPT_UID" != 0 ]; then
        echo  "Installer should be run as root"
        exit 1
    fi
}

function detect_operating_system() {

    echo "Detecting operating system"
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
        apt-get install python -y >> ${INSTALL_LOG}
    elif [ $OPERATING_SYSTEM == "REDHAT" ]; then
        echo "Installing Python using yum"
        yum install python -y >> ${INSTALL_LOG}
    fi

}

function remove_python() {
    if [ $OPERATING_SYSTEM == "DEBIAN" ]; then
        echo "Uninstalling Python using apt-get"
        apt-get remove python -y >> ${INSTALL_LOG}
        apt-get autoremove -y >> ${INSTALL_LOG}
    elif [ $OPERATING_SYSTEM == "REDHAT" ]; then
        echo "Installing Python using yum"
        yum remove python -y >> ${INSTALL_LOG}
    fi
}


function install_pip() {
    $PYTHON_PATH=$(which python)
    curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py >> ${INSTALL_LOG}
    $PYTHON_PATH /tmp/get-pip.py >> ${INSTALL_LOG}
}

function install_wavecli() {
    PIP_PATH=$(which pip)
    $PIP_PATH install wavefront-cli --no-cache >> ${INSTALL_LOG}
}


detect_operating_system
check_if_root_or_die

# Detect python
PYTHON_PATH=$(which python)
PYTHON_INSTALLED=false

if [ -z "$PYTHON_PATH" ]; then
    echo "Python is not installed. Installing Python."
    echo "Python will be uninstalled automatically after installtion finishes."
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

# Detect Wavefront CLI
WAVE_PATH=$(which wave)
if [ -z "$WAVE_PATH" ]; then
    echo "Wavefront CLI is not installed. Installing."
    install_wavecli
    WAVE_PATH=$(which wave)
fi


cli_args=""
for arg in "$@"
do
   cli_args="$cli_args $arg"
done

# Run Cli installation process
$WAVE_PATH install $cli_args


if [ $PYTHON_INSTALLED == false ]; then
    remove_python
fi

                                                                                                                                                                                                  125,0-1       Bot
