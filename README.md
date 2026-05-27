# SecureAudit MX

Software de auditoría de ciberseguridad orientado a PyMES en México, basado en los **CIS Controls v8 — Implementation Group 1 (IG1)**.

## Descripción

SecureAudit MX permite evaluar la postura de seguridad de una pequeña o mediana empresa mediante un cuestionario estructurado de 71 preguntas distribuidas en los 18 controles del marco CIS Controls v8. Cada pregunta está clasificada por impacto en la **Triada CIA** (Confidencialidad, Integridad, Disponibilidad) y por nivel de criticidad (Alta / Media / Baja).

El objetivo es ofrecer a las PyMES una herramienta accesible para identificar brechas de seguridad y priorizar acciones de mejora conforme a un estándar internacional reconocido.

## Controles cubiertos

| # | Control | Preguntas |
|---|---------|-----------|
| 1 | Inventario y Control de Activos de Hardware | 4 |
| 2 | Inventario y Control de Activos de Software | 4 |
| 3 | Protección de Datos | 5 |
| 4 | Configuración Segura de Activos | 4 |
| 5 | Gestión de Cuentas | 5 |
| 6 | Gestión de Control de Acceso | 5 |
| 7 | Gestión Continua de Vulnerabilidades | 4 |
| 8 | Gestión de Registros de Auditoría (Logs) | 4 |
| 9 | Protecciones del Navegador y Correo Electrónico | 4 |
| 10 | Defensas contra Malware | 4 |
| 11 | Recuperación de Datos (Backups) | 4 |
| 12 | Gestión de Infraestructura de Red | 4 |
| 13 | Monitoreo y Defensa de Red | 3 |
| 14 | Concienciación y Capacitación | 4 |
| 15 | Gestión de Proveedores y Servicios de Terceros | 3 |
| 16 | Seguridad del Software Desarrollado Internamente | 3 |
| 17 | Gestión de Respuesta a Incidentes | 4 |
| 18 | Pruebas de Penetración | 3 |
| | **Total** | **71** |

## Estructura del proyecto

```
secureaudit_mx/
├── app/          # Código fuente de la aplicación
├── docs/         # Documentación y checklists de auditoría
├── reports/      # Reportes generados por auditoría
└── tests/        # Pruebas automatizadas
```

## Marco de referencia

- **Estándar:** [CIS Controls v8](https://www.cisecurity.org/controls)
- **Grupo de implementación:** IG1 (controles esenciales para organizaciones con recursos limitados)
- **Contexto normativo:** Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP)

## Estado del proyecto

En desarrollo activo.

## Licencia

Por definir.
