# SCMDB en español

Traducción al español para [SCMDB](https://scmdb.dev), la base de datos de misiones de Star Citizen.

> ⚙️ **Sistema automático, no gestionado.**
> Este repositorio se actualiza solo: no hay nadie revisándolo ni manteniéndolo a mano. Si algo se rompe, se corregirá, pero sin plazos ni garantías. Los textos son los de la traducción de Thord82 tal cual; los errores de traducción se reportan en [su repositorio](https://github.com/Thord82/Star_citizen_ES/issues), no aquí.

## Cómo usarlo

1. En SCMDB abre los ajustes (⚙️) → **Community Translation**.
2. Pega esta URL:
   ```
   https://raw.githubusercontent.com/Crosus97/SCMDB_LANG/refs/heads/main/lang-es-latest.json
   ```
3. Listo. La URL **no cambia nunca**: al recargar SCMDB cargará siempre la versión más reciente.

Las URLs antiguas (`lang-es-global-<versión>.json`) siguen funcionando y también reciben siempre la versión actual, pero es mejor usar la de arriba.

## Cómo se actualiza

Cada 6 horas una GitHub Action ([`update-scmdb-es.yml`](.github/workflows/update-scmdb-es.yml)):

1. Descarga la plantilla LIVE más reciente de [KrovaxCode/SCMDB_LANG](https://github.com/KrovaxCode/SCMDB_LANG).
2. Descarga el `global.ini` actual de [Thord82/Star_citizen_ES](https://github.com/Thord82/Star_citizen_ES) (rama `propuestas_thord`).
3. Genera el archivo con el script oficial de SCMDB y, solo si ha cambiado, lo publica.

Si la generación sale mal (menos de 1.000 textos traducidos) no se publica nada y se mantiene la versión anterior. Los textos que todavía no están traducidos aparecen en inglés.

## Créditos

- **Traducción:** [Thord82](https://github.com/Thord82/Star_citizen_ES).
- **Plantillas y herramienta:** [SCMDB / KrovaxCode](https://github.com/KrovaxCode/SCMDB_LANG).
- **Automatización:** Crosus97.

¿Buscas el juego en español con estadísticas de naves, componentes y misiones? → [StarCitizen-ES-SmartCitizen](https://github.com/Crosus97/StarCitizen-ES-SmartCitizen)

Proyecto no oficial, sin relación con Cloud Imperium Games.
