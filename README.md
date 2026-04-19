# Sistema de Gestión de Servicios de Refrigeración

#### Video Demo: [<URL AQUÍ>](https://youtu.be/5t6d7za09V0)

#### Description:

Este proyecto refleja mi interés en combinar programación con mi trabajo en refrigeración (Actualmente soy técnico en refrigeración y vivo de eso).

Este programa web consiste en una aplicación web desarrollada con Flask que permite gestionar clientes, servicios técnicos y productos dentro de un negocio de refrigeración. La aplicación fue diseñada con el objetivo de resolver una necesidad real: llevar un control organizado de los trabajos realizados a cada cliente, así como de los productos utilizados en el proceso.

El sistema permite registrar clientes con información básica como nombre, teléfono, dirección y correo electrónico. A cada cliente se le pueden asociar múltiples servicios técnicos, como limpieza, reparación, instalación o carga de gas, lo que permite llevar un historial completo de intervenciones realizadas.

Una de las funcionalidades más importantes es la visualización del historial de servicios por cliente. Esto facilita el seguimiento de trabajos previos, permitiendo conocer qué tipo de servicio se realizó, en qué fecha y con qué observaciones. Esta característica es especialmente útil en el ámbito de la refrigeración, donde el mantenimiento periódico es clave.

La aplicación también incluye un módulo de productos, donde se pueden registrar elementos con su nombre, precio y stock disponible. Aunque actualmente este módulo es básico, sienta las bases para futuras mejoras como la integración de productos utilizados en cada servicio técnico o el registro de ventas por cliente.

En cuanto a la seguridad, el sistema implementa un mecanismo de autenticación mediante login. Las contraseñas no se almacenan en texto plano, sino que se utilizan funciones de hash para proteger la información de los usuarios. Además, se emplean sesiones para restringir el acceso a las distintas rutas de la aplicación, garantizando que solo usuarios autenticados puedan interactuar con el sistema.

Desde el punto de vista técnico, el proyecto fue desarrollado utilizando Flask como framework principal, SQLite como base de datos y Bootstrap para el diseño de la interfaz. Se optó por SQLite por su simplicidad y facilidad de integración, lo cual resulta ideal para proyectos pequeños o medianos.

Durante el desarrollo, se tomaron decisiones importantes relacionadas con la gestión de datos. Por ejemplo, al eliminar un cliente, también se eliminan manualmente sus servicios asociados para evitar registros huérfanos en la base de datos. Esta solución asegura la integridad de los datos sin necesidad de implementar configuraciones más avanzadas como ON DELETE CASCADE.

El proyecto fue construido de manera incremental, comenzando con funcionalidades básicas y evolucionando progresivamente hacia un sistema más completo. Este enfoque permitió comprender en profundidad conceptos clave como rutas en Flask, manejo de formularios, consultas SQL, relaciones entre tablas y control de sesiones.

Como posibles mejoras futuras, se podrían implementar funcionalidades como la asociación de productos a servicios o clientes, generación de reportes, filtros de búsqueda avanzados o una interfaz más robusta para la administración del sistema.

En conclusión, este proyecto no solo cumple con los requisitos del curso CS50x, sino que también representa una herramienta funcional que puede ser utilizada en un entorno real de trabajo dentro del área de refrigeración.

Obs: Yo también soy técnico en refrigeración y esta herramienta la iré usando, probando y agregando más y más funcionalidades a medida que las necesite.
