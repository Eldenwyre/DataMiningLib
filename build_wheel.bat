python .\setup.py bdist_wheel

SET /P response= Update currently installed version? (Y/N)
GOTO :input_check

:input_check
IF "%response%"=="Y" GOTO :update_wheel
IF "%response%"=="N" GOTO :end
SET /P response= Please enter Y for yes or N for no
GOTO :input_check

:update_wheel
pushd .\dist
for /f "tokens=*" %%a in ('dir /b /od') do set latest=%%a
pip install %latest% --upgrade
GOTO :end

:end
echo exiting script...