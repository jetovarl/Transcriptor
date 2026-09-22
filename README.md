# Transcriptor

Convierte audios y videos en texto dentro de su propio computador. Sirve para grabaciones de reuniones, notas de voz de WhatsApp, audiencias y entrevistas.

El audio no sale de su equipo. No se sube a ningún servicio ni se envía a ningún proveedor; lo único que viaja por internet es la descarga del modelo la primera vez que lo usa. Por eso puede transcribir material de clientes sin pedirle permiso a nadie.

---

## Cómo descargar esta carpeta

Si nunca ha usado GitHub, no se preocupe: no hay que saber programar ni entender nada de lo que aparece en esta página. GitHub es un archivador donde se guardan programas y se lleva la cuenta de cada cambio, y de aquí se descarga igual que cualquier archivo adjunto.

1. Arriba a la derecha de la lista de archivos hay un botón verde que dice **`Code`**. Óprimalo.
2. Se abre una lista pequeña. Abajo de todo está **`Download ZIP`**. Esa es la que sirve; las demás son para programadores.
3. El archivo comprimido queda en su carpeta de Descargas.
4. **Este paso es el que más se olvida.** Haga clic derecho sobre el archivo descargado y escoja **«Extraer todo»**. Windows deja mirar dentro del comprimido con doble clic y eso engaña, porque parece que ya estuviera listo; si trabaja desde adentro del comprimido, el programa no funciona.
5. Deje la carpeta que resulta donde quiera, por ejemplo en el Escritorio, y renómbrela a algo corto como `Transcriptor`.

Si al abrir alguno de los archivos Windows muestra una advertencia azul diciendo que protegió el equipo, oprima **«Más información»** y después **«Ejecutar de todas formas»**. Es la desconfianza de rutina de Windows con lo que viene de internet, y ocurre una sola vez por archivo.

## Instalación (una sola vez)

1. Abra la carpeta que acaba de extraer.
2. Haga doble clic en **`instalar (primera vez).bat`** y espere a que termine.
3. Si le avisa que no encuentra Python, instálelo desde [python.org/downloads](https://www.python.org/downloads/) y **marque la casilla «Add python.exe to PATH»** en la primera pantalla del instalador. Después vuelva al paso 2.

## Uso diario

1. Copie sus audios o videos a la carpeta **`Entrada`**.
2. Haga doble clic en **`Transcribir (doble clic).bat`**.
3. Pulse **Enter** cuando aparezca el menú, o escoja una de las otras tres opciones.
4. Al terminar se abre sola la carpeta **`Salida`** con los textos. Los audios ya procesados quedan guardados en **`Hecho`**.

Por cada grabación queda un solo archivo, un `.txt` con el texto corrido, listo para leer o pegar en un documento.

El menú ofrece tres alternativas a la opción normal:

| Opción | Cuándo usarla |
|---|---|
| **2**, máxima precisión | Audio difícil: eco, varias personas hablando encima, ruido de fondo, una llamada de mala calidad. Demora unas tres veces más y se equivoca bastante menos |
| **3**, otro idioma | El audio no está en español. Se escribe el código del idioma, o `auto` para que lo detecte solo |
| **4**, marcas de tiempo | El `.txt` lleva `[hh:mm:ss]` al inicio de cada párrafo. Para actas, y para volver al minuto exacto de la grabación cuando hay que verificar algo |

La primera transcripción demora más que las demás porque descarga el modelo, cerca de 1 GB. Las siguientes arrancan de inmediato.

## Qué archivos acepta

Video: `.mp4` `.mkv` `.mov` `.avi` `.webm` `.m4v` `.flv` `.wmv` `.mpg` `.mpeg` `.3gp`

Audio: `.mp3` `.wav` `.m4a` `.aac` `.ogg` `.flac` `.wma` `.opus` `.amr` `.aiff`

Las notas de voz de WhatsApp (`.ogg`) funcionan tal como se descargan, sin convertirlas.

## Cuánto demora

Sobre un computador sin tarjeta de video dedicada, calcule más o menos un tercio de la duración del audio: una reunión de una hora sale en unos veinte minutos. Si el equipo tiene tarjeta NVIDIA, el programa la usa solo y baja a unos pocos minutos.

## Opciones

Para usarlas hay que correrlo desde la terminal, parado en esta carpeta:

| Comando | Para qué |
|---|---|
| `python transcribir.py` | Lo mismo que el doble clic: español, modelo rápido |
| `python transcribir.py --model large-v3` | Máxima precisión, bastante más lento |
| `python transcribir.py --lang auto` | Detecta el idioma de cada archivo |
| `python transcribir.py --lang en` | Fuerza inglés |
| `python transcribir.py --con-tiempos` | El `.txt` lleva `[hh:mm:ss]` al inicio de cada línea |
| `python transcribir.py --srt` | Genera además un `.srt` de subtítulos |

También puede arrastrar esas opciones al `.bat`, o crear un acceso directo con la opción escrita al final.

## Si algo sale mal

**No pasa nada al hacer doble clic.** Falta Python o faltó la instalación; corra `instalar (primera vez).bat`.

**Un archivo falla y los demás siguen.** El que falla se queda en `Entrada` y al final aparece en la lista de pendientes. Suele ser un archivo dañado o incompleto; ábralo primero en el reproductor para confirmar que suena.

**Dice que no reconoció voz.** El audio está mudo o demasiado bajo. También pasa con grabaciones donde solo hay ruido de fondo.

**El texto sale en otro idioma o sin sentido.** El audio no estaba en español; use `--lang auto` o indique el idioma.

**El texto tiene errores en nombres propios y cifras.** Es normal en cualquier transcripción automática. Revise siempre contra el audio antes de usar el texto en un documento que salga de la oficina; la opción **4** del menú, la de marcas de tiempo, le permite saltar al minuto exacto de lo que quiere confirmar.

## Un aviso sobre las carpetas

`Entrada`, `Hecho` y `Salida` guardan material de trabajo y por eso nunca se suben a este repositorio. Lo que usted transcriba se queda en su computador.
