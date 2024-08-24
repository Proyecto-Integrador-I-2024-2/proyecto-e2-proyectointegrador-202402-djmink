# Normas de uso del Repositorio

A continuacion, se presentaran las normas de uso del repositorio a usar en el desarrollo del proyecto.

## Estructura de Ramas

### Ramas Principales

- **'main':** Esta es la rama principal que contiene el código estable y listo para producción. Solo se realizan _merges_ a **'main'** desde la rama **'release'**.

- **'develop':** Utilizada para el desarrollo continuo. Todas las nuevas funcionalidades y correcciones de errores se integran aquí antes de ser liberadas.

### Ramas de Soporte

- **'feature/{nombre_funcionalidad}':** Cada nueva funcionalidad tiene su propia rama que se crea desde **'develop'**. El nombre de la rama debe describir claramente la funcionalidad que se está desarrollando (e.g., **'feature/autenticacion_usuarios'**).

- **'hotfix/{nombre_fallo}':** Ramas para corrección de errores críticos en producción. Se crean desde **'main'** y, una vez corregido, se hace _merge_ tanto a **'main'** como a **'develop'**.

- **'release/{version}':** Preparada para la liberación de una nueva versión. Se crea desde **'develop'** y permite realizar ajustes menores y pruebas antes de la fusión con **'main'**.

## Realizacion de _Commits_

### Formato de los Mensajes de Commit

Cada commit debe seguir una estructura clara y concisa:

**Tipo de cambio:** Describe el tipo de commit. Los tipos comunes incluyen:

- **'feat':** Nueva funcionalidad.

- **'fix':** Correcion de errores.

- **'docs':** Cambios en la documentación.

- **'style':** Cambios de formato, no afecta al código (espacios en blanco, etc.).

- **'refactor':** Refactorización del código sin cambios en la funcionalidad.

- **'test':** Adición o modificación de pruebas.

- **'chore':** Actualización de tareas de construcción o configuraciones.

**Descripcion Breve:** Una breve descripción de lo que hace el commit.

Ejemplo de _commits_:

```vbnet
feat: agregar autenticacion de usuarios
fix: corregir error en el calculo de precios
docs: actualizar README con nueva seccion de instalacion
```

### Reglas para los _Commits_

- **Atomicidad:** Cada _commit_ debe contener un cambio atómico, es decir, un cambio específico y autónomo que pueda describirse en una sola frase.

- **Frecuencia:** Realiza _commits_ frecuentes para mantener un historial claro y comprensible.

- **Referencias:** Si el _commit_ está relacionado con un _issue_, incluye la referencia en el mensaje del _commit_, por ejemplo: **'fix: corregir error en autenticación (closes #15)'**.