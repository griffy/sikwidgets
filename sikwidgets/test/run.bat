:: We must use Java 6, 32-bit
set JAVA_EXE="C:\Program Files\Java\jre6\bin\java.exe"
if defined PROGRAMFILES(X86) set JAVA_EXE="%PROGRAMFILES(X86)%\Java\jre6\bin\java.exe"

%JAVA_EXE% -cp "%SIKULI_HOME%\sikuli-script.jar" org.python.util.jython %1%