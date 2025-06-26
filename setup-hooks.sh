#!/bin/bash

# copiar el hook commit-msg y el hook pre-push al directorio de hooks de git
cp hooks/commit-msg.sh .git/hooks/commit-msg
cp hooks/pre-push.sh .git/hooks/pre-push

# asignar permisos de ejecución a ambos hooks 
chmod +x .git/hooks/commit-msg .git/hooks/pre-push