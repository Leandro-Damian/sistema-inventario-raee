Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

' Obtiene la carpeta donde esta guardado este archivo .vbs
carpeta = fso.GetParentFolderName(WScript.ScriptFullName)
shell.CurrentDirectory = carpeta

' Verifica si el puerto 8000 ya esta en uso para no abrir el servidor dos veces
cmdCheck = "powershell -NoProfile -WindowStyle Hidden -Command ""if (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"""
puertoActivo = shell.Run(cmdCheck, 0, True)

If puertoActivo <> 0 Then
    ' Arranca el servidor en segundo plano con ventana totalmente oculta (0)
    shell.Run "cmd /c """ & carpeta & "\iniciar.bat""", 0, False
    ' Espera 3 segundos a que Uvicorn termine de levantar
    WScript.Sleep 3000
End If

' Abre el sistema en el navegador predeterminado
shell.Run "http://localhost:8000", 1, False