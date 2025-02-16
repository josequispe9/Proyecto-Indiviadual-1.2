# Sistema de Recomendación de Películas basado en Similitud del Coseno

![Licencia](https://img.shields.io/badge/licencia-MIT-blue.svg) <!-- Cambia la licencia si es necesario -->

Este proyecto es un sistema de recomendación de películas que utiliza técnicas de **similitud del coseno**  para analizar similitudes entre películas basadas en características como género, actores y descripciones textuales. El sistema está diseñado para ser eficiente y escalable, y se implementa como una **API RESTful** utilizando **Flask**, desplegada en **Render** para garantizar disponibilidad y escalabilidad.

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Despliegue](#despliegue)
- [Validación del Modelo](#validación-del-modelo)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Objetivo

El objetivo de este proyecto es desarrollar un sistema de recomendación eficiente basado en análisis de similitud de contenido para plataformas de streaming. El sistema utiliza similitud del coseno para proporcionar recomendaciones personalizadas y relevantes a los usuarios.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal para el desarrollo del modelo y la API.
- **Flask**: Framework para crear la API RESTful.
- **Pandas y NumPy**: Para el procesamiento y limpieza de datos.
- **Scikit-learn**: Para calcular la similitud del coseno.
- **Render**: Plataforma de despliegue en la nube.

## Proceso de Desarrollo

1. **Preprocesamiento de Datos**:
   - Limpieza y normalización de datos (eliminación de valores nulos, duplicados, etc.).
   - Normalización de texto para mejorar la calidad del entrenamiento del modelo.

2. **Modelo de Recomendación**:
   - Cálculo de similitud del coseno entre películas basado en género, actores y descripciones.

3. **API RESTful**:
   - Desarrollo de una API con Flask para permitir consultas en tiempo real.

4. **Despliegue**:
   - Implementación del sistema en Render para garantizar escalabilidad y disponibilidad.

## Despliegue

El sistema está desplegado en **Render** para garantizar escalabilidad y disponibilidad. Puedes acceder a la API en el siguiente enlace: [Enlace a la API en Render](https://tuenlace.render.com).


## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del proyecto.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Añade nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

Asegúrate de incluir pruebas unitarias y documentación actualizada.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
