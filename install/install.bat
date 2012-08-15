set JAVA_EXE="C:\Program Files\Java\jre6\bin\java.exe"
if defined PROGRAMFILES(X86) set JAVA_EXE="%PROGRAMFILES(X86)%\Java\jre6\bin\java.exe"

:: Remove previous installs
rd /S /Q "%SIKULI_HOME%\Lib"
rd /S /Q "%SIKULI_HOME%\bin"

:: Create some directories we'll need inside our Sikuli installation 
:: for installing Jython packages
md "%SIKULI_HOME%\Lib"
md "%SIKULI_HOME%\Lib\site-packages"
md "%SIKULI_HOME%\bin"

:: Download and install setuptools into Jython 2.5 (default Sikuli version)
cscript.exe download-ez_setup.vbs
%JAVA_EXE% -cp "%SIKULI_HOME%\sikuli-script.jar" org.python.util.jython -Dpython.executable="ez_setup.py" ez_setup.py
del ez_setup.py

:: Remove any previous builds of sikwidgets
cd ..
rd /S /Q sikwidgets.egg-info
rd /S /Q build
rd /S /Q dist

:: Install sikwidgets using setuptools
%JAVA_EXE% -cp "%SIKULI_HOME%\sikuli-script.jar" org.python.util.jython -Dpython.executable="setup.py" setup.py install

:: Add our scripts to the path
:: http://stackoverflow.com/questions/1156723/permanently-altering-a-users-path-via-batch-or-python
:: http://www.codeproject.com/Articles/12153/SetEnv
cd install
SetEnv.exe -a PATH %%"%SIKULI_HOME%\bin"
SetEnv.exe -a PATH %%"%SIKULI_HOME%\libs"
