# Publicación en GitHub (Paso 7)

Repositorio por defecto: `skill-generator` del usuario. Estructura esperada:

```
skill-generator/
├── cp-v1/                 ← esta skill (la fábrica)
├── skills/
│   ├── REGISTRO.md        ← índice de skills generadas
│   └── <nombre>/          ← cada skill generada
├── install.sh
└── README.md
```

## Procedimiento

1. **Validar y escanear** la skill (`validate_skill.py`, `scan_secrets.py`). Sin errores para continuar.
2. **Punto de control 2**: confirmar repo, visibilidad y contenido con el usuario.
3. **Actualizar el repo local** antes de copiar:
   ```bash
   git -C <repo> pull --ff-only
   ```
4. **Copiar** la skill a `skills/<nombre>/` (si ya existe, reemplazar solo esa carpeta).
5. **Registrar**:
   ```bash
   python3 cp-v1/scripts/registry.py agregar --raiz skills --skill skills/<nombre>
   ```
6. **Escanear el repo completo** una vez más: `python3 cp-v1/scripts/scan_secrets.py .`
7. **Commit y push**:
   ```bash
   git add skills/<nombre> skills/REGISTRO.md
   git commit -m "skill(<nombre>): v<version> — <resumen del cambio>"
   git push
   ```
   Si el push es rechazado por cambios remotos: `git pull --rebase` y reintenta una vez. Nunca `--force`.
8. **Informar**: nombre, versión, enlace a la carpeta en GitHub y cómo instalarla.

## Sin acceso a git

Si la sesión no puede hacer push: genera el `.zip` con `package_skill.py`, entrégalo al usuario y explícale que debe subir la carpeta a `skills/<nombre>/` y añadir la línea correspondiente en `skills/REGISTRO.md`.
