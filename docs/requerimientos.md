# SecureAudit MX — Especificación de Requerimientos de Software

| Campo                      | Valor         |
| -------------------------- | ------------- |
| **Versión**                | 1.0.0         |
| **Fecha**                  | 2026-05-29    |
| **Autor**                  | Roberto Pérez |
| **Estado**                 | En desarrollo |
| **Estándar de referencia** | IEEE 830      |

---

## Tabla de contenido

- [1. Introducción](#1-introducción)
  - [1.1 Propósito del documento](#11-propósito-del-documento)
  - [1.2 Alcance del sistema](#12-alcance-del-sistema)
  - [1.3 Definiciones y acrónimos](#13-definiciones-y-acrónimos)
  - [1.4 Referencias](#14-referencias)
- [2. Descripción General](#2-descripción-general)
  - [2.1 Perspectiva del producto](#21-perspectiva-del-producto)
  - [2.2 Descripción del producto](#22-descripción-del-producto)
  - [2.3 Usuarios y stakeholders](#23-usuarios-y-stakeholders)
  - [2.4 Supuestos y dependencias](#24-supuestos-y-dependencias)
- [3. Requerimientos Funcionales](#3-requerimientos-funcionales-rf)
- [4. Requerimientos No Funcionales](#4-requerimientos-no-funcionales-rnf)
- [5. Casos de uso](#5-casos-de-uso)
- [6. Restricciones](#6-restricciones)

---

## 1. Introducción

### 1.1 Propósito del documento

Este documento especifica los requerimientos funcionales y no funcionales de **SecureAudit MX**, y sirve como referencia técnica para el equipo de desarrollo, auditores que implementen la herramienta, y como evidencia de diseño ante stakeholders académicos y profesionales.

### 1.2 Alcance del sistema

**Dentro del alcance:**

- Evaluación guiada de los 18 controles CIS v8 IG1 mediante cuestionarios y verificaciones técnicas
- Generación de reportes de cumplimiento con hallazgos y recomendaciones por control
- Gestión de sesiones de auditoría (crear, pausar y reanudar)
- Selección personalizada de controles a auditar
- Autenticación de usuarios con roles diferenciados

**Fuera del alcance:**

- Remediación automática de vulnerabilidades encontradas
- Monitoreo continuo o en tiempo real (no es un SIEM)
- Cobertura completa de controles IG2 e IG3 (la versión actual incluye únicamente salvaguardas IG1 completas más elementos selectos de IG2 relevantes para PyMES)
- Integración con herramientas externas de terceros
- Auditoría de infraestructura cloud
- Gestión o modificación directa de configuraciones del sistema auditado
- Soporte multiempresa simultáneo (la versión actual evalúa una organización a la vez)

### 1.3 Definiciones y acrónimos

**Acrónimos**

| Acrónimo | Significado                               |
| -------- | ----------------------------------------- |
| CIS      | Center for Internet Security              |
| IG1      | Implementation Group 1                    |
| IG2      | Implementation Group 2                    |
| IG3      | Implementation Group 3                    |
| PyME     | Pequeña y Mediana Empresa                 |
| SRS      | Software Requirements Specification       |
| RF       | Requerimiento Funcional                   |
| RNF      | Requerimiento No Funcional                |
| UX/UI    | User Experience / User Interface          |
| PDF      | Portable Document Format                  |
| HTML     | HyperText Markup Language                 |
| SIEM     | Security Information and Event Management |
| TI       | Tecnologías de la Información             |

**Definiciones**

| Término                      | Definición                                                                                                                                                                         |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CIS Controls v8              | Marco de referencia de 18 controles de seguridad publicado por el Center for Internet Security, diseñado para reducir el riesgo cibernético en organizaciones de cualquier tamaño. |
| Implementation Group 1 (IG1) | Subconjunto básico de salvaguardas CIS orientado a empresas pequeñas con recursos limitados de TI; representa el estándar mínimo de ciberhigiene.                                  |
| Auditoría de seguridad       | Proceso sistemático de evaluación del cumplimiento de una organización respecto a un conjunto de controles o estándares de seguridad definidos.                                    |
| Sesión de auditoría          | Instancia de trabajo dentro de SecureAudit MX que agrupa los resultados de una evaluación para una organización en un momento determinado.                                         |
| Hallazgo                     | Resultado de la evaluación de un control CIS que indica si la organización cumple, cumple parcialmente o no cumple con el requisito.                                               |
| Reporte de cumplimiento      | Documento generado por la herramienta que consolida los hallazgos de la auditoría con recomendaciones de remediación.                                                              |
| Remediación                  | Conjunto de acciones correctivas recomendadas para subsanar un hallazgo de incumplimiento.                                                                                         |
| Activo de empresa            | Cualquier dispositivo, sistema o dato que tenga valor para la organización y requiera protección.                                                                                  |
| Rol de usuario               | Conjunto de permisos y capacidades asignados a un tipo de usuario dentro de SecureAudit MX.                                                                                        |

### 1.4 Referencias

| ID  | Referencia                                                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------- |
| R01 | Center for Internet Security. _CIS Controls v8_. CIS, 2021. https://www.cisecurity.org/controls/v8                              |
| R02 | IEEE. _IEEE 830-1998: Recommended Practice for Software Requirements Specifications_. IEEE, 1998.                               |
| R03 | Flask Project. _Flask Documentation v3.x_. Pallets Projects, 2024. https://flask.palletsprojects.com                            |
| R04 | Python Software Foundation. _Python 3.x Documentation_. PSF, 2024. https://docs.python.org/3                                    |
| R05 | NIST. _Small Business Cybersecurity Corner_. National Institute of Standards and Technology. https://www.nist.gov/cybersecurity |
| R06 | INEGI. _Estadísticas sobre las Micro, Pequeñas y Medianas Empresas en México_. INEGI, 2023. https://www.inegi.org.mx            |

---

## 2. Descripción General

### 2.1 Perspectiva del producto

SecureAudit MX es una aplicación web local (_standalone_) desarrollada en Python con Flask. Se distribuye como repositorio público en GitHub y se instala directamente en el equipo del auditor o administrador de TI, sin requerir conexión a internet durante su ejecución.

El sistema opera bajo una arquitectura cliente-servidor local:

- **Servidor:** instancia Flask ejecutándose en `localhost`
- **Cliente:** navegador web del equipo local (Chrome, Firefox)
- **Persistencia:** base de datos SQLite almacenada localmente

SecureAudit MX no depende de servicios externos en tiempo de ejecución ni transmite datos de la auditoría fuera del equipo donde está instalado, lo cual es relevante para organizaciones con políticas de confidencialidad de datos.

### 2.2 Descripción del producto

**Contexto**

Las PyMES en México representan el 99.8% del total de empresas del país (INEGI, 2023); sin embargo, la gran mayoría carece de procesos formales de seguridad informática. La ausencia de auditorías periódicas expone sus activos digitales a vulnerabilidades conocidas y evitables.

**Problema identificado**

Las PyMES mexicanas no cuentan con herramientas accesibles que les permitan evaluar su postura de seguridad de manera estructurada. Las soluciones existentes en el mercado están orientadas a grandes empresas, requieren conocimiento técnico avanzado o representan un costo prohibitivo para organizaciones pequeñas.

**Solución propuesta**

SecureAudit MX ofrece una herramienta de auditoría local, gratuita y guiada, basada en CIS Controls v8 IG1 — el estándar mínimo de ciberhigiene recomendado internacionalmente — que permite a auditores y administradores de TI identificar áreas de oportunidad sin requerir infraestructura especializada.

### 2.3 Usuarios y stakeholders

**Stakeholders**

| Rol             | Descripción                                                                          | Interés en el sistema                                              |
| --------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| Desarrollador   | Roberto Pérez — responsable del diseño, desarrollo y mantenimiento de SecureAudit MX | Que el sistema cumpla los requerimientos definidos y sea escalable |
| PyME cliente    | Organización que contrata o adopta la herramienta                                    | Conocer su postura de seguridad y reducir riesgos                  |
| Auditor externo | Profesional de ciberseguridad que usa la herramienta como apoyo en sus servicios     | Eficiencia y credibilidad del reporte generado                     |

**Usuarios del sistema**

| ID  | Rol                           | Descripción                                                                                                                                                            | Nivel técnico | Motivación                                                                                                   |
| --- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------ |
| U01 | Auditor / Sysadmin            | Profesional de seguridad o administrador responsable de ejecutar la auditoría completa                                                                                 | Alto          | Obtener un reporte estructurado y exportable para presentar hallazgos                                        |
| U02 | Técnico de soporte / Admin TI | Personal interno de la PyME que asiste en la recolección de evidencia y puede ejecutar auditorías parciales limitadas a los controles pertinentes a su área de gestión | Medio         | Verificar el cumplimiento de los activos bajo su responsabilidad sin requerir acceso a la auditoría completa |
| U03 | Directivo / Dueño PyME        | Responsable de la toma de decisiones que consulta los resultados sin operar la herramienta directamente                                                                | Bajo          | Entender el riesgo de la empresa en términos no técnicos y priorizar inversión                               |

**Permisos por rol**

| Funcionalidad                                        | U01 Auditor | U02 Técnico | U03 Directivo |
| ---------------------------------------------------- | :---------: | :---------: | :-----------: |
| Ejecutar auditoría completa (18 controles)           |      ✓      |      ✗      |       ✗       |
| Ejecutar auditoría parcial (controles seleccionados) |      ✓      |      ✓      |       ✗       |
| Configurar controles a auditar                       |      ✓      |      ✓      |       ✗       |
| Gestionar sesiones (crear, pausar, reanudar)         |      ✓      |      ✓      |       ✗       |
| Consultar reportes generados                         |      ✓      |      ✓      |       ✓       |
| Exportar reportes (PDF/HTML)                         |      ✓      |      ✓      |       ✓       |
| Gestionar usuarios                                   |      ✓      |      ✗      |       ✗       |

### 2.4 Supuestos y dependencias

**Supuestos**

| ID  | Supuesto                                                                                                  |
| --- | --------------------------------------------------------------------------------------------------------- |
| S01 | El equipo donde se instala SecureAudit MX cuenta con Python 3.10 o superior.                              |
| S02 | El auditor o técnico tiene permisos de administrador en el equipo donde se ejecuta la herramienta.        |
| S03 | El equipo tiene un navegador web moderno instalado (Chrome, Firefox o Edge en versiones recientes).       |
| S04 | El usuario tiene conocimientos básicos de seguridad informática para interpretar los hallazgos generados. |
| S05 | La organización auditada proporciona acceso e información verídica durante el proceso de auditoría.       |
| S06 | Los datos de auditoría son confidenciales y responsabilidad del auditor que ejecuta la herramienta.       |

**Dependencias**

| ID  | Dependencia                           | Tipo         | Impacto si falla                                         |
| --- | ------------------------------------- | ------------ | -------------------------------------------------------- |
| D01 | Python 3.10+                          | Tecnológica  | El sistema no puede ejecutarse                           |
| D02 | Flask 3.x                             | Tecnológica  | El servidor local no levanta                             |
| D03 | SQLite3                               | Tecnológica  | No hay persistencia de sesiones ni reportes              |
| D04 | Repositorio GitHub (`secureaudit-mx`) | Distribución | El usuario no puede obtener ni actualizar la herramienta |
| D05 | Navegador web local                   | Tecnológica  | La interfaz no es accesible para el usuario              |

---

---

## 3. Requerimientos Funcionales (RF)

### Resumen

| ID    | Módulo                                    | Prioridad |  Estado   |   Fase   |
| ----- | ----------------------------------------- | :-------: | :-------: | :------: |
| RF-01 | Autenticación y gestión de usuarios       |   Alta    | Pendiente | Semana 7 |
| RF-02 | Gestión de empresas auditadas             |   Alta    | Pendiente | Semana 3 |
| RF-03 | Gestión de sesiones de auditoría          |   Alta    | Pendiente | Semana 4 |
| RF-04 | Cuestionario de auditoría                 |   Alta    | Pendiente | Semana 4 |
| RF-05 | Sistema de scoring y evaluación de riesgo |   Alta    | Pendiente | Semana 5 |
| RF-06 | Dashboard de resultados                   |   Media   | Pendiente | Semana 5 |
| RF-07 | Generación y exportación de reportes      |   Alta    | Pendiente | Semana 6 |
| RF-08 | Módulo de escaneo de red                  |   Media   | Pendiente | Semana 8 |
| RF-09 | Log de actividad interno                  |   Alta    | Pendiente | Semana 7 |

---

### RF-01 — Autenticación y gestión de usuarios

| Campo         | Detalle                             |
| ------------- | ----------------------------------- |
| **ID**        | RF-01                               |
| **Nombre**    | Autenticación y gestión de usuarios |
| **Prioridad** | Alta                                |
| **Actores**   | U01 Auditor, U02 Técnico            |
| **Fase**      | Semana 7                            |

**Descripción**

El sistema debe permitir el registro, autenticación y administración de usuarios con roles diferenciados. Cada usuario accede únicamente a las auditorías y datos bajo su responsabilidad.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                                                                                                                                                                    |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-01.1 | El sistema debe permitir registrar un nuevo usuario con nombre, correo electrónico y contraseña.                                                                                                                                                                               |
| RF-01.2 | El sistema debe autenticar usuarios mediante correo y contraseña. Las contraseñas deben almacenarse con hash (bcrypt).                                                                                                                                                         |
| RF-01.3 | El sistema debe mantener la sesión activa mediante cookies seguras y cerrarla al hacer logout o por inactividad.                                                                                                                                                               |
| RF-01.4 | El sistema debe soportar tres roles: **Auditor** (acceso completo a auditorías y reportes), **Técnico** (auditorías parciales y consulta de reportes) y **Directivo** (solo lectura: consulta y exportación de reportes). La gestión de usuarios es exclusiva del rol Auditor. |
| RF-01.5 | Todas las rutas de la aplicación deben estar protegidas y requerir autenticación activa.                                                                                                                                                                                       |
| RF-01.6 | El Auditor (U01) puede crear, desactivar y eliminar cuentas de usuario.                                                                                                                                                                                                        |
| RF-01.7 | El sistema debe limitar los intentos de login fallidos a un máximo de 5 por cuenta. Tras alcanzar el límite, la cuenta debe bloquearse temporalmente durante 15 minutos. El bloqueo y los intentos fallidos deben registrarse en el log interno (RF-09).                        |

---

### RF-02 — Gestión de empresas auditadas

| Campo         | Detalle                       |
| ------------- | ----------------------------- |
| **ID**        | RF-02                         |
| **Nombre**    | Gestión de empresas auditadas |
| **Prioridad** | Alta                          |
| **Actores**   | U01 Auditor, U02 Técnico      |
| **Fase**      | Semana 3                      |

**Descripción**

El sistema debe permitir registrar y administrar los datos de las organizaciones que serán auditadas, asociando cada empresa a las sesiones de auditoría que le corresponden.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| RF-02.1 | El sistema debe permitir crear un registro de empresa con nombre, sector, tamaño (número de empleados) y nombre del contacto. |
| RF-02.2 | El sistema debe listar todas las empresas registradas por el usuario autenticado.                                             |
| RF-02.3 | El sistema debe permitir editar los datos de una empresa existente.                                                           |
| RF-02.4 | El sistema debe impedir eliminar una empresa que tenga sesiones de auditoría activas o finalizadas asociadas.                 |

---

### RF-03 — Gestión de sesiones de auditoría

| Campo         | Detalle                          |
| ------------- | -------------------------------- |
| **ID**        | RF-03                            |
| **Nombre**    | Gestión de sesiones de auditoría |
| **Prioridad** | Alta                             |
| **Actores**   | U01 Auditor, U02 Técnico         |
| **Fase**      | Semana 4                         |

**Descripción**

El sistema debe permitir crear, pausar, reanudar y finalizar sesiones de auditoría vinculadas a una empresa. Una sesión agrupa todas las respuestas y resultados de una evaluación en un momento determinado.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                             |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| RF-03.1 | El sistema debe permitir crear una nueva sesión de auditoría asociada a una empresa, registrando fecha de inicio y auditor responsable. |
| RF-03.2 | El sistema debe permitir seleccionar los controles CIS a evaluar antes de iniciar (auditoría completa o parcial).                       |
| RF-03.3 | El sistema debe permitir pausar una sesión en cualquier punto y reanudarla posteriormente desde donde se dejó.                          |
| RF-03.4 | El sistema debe mostrar el estado de cada sesión: **En progreso**, **Pausada** o **Finalizada**.                                        |
| RF-03.5 | Una sesión finalizada no puede ser modificada; solo puede consultarse y exportarse.                                                     |
| RF-03.6 | El sistema debe listar todas las sesiones de auditoría del usuario, ordenadas por fecha de creación.                                    |

---

### RF-04 — Cuestionario de auditoría

| Campo         | Detalle                   |
| ------------- | ------------------------- |
| **ID**        | RF-04                     |
| **Nombre**    | Cuestionario de auditoría |
| **Prioridad** | Alta                      |
| **Actores**   | U01 Auditor, U02 Técnico  |
| **Fase**      | Semana 4                  |

**Descripción**

El sistema debe presentar de forma guiada las preguntas de evaluación correspondientes a cada control CIS v8 IG1. El auditor responde cada pregunta y puede navegar entre controles libremente.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| RF-04.1 | El sistema debe mostrar las preguntas organizadas por control CIS (máximo 18 secciones).                                      |
| RF-04.2 | Cada pregunta debe ofrecer tres opciones de respuesta: **Sí**, **No** y **N/A**.                                              |
| RF-04.3 | El sistema debe permitir agregar un comentario opcional por pregunta para registrar evidencia o contexto.                     |
| RF-04.4 | El sistema debe mostrar una barra de progreso global y por control durante la auditoría.                                      |
| RF-04.5 | El sistema debe permitir navegar libremente entre controles (anterior / siguiente) sin perder respuestas ya guardadas.        |
| RF-04.6 | El sistema debe guardar automáticamente las respuestas al avanzar entre preguntas, sin requerir acción explícita del usuario. |
| RF-04.7 | El sistema debe indicar visualmente qué controles ya fueron completados y cuáles están pendientes.                            |

---

### RF-05 — Sistema de scoring y evaluación de riesgo

| Campo         | Detalle                                   |
| ------------- | ----------------------------------------- |
| **ID**        | RF-05                                     |
| **Nombre**    | Sistema de scoring y evaluación de riesgo |
| **Prioridad** | Alta                                      |
| **Actores**   | U01 Auditor, U02 Técnico                  |
| **Fase**      | Semana 5                                  |

**Descripción**

El sistema debe calcular automáticamente un puntaje de riesgo por control y un score global al finalizar la auditoría, utilizando la criticidad de cada pregunta como ponderador.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RF-05.1 | Cada pregunta debe tener asignada una criticidad: **Alta**, **Media** o **Baja**.                                                                                                               |
| RF-05.2 | El sistema debe calcular el score de riesgo de acuerdo con la siguiente tabla: respuesta "No" en pregunta Alta = 3 puntos; Media = 2 puntos; Baja = 1 punto; respuesta "Sí" o "N/A" = 0 puntos. |
| RF-05.3 | El sistema debe calcular un score parcial por cada control CIS y un score global de la auditoría (escala 0–100, donde 100 representa el máximo riesgo).                                         |
| RF-05.4 | El sistema debe clasificar cada control con un nivel de riesgo: **Crítico** (≥ 75%), **Alto** (50–74%), **Medio** (25–49%) o **Bajo** (< 25%).                                                  |
| RF-05.5 | El sistema debe recalcular el score en tiempo real conforme el auditor avanza en el cuestionario.                                                                                               |

---

### RF-06 — Dashboard de resultados

| Campo         | Detalle                                 |
| ------------- | --------------------------------------- |
| **ID**        | RF-06                                   |
| **Nombre**    | Dashboard de resultados                 |
| **Prioridad** | Media                                   |
| **Actores**   | U01 Auditor, U02 Técnico, U03 Directivo |
| **Fase**      | Semana 5                                |

**Descripción**

El sistema debe presentar una vista consolidada de los resultados de una auditoría con visualizaciones que permitan identificar rápidamente las áreas de mayor riesgo.

**Requerimientos específicos**

| ID      | Descripción                                                                                                           |
| ------- | --------------------------------------------------------------------------------------------------------------------- |
| RF-06.1 | El sistema debe mostrar el score global de la auditoría con indicador visual tipo semáforo (Verde / Amarillo / Rojo). |
| RF-06.2 | El sistema debe mostrar una gráfica de radar con el nivel de riesgo de cada uno de los 18 controles CIS.              |
| RF-06.3 | El sistema debe listar los hallazgos (respuestas "No") ordenados por criticidad descendente.                          |
| RF-06.4 | El sistema debe mostrar un resumen de cumplimiento: número de controles con riesgo Crítico, Alto, Medio y Bajo.       |
| RF-06.5 | El dashboard debe ser accesible para el rol U03 (Directivo) en modo solo lectura, sin opción de editar respuestas.    |

---

### RF-07 — Generación y exportación de reportes

| Campo         | Detalle                                 |
| ------------- | --------------------------------------- |
| **ID**        | RF-07                                   |
| **Nombre**    | Generación y exportación de reportes    |
| **Prioridad** | Alta                                    |
| **Actores**   | U01 Auditor, U02 Técnico, U03 Directivo |
| **Fase**      | Semana 6                                |

**Descripción**

El sistema debe generar un reporte profesional descargable en formato PDF que consolide todos los hallazgos, scores y recomendaciones de la auditoría en un documento apto para ser entregado al cliente.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                                                                                                                                            |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-07.1 | El sistema debe generar un reporte PDF con la siguiente estructura: portada (nombre empresa, fecha, auditor), resumen ejecutivo, score global con semáforo, hallazgos por control con nivel de riesgo, top 10 recomendaciones priorizadas, y glosario. |
| RF-07.2 | El resumen ejecutivo debe estar redactado en lenguaje no técnico, orientado al perfil U03 (Directivo / Dueño PyME).                                                                                                                                    |
| RF-07.3 | El sistema debe permitir descargar el reporte PDF directamente desde la vista de resultados de una sesión finalizada.                                                                                                                                  |
| RF-07.4 | El sistema debe ofrecer también exportación en formato HTML para visualización en navegador sin necesidad de lector PDF.                                                                                                                               |
| RF-07.5 | El reporte debe incluir fecha de generación, versión del sistema y nombre del auditor que ejecutó la auditoría.                                                                                                                                        |

---

### RF-08 — Módulo de escaneo de red

| Campo         | Detalle                  |
| ------------- | ------------------------ |
| **ID**        | RF-08                    |
| **Nombre**    | Módulo de escaneo de red |
| **Prioridad** | Media                    |
| **Actores**   | U01 Auditor              |
| **Fase**      | Semana 8                 |

**Descripción**

El sistema debe ofrecer un módulo opcional que automatice parcialmente el cuestionario técnico mediante escaneo de red con Nmap. Su uso requiere autorización explícita del auditor y solo debe emplearse en redes propias o con permiso escrito del cliente.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RF-08.1 | El sistema debe mostrar un aviso legal y requerir confirmación explícita del auditor antes de ejecutar cualquier escaneo.                                                                  |
| RF-08.2 | El sistema debe permitir especificar el rango de red a escanear (CIDR, e.g. `192.168.1.0/24`).                                                                                             |
| RF-08.3 | El sistema debe detectar hosts activos, puertos abiertos y versiones de servicios en la red especificada mediante python-nmap.                                                             |
| RF-08.4 | El sistema debe correlacionar automáticamente los resultados del escaneo con preguntas del cuestionario. Por ejemplo: puerto 23 (Telnet) abierto → marcar control CIS 4.3 como incumplido. |
| RF-08.5 | Las respuestas auto-completadas por el escaneo deben ser identificables visualmente y el auditor debe poder revisarlas y modificarlas manualmente.                                         |
| RF-08.6 | Los resultados del escaneo deben integrarse en el reporte PDF como sección de evidencia técnica.                                                                                           |
| RF-08.7 | El módulo de escaneo requiere que Nmap esté instalado en el sistema operativo del equipo donde corre la aplicación.                                                                        |

---

### RF-09 — Log de actividad interno

| Campo         | Detalle                  |
| ------------- | ------------------------ |
| **ID**        | RF-09                    |
| **Nombre**    | Log de actividad interno |
| **Prioridad** | Alta                     |
| **Actores**   | U01 Auditor              |
| **Fase**      | Semana 7                 |

**Descripción**

SecureAudit MX es una herramienta de auditoría — debe ser auditable ella misma. El sistema debe registrar en un log interno las acciones relevantes realizadas por los usuarios, de modo que exista trazabilidad de quién hizo qué y cuándo dentro de la aplicación.

**Requerimientos específicos**

| ID      | Descripción                                                                                                                                                                                                                                                                      |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RF-09.1 | El sistema debe registrar en un log interno las siguientes acciones: inicio y cierre de sesión de usuario, creación y finalización de sesiones de auditoría, generación y exportación de reportes, ejecución del módulo de escaneo de red, y creación o eliminación de usuarios. |
| RF-09.2 | Cada entrada de log debe contener: marca de tiempo (timestamp), identificador del usuario, tipo de acción y resultado (éxito / fallo).                                                                                                                                           |
| RF-09.3 | El log debe persistirse en un archivo local (e.g., `logs/auditoria.log`) con rotación automática al superar 10 MB.                                                                                                                                                               |
| RF-09.4 | El log no debe contener información sensible como contraseñas, tokens de sesión ni datos personales de los usuarios auditados.                                                                                                                                                   |
| RF-09.5 | El Auditor (U01) debe poder consultar el log de actividad desde la interfaz de administración. Otros roles no tienen acceso al log.                                                                                                                                              |

---

## 4. Requerimientos No Funcionales (RNF)

### Resumen

| ID     | Categoría      | Prioridad |
| ------ | -------------- | :-------: |
| RNF-01 | Seguridad      |   Alta    |
| RNF-02 | Usabilidad     |   Alta    |
| RNF-03 | Rendimiento    |   Media   |
| RNF-04 | Portabilidad   |   Alta    |
| RNF-05 | Mantenibilidad |   Media   |
| RNF-06 | Confiabilidad  |   Alta    |

---

### RNF-01 — Seguridad

**Descripción**

Dado que SecureAudit MX es una herramienta de auditoría de seguridad, la aplicación misma no debe presentar las vulnerabilidades que evalúa. La implementación debe seguir las prácticas recomendadas por OWASP para aplicaciones web.

| ID       | Requerimiento                                                                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-01.1 | Las contraseñas de usuario deben almacenarse usando hashing bcrypt. Queda prohibido almacenar contraseñas en texto plano.                                   |
| RNF-01.2 | Todos los formularios POST deben incluir protección contra CSRF mediante tokens de sesión.                                                                  |
| RNF-01.3 | La aplicación debe sanitizar y validar todos los inputs del usuario para prevenir inyección SQL y XSS.                                                      |
| RNF-01.4 | La aplicación debe incluir headers de seguridad HTTP: `Content-Security-Policy`, `X-Content-Type-Options` y `X-Frame-Options`. El header `Strict-Transport-Security` debe configurarse únicamente en despliegues futuros sobre HTTPS — en `localhost` HTTP es ignorado por el navegador y no aplica en v1.0.0. |
| RNF-01.5 | Las sesiones de usuario deben expirar tras 60 minutos de inactividad.                                                                                       |
| RNF-01.6 | El módulo de escaneo de red (RF-08) debe requerir confirmación explícita antes de ejecutarse y registrar en log la autorización del auditor.                |

---

### RNF-02 — Usabilidad

**Descripción**

La herramienta debe ser operable por usuarios con distintos niveles técnicos, incluyendo el perfil U03 (Directivo / Dueño PyME) que tiene nivel técnico bajo. El flujo de auditoría debe ser guiado y no requerir capacitación previa.

| ID       | Requerimiento                                                                                                                                                                    |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-02.1 | Un auditor sin experiencia previa con la herramienta debe poder completar su primera auditoría en menos de 45 minutos.                                                           |
| RNF-02.2 | La interfaz debe estar completamente en español, incluyendo mensajes de error, etiquetas y ayudas contextuales.                                                                  |
| RNF-02.3 | Cada pregunta del cuestionario debe incluir una descripción de ayuda que explique qué se está evaluando, sin asumir conocimiento técnico avanzado del usuario.                   |
| RNF-02.4 | Los mensajes de error deben ser descriptivos e indicar al usuario la acción correctiva, sin exponer detalles internos del sistema (stack traces, rutas de archivo, etc.).        |
| RNF-02.5 | El reporte PDF generado (RF-07) debe incluir un resumen ejecutivo comprensible para un perfil no técnico, evitando siglas sin definir y terminología especializada sin contexto. |
| RNF-02.6 | La aplicación debe ser responsiva y operable desde un navegador de escritorio con resolución mínima de 1280 × 720 px.                                                            |

---

### RNF-03 — Rendimiento

**Descripción**

La aplicación debe responder en tiempos razonables en hardware típico de una PyME, sin requerir equipos especializados ni conexión a internet.

| ID       | Requerimiento                                                                                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RNF-03.1 | El tiempo de respuesta de cualquier página de la aplicación (excluido el escaneo de red) no debe superar 2 segundos en un equipo con 4 GB de RAM y procesador de doble núcleo. |
| RNF-03.2 | La generación del reporte PDF no debe tardar más de 10 segundos para una auditoría completa de 18 controles.                                                                   |
| RNF-03.3 | El inicio del servidor Flask local debe completarse en menos de 5 segundos desde la ejecución del comando de arranque.                                                         |
| RNF-03.4 | La base de datos SQLite debe soportar el almacenamiento de al menos 500 sesiones de auditoría sin degradación perceptible del rendimiento.                                     |

---

### RNF-04 — Portabilidad

**Descripción**

La herramienta debe poder instalarse y ejecutarse en los sistemas operativos más comunes sin requerir configuración compleja ni dependencias de red.

| ID       | Requerimiento                                                                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-04.1 | La aplicación debe funcionar en Windows 10/11, Ubuntu 20.04+ y macOS 12+.                                                                                   |
| RNF-04.2 | La aplicación debe ejecutarse con Python 3.10 o superior. No debe depender de versiones específicas del sistema operativo más allá de lo que impone Python. |
| RNF-04.3 | Todas las dependencias deben estar declaradas en `requirements.txt` e instalarse mediante `pip install -r requirements.txt` sin pasos adicionales.          |
| RNF-04.4 | La aplicación no debe requerir conexión a internet durante su ejecución. Todas las librerías frontend (Bootstrap, Chart.js) deben servirse localmente.      |
| RNF-04.5 | La base de datos SQLite debe crearse e inicializarse automáticamente en el primer arranque, sin intervención del usuario.                                   |

---

### RNF-05 — Mantenibilidad

**Descripción**

El código debe estar organizado de forma modular, documentado y cubierto por pruebas automatizadas, de manera que sea comprensible para evaluadores académicos y colaboradores externos.

| ID       | Requerimiento                                                                                                                                                       |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-05.1 | El proyecto debe seguir la estructura de directorios definida en el plan (`app/models/`, `app/routes/`, `app/templates/`, `tests/`).                                |
| RNF-05.2 | La cobertura de pruebas automatizadas debe ser mayor al 70% para los módulos de scoring (RF-05) y generación de reportes (RF-07).                                   |
| RNF-05.3 | Cada módulo de rutas debe incluir docstrings que describan el propósito de la ruta, los parámetros esperados y el valor de retorno.                                 |
| RNF-05.4 | Los commits en el repositorio deben seguir el formato: `tipo(módulo): descripción breve en español` (e.g., `feat(scoring): agregar cálculo de riesgo por control`). |
| RNF-05.5 | El archivo `README.md` debe incluir instrucciones de instalación, ejecución y descripción del stack tecnológico.                                                    |

---

### RNF-06 — Confiabilidad

**Descripción**

La aplicación debe garantizar que los datos de una sesión de auditoría no se pierdan ante cierres inesperados del navegador o del servidor, y que el estado de la sesión pueda recuperarse íntegramente.

| ID       | Requerimiento                                                                                                                                                                                 |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RNF-06.1 | Las respuestas del cuestionario deben persistirse en la base de datos de forma incremental (RF-04.6), de modo que un cierre inesperado no provoque pérdida de más de una respuesta.           |
| RNF-06.2 | Al reanudar una sesión pausada, el sistema debe restaurar exactamente el estado en que se dejó: respuestas previas, control activo y progreso acumulado.                                      |
| RNF-06.3 | El sistema no debe permitir que una sesión quede en estado inconsistente (respuestas parciales sin sesión asociada). Las operaciones de escritura deben realizarse en transacciones atómicas. |
| RNF-06.4 | Ante un error interno del servidor (código 500), el sistema debe mostrar una página de error amigable sin exponer información sensible, y registrar el detalle del error en un log interno.   |

---

## 5. Casos de uso

### Diagrama de actores

```
┌─────────────────────────────────────────────────────┐
│                   SecureAudit MX                    │
│                                                     │
│  CU-01 Iniciar sesión          ◄── U01, U02, U03    │
│  CU-02 Crear sesión auditoría  ◄── U01, U02         │
│  CU-03 Ejecutar cuestionario   ◄── U01, U02         │
│  CU-04 Consultar dashboard     ◄── U01, U02, U03    │
│  CU-05 Generar reporte PDF     ◄── U01, U02, U03    │
│  CU-06 Escaneo de red          ◄── U01              │
└─────────────────────────────────────────────────────┘
```

### Resumen

| ID    | Nombre                                 | Actor principal | RF relacionados |
| ----- | -------------------------------------- | --------------- | --------------- |
| CU-01 | Registrar e iniciar sesión             | U01, U02, U03   | RF-01           |
| CU-02 | Crear y configurar sesión de auditoría | U01, U02        | RF-02, RF-03    |
| CU-03 | Ejecutar cuestionario de auditoría     | U01, U02        | RF-04, RF-05    |
| CU-04 | Consultar dashboard de resultados      | U01, U02, U03   | RF-05, RF-06    |
| CU-05 | Generar y exportar reporte             | U01, U02, U03   | RF-07           |
| CU-06 | Ejecutar escaneo de red automatizado   | U01             | RF-08           |

---

### CU-01 — Registrar e iniciar sesión

| Campo             | Detalle                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------ |
| **ID**            | CU-01                                                                                      |
| **Actores**       | U01 Auditor, U02 Técnico, U03 Directivo                                                    |
| **Precondición**  | La aplicación está en ejecución. El usuario tiene un navegador web abierto en `localhost`. |
| **Postcondición** | El usuario queda autenticado y es redirigido al dashboard principal según su rol.          |

**Flujo principal**

1. El usuario accede a la URL de la aplicación.
2. El sistema muestra el formulario de inicio de sesión.
3. El usuario ingresa su correo electrónico y contraseña.
4. El sistema valida las credenciales contra la base de datos.
5. El sistema crea una sesión activa y redirige al usuario según su rol: Auditor → lista de auditorías; Técnico → lista de auditorías parciales; Directivo → lista de reportes.

**Flujos alternativos**

| ID       | Condición                        | Respuesta del sistema                                                                                                                           |
| -------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| CU-01-A1 | Las credenciales son incorrectas | El sistema muestra un mensaje de error genérico ("Credenciales inválidas") sin especificar cuál campo es incorrecto.                            |
| CU-01-A2 | El usuario no tiene cuenta       | El usuario puede registrarse; el sistema solicita nombre, correo y contraseña. El primer usuario registrado obtiene el rol Auditor por defecto. |
| CU-01-A3 | La sesión ya está activa         | El sistema redirige directamente al dashboard sin mostrar el formulario.                                                                        |

---

### CU-02 — Crear y configurar sesión de auditoría

| Campo             | Detalle                                                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**            | CU-02                                                                                                                                         |
| **Actores**       | U01 Auditor, U02 Técnico                                                                                                                      |
| **Precondición**  | El usuario está autenticado. Existe al menos una empresa registrada en el sistema.                                                            |
| **Postcondición** | Se crea una sesión de auditoría en estado **En progreso**, asociada a la empresa seleccionada, y el sistema redirige al cuestionario (CU-03). |

**Flujo principal**

1. El usuario selecciona "Nueva auditoría" desde el menú principal.
2. El sistema muestra el formulario de configuración: selección de empresa y selección de controles a evaluar.
3. El usuario selecciona la empresa auditada.
4. El usuario elige el alcance: auditoría completa (18 controles) o parcial (selección manual de controles).
5. El usuario confirma y el sistema crea la sesión con fecha de inicio y auditor responsable.
6. El sistema redirige al primer control del cuestionario.

**Flujos alternativos**

| ID       | Condición                                              | Respuesta del sistema                                                                                 |
| -------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| CU-02-A1 | No existe ninguna empresa registrada                   | El sistema notifica al usuario y lo redirige al formulario de registro de empresa antes de continuar. |
| CU-02-A2 | U02 (Técnico) intenta crear una auditoría completa     | El sistema restringe la selección a auditorías parciales según el rol.                                |
| CU-02-A3 | Ya existe una sesión en progreso para la misma empresa | El sistema muestra una advertencia y ofrece reanudar la sesión existente o crear una nueva.           |

---

### CU-03 — Ejecutar cuestionario de auditoría

| Campo             | Detalle                                                                                                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**            | CU-03                                                                                                                                                                                                      |
| **Actores**       | U01 Auditor, U02 Técnico                                                                                                                                                                                   |
| **Precondición**  | Existe una sesión de auditoría en estado **En progreso** o **Pausada**. El usuario está autenticado.                                                                                                       |
| **Postcondición** | Las respuestas quedan persistidas en la base de datos. Si se completan todos los controles seleccionados, la sesión pasa a estado **Finalizada** y el sistema redirige al dashboard de resultados (CU-04). |

**Flujo principal**

1. El sistema presenta las preguntas del control activo, una por una o agrupadas por control.
2. El usuario selecciona la respuesta: **Sí**, **No** o **N/A**.
3. El usuario puede agregar un comentario opcional de evidencia.
4. El sistema guarda la respuesta automáticamente y actualiza la barra de progreso.
5. El usuario avanza al siguiente control o regresa a uno anterior mediante los controles de navegación.
6. Al responder el último control, el sistema solicita confirmación para finalizar la auditoría.
7. El usuario confirma y el sistema calcula el scoring final (RF-05) y actualiza el estado de la sesión a **Finalizada**.

**Flujos alternativos**

| ID       | Condición                                          | Respuesta del sistema                                                                                      |
| -------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| CU-03-A1 | El usuario cierra el navegador sin finalizar       | Las respuestas ya guardadas persisten. Al regresar, el sistema reanuda desde el último control respondido. |
| CU-03-A2 | El usuario pausa la sesión explícitamente          | El sistema actualiza el estado a **Pausada** y redirige al menú principal.                                 |
| CU-03-A3 | El usuario intenta acceder a una sesión finalizada | El sistema muestra las respuestas en modo solo lectura sin permitir modificaciones.                        |

---

### CU-04 — Consultar dashboard de resultados

| Campo             | Detalle                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| **ID**            | CU-04                                                                                          |
| **Actores**       | U01 Auditor, U02 Técnico, U03 Directivo                                                        |
| **Precondición**  | El usuario está autenticado. Existe al menos una sesión de auditoría en estado **Finalizada**. |
| **Postcondición** | El usuario visualiza el resumen de resultados de la auditoría seleccionada.                    |

**Flujo principal**

1. El usuario selecciona una sesión finalizada desde la lista de auditorías.
2. El sistema muestra el dashboard con: score global con semáforo, gráfica de radar de los 18 controles, listado de hallazgos ordenados por criticidad y resumen de cumplimiento por nivel de riesgo.
3. El usuario puede filtrar hallazgos por nivel de riesgo (Crítico, Alto, Medio, Bajo).
4. El usuario puede navegar al detalle de cada control para ver las respuestas individuales.

**Flujos alternativos**

| ID       | Condición                           | Respuesta del sistema                                                                                     |
| -------- | ----------------------------------- | --------------------------------------------------------------------------------------------------------- |
| CU-04-A1 | U03 (Directivo) accede al dashboard | El sistema muestra la misma vista pero sin opciones de edición ni botones de acción sobre las respuestas. |
| CU-04-A2 | No existen sesiones finalizadas     | El sistema muestra un estado vacío con indicación de que aún no hay auditorías completadas.               |

---

### CU-05 — Generar y exportar reporte

| Campo             | Detalle                                                                               |
| ----------------- | ------------------------------------------------------------------------------------- |
| **ID**            | CU-05                                                                                 |
| **Actores**       | U01 Auditor, U02 Técnico, U03 Directivo                                               |
| **Precondición**  | El usuario está autenticado. Existe una sesión de auditoría en estado **Finalizada**. |
| **Postcondición** | El archivo PDF o HTML es generado y descargado en el equipo del usuario.              |

**Flujo principal**

1. Desde el dashboard de resultados (CU-04) o la lista de sesiones, el usuario selecciona "Exportar reporte".
2. El sistema muestra las opciones de formato: **PDF** o **HTML**.
3. El usuario selecciona el formato deseado.
4. El sistema genera el reporte con la estructura definida en RF-07.1 y lo entrega como descarga.

**Flujos alternativos**

| ID       | Condición                                          | Respuesta del sistema                                                                                       |
| -------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| CU-05-A1 | Error durante la generación del PDF                | El sistema muestra un mensaje de error amigable (RNF-02.4) y registra el detalle en el log interno.         |
| CU-05-A2 | El usuario intenta exportar una sesión en progreso | El sistema no permite la exportación y muestra un mensaje indicando que la auditoría debe estar finalizada. |

---

### CU-06 — Ejecutar escaneo de red automatizado

| Campo             | Detalle                                                                                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ID**            | CU-06                                                                                                                                                     |
| **Actores**       | U01 Auditor                                                                                                                                               |
| **Precondición**  | El usuario está autenticado con rol Auditor. Existe una sesión de auditoría en estado **En progreso**. Nmap está instalado en el equipo.                  |
| **Postcondición** | Los resultados del escaneo quedan registrados y las preguntas correlacionadas del cuestionario son auto-completadas con estado **Pendiente de revisión**. |

**Flujo principal**

1. Desde el cuestionario activo, el usuario selecciona "Ejecutar escaneo de red".
2. El sistema muestra el aviso legal y solicita confirmación explícita (RF-08.1).
3. El usuario acepta y especifica el rango de red en formato CIDR (e.g., `192.168.1.0/24`).
4. El sistema ejecuta el escaneo mediante python-nmap y muestra el progreso en pantalla.
5. Al finalizar, el sistema correlaciona los resultados con los controles CIS correspondientes (RF-08.4) y marca las preguntas afectadas.
6. El sistema presenta un resumen de hallazgos técnicos detectados automáticamente.
7. El usuario revisa cada respuesta auto-completada y confirma o modifica según su criterio.

**Flujos alternativos**

| ID       | Condición                             | Respuesta del sistema                                                                                                                |
| -------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| CU-06-A1 | Nmap no está instalado en el equipo   | El sistema detecta la ausencia de Nmap antes de iniciar, muestra un mensaje con instrucciones de instalación y cancela la operación. |
| CU-06-A2 | El rango CIDR ingresado es inválido   | El sistema valida el formato antes de ejecutar el escaneo y solicita corrección.                                                     |
| CU-06-A3 | El escaneo no encuentra hosts activos | El sistema informa el resultado y no modifica ninguna respuesta del cuestionario.                                                    |
| CU-06-A4 | El usuario cancela durante el escaneo | El sistema detiene el proceso y descarta los resultados parciales sin afectar las respuestas existentes.                             |

---

## 6. Restricciones

Las restricciones son límites no negociables que condicionan el diseño e implementación del sistema. A diferencia de los requerimientos no funcionales, no describen atributos de calidad sino fronteras fijas derivadas de decisiones técnicas, legales o de contexto del proyecto.

| ID   | Categoría     | Descripción breve                                  |
| ---- | ------------- | -------------------------------------------------- |
| R-01 | Tecnológica   | Stack obligatorio: Python 3.10+, Flask 3.x, SQLite |
| R-02 | De alcance    | Solo CIS Controls v8 IG1                           |
| R-03 | De despliegue | Aplicación local únicamente                        |
| R-04 | Legal / ética | Escaneo de red requiere autorización previa        |
| R-05 | De recursos   | Proyecto individual, 10 semanas                    |

---

### R-01 — Stack tecnológico obligatorio

El sistema debe desarrollarse exclusivamente con el stack definido en el plan de proyecto: **Python 3.10+** como lenguaje base, **Flask 3.x** como framework web y **SQLite** como motor de base de datos. No está permitido sustituir ninguno de estos componentes por alternativas (e.g., Django en lugar de Flask, PostgreSQL en lugar de SQLite) durante el desarrollo de la versión 1.0.0. Cualquier cambio de stack requiere una nueva versión del documento de requerimientos.

Esta restricción existe porque el stack fue elegido deliberadamente para maximizar la portabilidad (ver RNF-04) y minimizar las dependencias de instalación en entornos PyME.

---

### R-02 — Alcance del marco CIS Controls v8

El sistema evalúa los **18 controles CIS v8 IG1 de forma completa**, más un subconjunto de salvaguardas IG2 seleccionadas por su relevancia para el contexto PyME mexicano. La selección de elementos IG2 incluidos debe estar documentada y justificada en el checklist de auditoría (`docs/checklist_auditoria_v1.md`). Queda fuera del alcance de la versión 1.0.0 la cobertura completa de IG2, cualquier control IG3, otros marcos de referencia (NIST CSF, ISO 27001, CMMC) o controles personalizados definidos por el usuario. El contenido del cuestionario está basado en el estándar CIS publicado en 2021 y no se actualizará dinámicamente ante revisiones futuras del marco.

---

### R-03 — Despliegue local únicamente

SecureAudit MX está diseñado para ejecutarse en un entorno local (`localhost`). No se contempla despliegue en servidores públicos, infraestructura cloud ni acceso multiusuario simultáneo desde equipos distintos en la versión 1.0.0. La base de datos SQLite reside en el mismo equipo donde corre el servidor Flask, lo que implica que los datos de auditoría no son accesibles de forma remota por diseño.

Esta restricción es intencional y está alineada con el requisito de confidencialidad de datos de las organizaciones auditadas (S06).

---

### R-04 — Autorización obligatoria para escaneo de red

El módulo de escaneo de red (RF-08, CU-06) solo puede ejecutarse con autorización expresa del auditor, quien asume la responsabilidad legal del uso de la herramienta sobre la red objetivo. El sistema no puede —ni debe— ejecutar escaneos de forma automática, programada o sin confirmación activa. El uso del módulo en redes ajenas sin autorización escrita del propietario puede constituir un delito conforme a la legislación mexicana vigente (Código Penal Federal, Título Noveno, Capítulo II).

---

### R-05 — Proyecto individual con recursos acotados

SecureAudit MX es desarrollado por un único desarrollador (**Roberto Pérez Rosales**) en un período de **10 semanas** como proyecto de portafolio académico. Las decisiones de diseño y priorización de funcionalidades deben considerar esta restricción de recursos. Las funcionalidades marcadas con prioridad **Media** en las secciones 3 y 4 pueden posponerse a versiones futuras si el tiempo de desarrollo lo requiere, sin comprometer el MVP definido en las fases 2 y 3 del plan de proyecto.

---

_Documento generado como parte del portafolio académico y profesional — Ingeniería en Software, Universidad Tecnológica de Ciudad Juárez._
