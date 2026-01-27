# This script is designed to install the Microsoft ODBC driver for SQL Server (msodbcsql17)
# on supported versions of Ubuntu. It performs the following steps:
#
# 1. Checks if the current version of Ubuntu is one of the supported versions (16.04, 18.04, 20.04, 22.04).
#    If it's not a supported version, the script will output a message indicating the lack of support
#    and then exit without making any changes.
#
# 2. Elevates privileges to root, which is necessary for installing system-wide packages.
#
# 3. Adds the Microsoft repository GPG key to the system's trusted keys. This is required to authenticate
#    the packages that will be downloaded from the Microsoft repository.
#
# 4. Configures the package manager to use Microsoft's Ubuntu repository by downloading the repository
#    configuration file and placing it in the apt sources list directory.
#
# 5. Exits the root shell. The change to root privileges should be done with caution, and the script
#    returns to the normal user as soon as the task requiring root access is complete.
#
# 6. Runs an apt-get update to refresh the package lists with the newly added Microsoft repository.
#
# 7. Installs the 'msodbcsql17' package, which contains the Microsoft ODBC driver for SQL Server.
#    The 'ACCEPT_EULA=Y' environment variable is set to automatically accept the EULA (End-User License Agreement).
#
# 8. Optionally installs the 'mssql-tools' package, which contains command-line tools for SQL Server such as
#    bcp and sqlcmd. The acceptance of the EULA is also handled automatically.
#
# 9. Adds the path to the installed mssql-tools to the system's PATH variable, and updates the current shell
#    environment to include it by sourcing the user's .bashrc file.
#
# 10. Optionally installs the 'unixodbc-dev' package, which contains the development headers for unixODBC.
#     These are often needed to compile other applications that use ODBC to connect to databases.
#
# Please note: This script must be run with appropriate permissions to install software and edit system configuration files.


if ! [[ "16.04 18.04 20.04 22.04" == *"$(lsb_release -rs)"* ]];
then
    echo "Ubuntu $(lsb_release -rs) is not currently supported.";
    exit;
fi

sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

exit
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev