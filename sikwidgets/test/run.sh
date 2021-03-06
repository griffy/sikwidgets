#!/bin/sh

# Must have Java 6 installed as 'java'

# Assumes sikuli has been installed in /opt/sikuli-ide by default
# if the path is not defined
if [ -z $SIKULI_HOME ]; then
  SIKULI_HOME="/opt/sikuli-ide"
fi

java -cp "$SIKULI_HOME/sikuli-script.jar" org.python.util.jython $1 