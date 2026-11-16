@REM ----------------------------------------------------------------------------
@REM Apache Maven Wrapper Batch Script
@REM ----------------------------------------------------------------------------

@echo off
@setlocal

set ERROR_CODE=0
@set "BASE_DIR=%~dp0"

@REM Si mvn está instalado globalmente, usarlo directamente
where mvn >nul 2>nul
if %ERRORLEVEL% equ 0 (
  mvn %*
  goto end
)

@REM Resolve JAVA_HOME
set "JAVACMD=java.exe"
if not "%JAVA_HOME%" == "" (
  if exist "%JAVA_HOME%\bin\java.exe" (
    set "JAVACMD=%JAVA_HOME%\bin\java.exe"
  )
)

set "WRAPPER_JAR=%BASE_DIR%\.mvn\wrapper\maven-wrapper.jar"
set "WRAPPER_LAUNCHER=org.apache.maven.wrapper.MavenWrapperMain"

"%JAVACMD%" %MAVEN_OPTS% -classpath "%WRAPPER_JAR%" "-Dmaven.multiModuleProjectDirectory=%BASE_DIR%" %WRAPPER_LAUNCHER% %*
if ERRORLEVEL 1 goto error
goto end

:error
set ERROR_CODE=1

:end
@endlocal & set ERROR_CODE=%ERROR_CODE%
cmd /C exit /B %ERROR_CODE%
