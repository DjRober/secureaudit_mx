# Checklist de Auditoría de Seguridad — SecureAudit MX
**Basado en:** CIS Controls v8 — Implementation Group 1 (IG1)  
**Versión:** 1.0  
**Contexto:** PyMEs en Ciudad Juárez, México  
**Triada CIA:** C = Confidencialidad | I = Integridad | A = Disponibilidad  
**Criticidad:** Alta | Media | Baja

---

## CIS Control 1 — Inventario y Control de Activos de Hardware

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 1.1 | ¿La empresa tiene un inventario actualizado de todos los dispositivos conectados a la red (computadoras, impresoras, routers, etc.)? | C, I, A | Alta |
| 1.2 | ¿Se registra quién es el responsable de cada dispositivo? | I | Media |
| 1.3 | ¿Existe algún proceso para registrar dispositivos nuevos antes de conectarlos a la red? | C, A | Alta |
| 1.4 | ¿Se detectan y bloquean dispositivos no autorizados que se conecten a la red? | C | Alta |

---

## CIS Control 2 — Inventario y Control de Activos de Software

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 2.1 | ¿La empresa tiene un listado del software instalado en sus equipos? | I | Media |
| 2.2 | ¿Está prohibido instalar software sin autorización? | C, I | Alta |
| 2.3 | ¿Se verifica periódicamente si hay software no autorizado instalado? | C, I | Alta |
| 2.4 | ¿El software utilizado cuenta con licencias válidas y actualizadas? | I | Baja |

---

## CIS Control 3 — Protección de Datos

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 3.1 | ¿La empresa sabe qué datos son sensibles (datos de clientes, financieros, personales)? | C, I | Alta |
| 3.2 | ¿Los datos sensibles están cifrados cuando se almacenan? | C | Alta |
| 3.3 | ¿Los datos sensibles están cifrados cuando se transmiten (uso de HTTPS, VPN, etc.)? | C | Alta |
| 3.4 | ¿Existe una política sobre qué empleados pueden acceder a qué datos? | C | Alta |
| 3.5 | ¿Se tiene conocimiento de la Ley Federal de Protección de Datos Personales (LFPDPPP) y se cumple con ella? | C, I | Alta |

---

## CIS Control 4 — Configuración Segura de Activos

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 4.1 | ¿Se cambian las contraseñas por defecto de routers, switches y otros dispositivos de red? | C | Alta |
| 4.2 | ¿Los equipos tienen activado el firewall del sistema operativo? | A | Alta |
| 4.3 | ¿Se deshabilitan servicios y puertos innecesarios en los equipos? | C, A | Media |
| 4.4 | ¿Las configuraciones de seguridad de los equipos se revisan periódicamente? | I | Media |

---

## CIS Control 5 — Gestión de Cuentas

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 5.1 | ¿Cada empleado tiene su propia cuenta de usuario (no comparten cuentas)? | C, I | Alta |
| 5.2 | ¿Existen cuentas de administrador separadas de las cuentas de uso diario? | C, I | Alta |
| 5.3 | ¿Se eliminan o deshabilitan las cuentas de empleados que ya no trabajan en la empresa? | C | Alta |
| 5.4 | ¿Se tiene un registro de todas las cuentas de usuario activas? | I | Media |
| 5.5 | ¿Se revisa periódicamente quién tiene acceso a qué sistemas? | C, I | Alta |

---

## CIS Control 6 — Gestión de Control de Acceso

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 6.1 | ¿Se aplica el principio de mínimo privilegio (cada usuario solo accede a lo que necesita)? | C | Alta |
| 6.2 | ¿Se usa autenticación de dos factores (2FA) en sistemas críticos o correo corporativo? | C | Alta |
| 6.3 | ¿Las contraseñas cumplen con una política de seguridad (mínimo de caracteres, complejidad)? | C | Alta |
| 6.4 | ¿Se bloquea la sesión automáticamente tras un período de inactividad? | C | Media |
| 6.5 | ¿Está prohibido compartir contraseñas entre empleados? | C | Alta |

---

## CIS Control 7 — Gestión Continua de Vulnerabilidades

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 7.1 | ¿Los sistemas operativos de los equipos están actualizados? | A | Alta |
| 7.2 | ¿Las aplicaciones (navegadores, Office, etc.) están actualizadas? | C, I | Alta |
| 7.3 | ¿Se aplican parches de seguridad cuando están disponibles? | A | Alta |
| 7.4 | ¿Existe algún proceso para conocer nuevas vulnerabilidades que afecten el software que usan? | I | Media |

---

## CIS Control 8 — Gestión de Registros de Auditoría (Logs)

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 8.1 | ¿Los sistemas críticos generan logs de actividad (accesos, errores, cambios)? | I | Alta |
| 8.2 | ¿Los logs se almacenan de forma segura y no pueden ser borrados por usuarios normales? | I | Alta |
| 8.3 | ¿Alguien revisa los logs periódicamente para detectar actividad sospechosa? | C, I | Alta |
| 8.4 | ¿Se conservan los logs por al menos 90 días? | I | Media |

---

## CIS Control 9 — Protecciones del Navegador y Correo Electrónico

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 9.1 | ¿Los empleados tienen capacitación básica para identificar correos de phishing? | C | Alta |
| 9.2 | ¿Existe un filtro de spam activo en el correo corporativo? | A | Alta |
| 9.3 | ¿Está bloqueado el acceso a sitios web maliciosos o no relacionados con el trabajo? | C | Media |
| 9.4 | ¿Los navegadores están actualizados a su versión más reciente? | C | Media |

---

## CIS Control 10 — Defensas contra Malware

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 10.1 | ¿Todos los equipos tienen un antivirus o antimalware instalado y activo? | C, I, A | Alta |
| 10.2 | ¿Las definiciones del antivirus se actualizan automáticamente? | C, I | Alta |
| 10.3 | ¿Está deshabilitada la ejecución automática de dispositivos USB? | C, I | Alta |
| 10.4 | ¿Se realizan escaneos periódicos completos en los equipos? | C, I | Media |

---

## CIS Control 11 — Recuperación de Datos (Backups)

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 11.1 | ¿Se realizan copias de seguridad (backups) de los datos críticos del negocio? | A | Alta |
| 11.2 | ¿Los backups se almacenan en una ubicación separada (externa o en la nube)? | A | Alta |
| 11.3 | ¿Se ha probado alguna vez la restauración de un backup para verificar que funciona? | A | Alta |
| 11.4 | ¿Con qué frecuencia se realizan los backups? (Diario/Semanal/Mensual) | A | Alta |

---

## CIS Control 12 — Gestión de Infraestructura de Red

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 12.1 | ¿La red WiFi de empleados está separada de la red WiFi para visitantes? | C | Alta |
| 12.2 | ¿El router/firewall perimetral tiene configuración de seguridad revisada? | C, A | Alta |
| 12.3 | ¿Se monitorea quién está conectado a la red en tiempo real? | C | Media |
| 12.4 | ¿Existen redes separadas (VLANs) para diferentes áreas del negocio? | C | Media |

---

## CIS Control 13 — Monitoreo y Defensa de Red

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 13.1 | ¿Existe algún sistema que alerte sobre actividad inusual en la red? | C, A | Alta |
| 13.2 | ¿Se monitorea el tráfico de red para detectar transferencias anómalas de datos? | C | Alta |
| 13.3 | ¿Se han definido qué eventos de red deben generar una alerta? | I | Media |

---

## CIS Control 14 — Concienciación y Capacitación

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 14.1 | ¿Los empleados reciben capacitación en seguridad informática al menos una vez al año? | C, I, A | Alta |
| 14.2 | ¿Existe una política de uso aceptable de los recursos tecnológicos de la empresa? | C, I | Alta |
| 14.3 | ¿Los empleados saben a quién reportar un incidente de seguridad? | A | Alta |
| 14.4 | ¿Se realizan simulacros de phishing para medir la concienciación del personal? | C | Media |

---

## CIS Control 15 — Gestión de Proveedores y Servicios de Terceros

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 15.1 | ¿Se evalúa la seguridad de los proveedores que tienen acceso a sistemas o datos de la empresa? | C | Alta |
| 15.2 | ¿Los contratos con proveedores incluyen cláusulas de seguridad y confidencialidad? | C, I | Alta |
| 15.3 | ¿Se revoca el acceso de proveedores cuando ya no son necesarios? | C | Alta |

---

## CIS Control 16 — Seguridad del Software Desarrollado Internamente

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 16.1 | ¿El software desarrollado internamente sigue prácticas de desarrollo seguro? | C, I | Alta |
| 16.2 | ¿Se realizan revisiones de seguridad antes de poner en producción nuevo software? | I | Alta |
| 16.3 | ¿Los errores de la aplicación se manejan sin exponer información técnica al usuario? | C | Media |

---

## CIS Control 17 — Gestión de Respuesta a Incidentes

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 17.1 | ¿Existe un plan de respuesta a incidentes de seguridad documentado? | A | Alta |
| 17.2 | ¿Los empleados clave saben qué hacer si detectan un ataque o brecha de seguridad? | A | Alta |
| 17.3 | ¿Se ha practicado o simulado alguna vez la respuesta a un incidente? | A | Media |
| 17.4 | ¿Se documentan los incidentes de seguridad ocurridos para aprender de ellos? | I | Media |

---

## CIS Control 18 — Pruebas de Penetración

| ID | Pregunta de Auditoría | CIA | Criticidad |
|----|----------------------|-----|------------|
| 18.1 | ¿Se realizan pruebas de penetración periódicas a los sistemas críticos? | C, I, A | Alta |
| 18.2 | ¿Los hallazgos de pruebas anteriores han sido corregidos? | C, I, A | Alta |
| 18.3 | ¿Existe un proceso formal para contratar y autorizar pruebas de seguridad externas? | I | Media |

---

## Resumen de Controles

| Control | Total Preguntas | Alta | Media | Baja |
|---------|----------------|------|-------|------|
| 1. Inventario Hardware | 4 | 3 | 1 | 0 |
| 2. Inventario Software | 4 | 2 | 1 | 1 |
| 3. Protección de Datos | 5 | 5 | 0 | 0 |
| 4. Configuración Segura | 4 | 2 | 2 | 0 |
| 5. Gestión de Cuentas | 5 | 4 | 1 | 0 |
| 6. Control de Acceso | 5 | 4 | 1 | 0 |
| 7. Vulnerabilidades | 4 | 3 | 1 | 0 |
| 8. Logs | 4 | 3 | 1 | 0 |
| 9. Navegador y Correo | 4 | 2 | 2 | 0 |
| 10. Malware | 4 | 3 | 1 | 0 |
| 11. Backups | 4 | 4 | 0 | 0 |
| 12. Red | 4 | 3 | 2 | 0 |
| 13. Monitoreo de Red | 3 | 2 | 1 | 0 |
| 14. Capacitación | 4 | 3 | 1 | 0 |
| 15. Proveedores | 3 | 3 | 0 | 0 |
| 16. Software Propio | 3 | 2 | 1 | 0 |
| 17. Respuesta Incidentes | 4 | 2 | 2 | 0 |
| 18. Pen Testing | 3 | 2 | 1 | 0 |
| **TOTAL** | **71** | **52** | **19** | **1** |

---
*Documento generado para el proyecto SecureAudit MX*  
*Referencia: CIS Controls v8 — https://www.cisecurity.org/controls*
