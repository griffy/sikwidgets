#!/bin/sh

# Must have Java 6 installed as 'java'

# Assumes sikuli has been installed in /opt/sikuli-ide by default
# if the path is not defined
if [ -z $SIKULI_HOME ]; then
  SIKULI_HOME="/opt/sikuli-ide"
fi

# Create some directories we'll need inside our Sikuli installation 
# for installing Jython packages
mkdir -p $SIKULI_HOME/Lib/site-packages
mkdir $SIKULI_HOME/bin

# Download and install setuptools into Jython 2.5 (default Sikuli version)
wget http://peak.telecommunity.com/dist/ez_setup.py
java -cp $SIKULI_HOME/sikuli-script.jar org.python.util.jython -Dpython.executable="ez_setup.py" ez_setup.py
rm ez_setup.py

# Install sikwidgets using setuptools
cd ..
java -cp $SIKULI_HOME/sikuli-script.jar org.python.util.jython -Dpython.executable="setup.py" setup.py install

# Make the script executable
chmod +x $SIKULI_HOME/bin/sikwidgets

# Create a shell script to add it to the path
echo -e 'if [ -z $SIKULI_HOME ]; then\n\tSIKULI_HOME="/opt/sikuli-ide"\nfi\nexport PATH=$PATH:$SIKULI_HOME/bin\n' > /etc/profile.d/sikwidgets.sh
chmod +x /etc/profile.d/sikwidgets.sh

# Run it
source /etc/profile.d/sikwidgets.sh