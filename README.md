# socio-hackathon 

## Configuracion del entorno y  ejecucion de los scripts.
### Requesitos previos.

Contar con **PIP** y **VENV** en tu sistema antes de iniciar.

> [!TIP]
> **Sistemas basados en APT (Ubuntu/Debian):**
> Puedes instalar los paquetes de Python ejecutando:
>
> ```bash
> sudo apt update && sudo apt install python3-venv python3-pip -y
> ```

## Inicio del entorno.

1. `make venv`
2. `make install`

## Ejecucion de los scripts.

1. `make dim1`
2. `make dim2`
3. `make dim3`

## Lista de comandos.

> [!WARNING]
> Usar con precaución **`make clean`**, ya que elimina por completo el entorno virtual (`.venv`) y requiere volver a ejecutar `make install`.

| Comando        | Descripción                                                                                                            |
| :------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `make venv`    | Crea el entorno virtual de Python en el directorio `.venv`.                                                            |
| `make install` | Crea el entorno virtual (si aún no existe) e instala las dependencias listadas en `requirements.txt`.                  |
| `make dim1`    | Ejecuta `scripts/ind_dim1.py` para calcular el índice de **Seguridad Económica**.                                      |
| `make dim2`    | Ejecuta `scripts/ind_dim2.py` para procesar y calcular los indicadores de la **Bienestar estructural**.                |
| `make dim3`    | Ejecuta `scripts/ind_dim3.py` para procesar y calcular los indicadores de la **Integración social**.                   |
| `make clean`   | Elimina el directorio del entorno virtual (`.venv`).                                                                   |