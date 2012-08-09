set JAVA_EXE="C:\Program Files\Java\jre6\bin\java.exe"
if defined PROGRAMFILES(X86) set JAVA_EXE="%PROGRAMFILES(X86)%\Java\jre6\bin\java.exe"

:: Create some directories we'll need inside our Sikuli installation 
:: for installing Jython packages
md "%SIKULI_HOME%\Lib"
md "%SIKULI_HOME%\Lib\site-packages"
md "%SIKULI_HOME%\bin"

:: Download and install setuptools into Jython 2.5 (default Sikuli version)
cscript.exe download-ez_setup.vbs
%JAVA_EXE% -cp "%SIKULI_HOME%\sikuli-script.jar" org.python.util.jython -Dpython.executable="ez_setup.py" ez_setup.py
del ez_setup.py

:: Install sikwidgets using setuptools
cd ..
%JAVA_EXE% -cp "%SIKULI_HOME%\sikuli-script.jar" org.python.util.jython -Dpython.executable="setup.py" setup.py install

:: Add our scripts to the path
setx PATH "%SIKULI_HOME%\bin;%path%;"