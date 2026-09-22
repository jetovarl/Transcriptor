# Transcriptor

Convierte audios y videos en texto dentro de su propio computador. Sirve para grabaciones de reuniones, notas de voz de WhatsApp, audiencias y entrevistas.

El audio no sale de su equipo. No se sube a ningún servicio ni se envía a ningún proveedor; lo único que viaja por internet es la descarga del modelo la primera vez que lo usa. Por eso puede transcribir material de clientes sin pedirle permiso a nadie.

---

## Instalación (una sola vez)

1. Descargue esta carpeta y déjela donde quiera, por ejemplo en el Escritorio.
2. Haga doble clic en **`instalar (primera vez).bat`** y espere a que termine.
3. Si le avisa que no encuentra Python, instálelo desde [python.org/downloads](https://www.python.org/downloads/) y **marque la casilla «Add python.exe to PATH»** en la primera pantalla del instalador. Después vuelva al paso 2.

## Uso diario

1. Copie sus audios o videos a la carpeta **`Entrada`**.
2. Haga doble clic en **`Transcribir (doble clic).bat`**.
3. Cuando termine, el texto queda en **`Salida`** y los archivos originales se mueven a **`Hecho`**.

Por cada archivo se generan dos: un `.txt` con el texto corrido para leer o pegar en un documento, y un `.srt` con las marcas de tiempo, que sirve para subtítulos y para ubicar un pasaje dentro de la grabación.

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
| `python transcribir.py --no-srt` | Genera solo el `.txt` |

También puede arrastrar esas opciones al `.bat`, o crear un acceso directo con la opción escrita al final.

## Si algo sale mal

**No pasa nada al hacer doble clic.** Falta Python o faltó la instalación; corra `instalar (primera vez).bat`.

**Un archivo falla y los demás siguen.** El que falla se queda en `Entrada` y al final aparece en la lista de pendientes. Suele ser un archivo dañado o incompleto; ábralo primero en el reproductor para confirmar que suena.

**Dice que no reconoció voz.** El audio está mudo o demasiado bajo. También pasa con grabaciones donde solo hay ruido de fondo.

**El texto sale en otro idioma o sin sentido.** El audio no estaba en español; use `--lang auto` o indique el idioma.

**El texto tiene errores en nombres propios y cifras.** Es normal en cualquier transcripción automática. Revise siempre contra el audio antes de usar el texto en un documento que salga de la oficina; el `.srt` ayuda a saltar al minuto exacto.

## Un aviso sobre las carpetas

`Entrada`, `Hecho` y `Salida` guardan material de trabajo y por eso nunca se suben a este repositorio. Lo que usted transcriba se queda en su computador.
