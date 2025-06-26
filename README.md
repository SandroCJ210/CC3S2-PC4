# CC3S2-PC4

### Git Hooks

Ejecuta el siguiente script para instalar los hooks en tu entorno local
```bash
bash setup-hooks.sh
```
Este script configura automáticamente dos hooks personalizados:

- pre-commit: se ejecuta antes de que un commit se registre, para validar el formato del mensaje.

- pre-push: se ejecuta antes de hacer un git push y revisa que todos los commits pendientes por subir cumplan con el formato.