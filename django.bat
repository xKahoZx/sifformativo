@ECHO OFF
echo "Empezando a sincronizar la base de datos "

IF EXIST "manage.py" (

echo Por Favor Recuerde Iniciar MySQL Xampp.Si ya lo hizo,Haga caso omiso a este mensaje

pause
echo SIncronizando la base de datos 
manage.py syncdb
echo Iniciando el servidor 
manage.py runserver

)ELSE (

echo "Esta es una ruta incorrecta . No existe ningun manage.py
)
pause
exit