# Entornos: dónde vive cada skill

GitHub es la **fuente de verdad**: la versión oficial de cada skill está en el repositorio. Cada entorno instala una copia desde ahí.

## Claude Code

- Skills personales (todas las carpetas del usuario): `~/.claude/skills/<nombre>/SKILL.md`
- Skills de un proyecto (se comparten con el repo del proyecto): `<proyecto>/.claude/skills/<nombre>/SKILL.md`

**Cómo guardar:** escribe la carpeta directamente con `new_skill.py --destino ~/.claude/skills` (o `.claude/skills`). Las skills se cargan al iniciar la sesión; si acabas de crearla, puede necesitar una sesión nueva para activarse sola. Mientras tanto, léela y síguela manualmente.

**Cómo instalar desde GitHub:**

```bash
git clone https://github.com/<usuario>/skill-generator.git
cd skill-generator && ./install.sh            # instala todas
./install.sh cp-web-mi-proyecto               # instala una
```

**PROGRESO.md:** en la raíz del proyecto (o en `docs/`), versionado junto al código.

## Claude (app web, escritorio o móvil)

- Claude no puede instalar skills por sí mismo: el usuario las añade.
- Si hay una herramienta para **proponer skills** (muestra una tarjeta de revisión), úsala con el `SKILL.md` completo; el usuario la guarda con un clic.
- Si no, empaqueta con `package_skill.py` y entrega el `.zip` para que el usuario lo suba en la sección de skills de su configuración.
- Si la sesión tiene acceso a GitHub (repositorio conectado), publica ahí también (Paso 7).

**PROGRESO.md:** como archivo del proyecto entregado al usuario o guardado en el repo del proyecto. Si no hay repositorio, entrégalo como archivo al final de cada sesión para que el usuario lo adjunte la próxima vez.

## Detectar el entorno

| Señal | Entorno |
|---|---|
| Existe `~/.claude/` y puedes leer archivos del proyecto del usuario | Claude Code |
| Workspace en la nube, archivos entregados con herramienta de envío, herramientas de artifacts | Claude (app) |
| Duda | Pregunta: "¿Estás usando Claude Code o la app de Claude?" |
