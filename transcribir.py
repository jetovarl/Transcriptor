#!/usr/bin/env python3
"""
transcribir.py - Transcripción por carpetas, todo en su computador.

Estructura de trabajo (se crea sola la primera vez):

    Transcript/
        transcribir.py
        Entrada/   <- ponga aquí los videos o audios a transcribir
        Hecho/     <- los originales ya transcritos se mueven aquí
        Salida/    <- quedan los .txt y .srt con nombre  <archivo>_transcript

Flujo: lee todo lo que haya en Entrada, transcribe, deja el texto en Salida y mueve
el original a Hecho. Si un archivo falla, se queda en Entrada para reintentar.

Uso normal: doble clic en «Transcribir (doble clic).bat».

Desde la terminal, parado en esta carpeta:
    python transcribir.py                     # todo lo de Entrada, español, modelo turbo
    python transcribir.py --model large-v3    # máxima precisión (bastante más lento)
    python transcribir.py --lang auto         # detectar el idioma de cada audio
    python transcribir.py --lang en           # forzar inglés
    python transcribir.py --con-tiempos       # el .txt lleva [hh:mm:ss] en cada línea
    python transcribir.py --no-srt            # generar solo .txt
"""

import argparse
import shutil
import sys
import time
from pathlib import Path

# La consola de Windows no siempre habla UTF-8 y los nombres con tilde rompen la
# corrida al imprimirlos. Esto lo evita antes de escribir la primera línea.
if sys.platform == "win32":
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

AYUDA_INSTALACION = """
No está instalado el motor de transcripción (faster-whisper).

Ciérrelo, haga doble clic en «instalar (primera vez).bat» y vuelva a intentar.

Si prefiere hacerlo a mano, abra una terminal en esta carpeta y corra:
    pip install -r requirements.txt
"""

try:
    from faster_whisper import WhisperModel
except ImportError:
    print(AYUDA_INSTALACION)
    sys.exit(1)

# El script trabaja relativo a SU PROPIA ubicación (donde lo guarde).
BASE = Path(__file__).resolve().parent
ENTRADA = BASE / "Entrada"
HECHO = BASE / "Hecho"
SALIDA = BASE / "Salida"

EXT_VIDEO = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v", ".flv", ".wmv", ".mpg", ".mpeg", ".3gp"}
EXT_AUDIO = {".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma", ".opus", ".amr", ".aiff"}
EXTENSIONES = EXT_VIDEO | EXT_AUDIO

MODELOS_CONOCIDOS = {
    "tiny", "base", "small", "medium", "large", "large-v1", "large-v2", "large-v3",
    "large-v3-turbo", "turbo", "distil-large-v3",
}

# Marcas de OneDrive para un archivo que figura en la carpeta pero vive en la nube.
ATRIBUTO_EN_LA_NUBE = 0x1000 | 0x400000  # OFFLINE | RECALL_ON_DATA_ACCESS


def fmt_tiempo(segundos: float) -> str:
    """Segundos (float) -> formato SRT  HH:MM:SS,mmm"""
    ms = int(round(segundos * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_duracion(segundos: float) -> str:
    """Segundos -> 1 h 04 min / 4 min 12 s / 38 s, para leer de un vistazo."""
    segundos = int(segundos)
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    if h:
        return f"{h} h {m:02d} min"
    if m:
        return f"{m} min {s:02d} s"
    return f"{s} s"


def destino_unico(carpeta: Path, nombre: str) -> Path:
    """Evita sobrescribir: si ya existe, agrega _1, _2, ..."""
    destino = carpeta / nombre
    if not destino.exists():
        return destino
    stem, suf = destino.stem, destino.suffix
    i = 1
    while (carpeta / f"{stem}_{i}{suf}").exists():
        i += 1
    return carpeta / f"{stem}_{i}{suf}"


def nombre_salida(stem: str) -> str:
    """
    Nombre base para el .txt y el .srt de un archivo, sin pisar transcripciones
    anteriores. El .txt y el .srt de una misma corrida comparten el sufijo.
    """
    nombre = f"{stem}_transcript"
    libre = lambda n: not (SALIDA / f"{n}.txt").exists() and not (SALIDA / f"{n}.srt").exists()
    if libre(nombre):
        return nombre
    i = 1
    while not libre(f"{nombre}_{i}"):
        i += 1
    return f"{nombre}_{i}"


def esta_en_la_nube(archivo: Path) -> bool:
    """True si OneDrive tiene el archivo liberado y habrá que bajarlo antes de leerlo."""
    try:
        return bool(getattr(archivo.stat(), "st_file_attributes", 0) & ATRIBUTO_EN_LA_NUBE)
    except OSError:
        return False


def elegir_motor(preferencia: str) -> tuple[str, str]:
    """Devuelve (dispositivo, precisión): la tarjeta de video si la hay, si no el procesador."""
    if preferencia == "cpu":
        return "cpu", "int8"
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda", "float16"
    except Exception:
        pass
    if preferencia == "gpu":
        print("   [aviso] No se detectó tarjeta de video compatible; se usa el procesador.")
    return "cpu", "int8"


def procesar(archivo: Path, modelo, lang: str | None, hacer_srt: bool, con_tiempos: bool) -> bool:
    print(f"\n=> {archivo.name}")
    if esta_en_la_nube(archivo):
        print("   (está solo en OneDrive; se descarga primero, puede demorar)")
    t0 = time.time()

    try:
        segmentos, info = modelo.transcribe(
            str(archivo),
            language=lang,             # None = detectar el idioma
            beam_size=5,
            vad_filter=True,           # filtra silencios -> menos alucinaciones en pausas
        )
        if lang is None:
            print(f"   Idioma detectado: {info.language} ({info.language_probability:.0%} de certeza)")

        lineas_txt, lineas_srt = [], []
        for i, seg in enumerate(segmentos, start=1):
            texto = seg.text.strip()
            if not texto:
                continue
            marca = f"[{fmt_tiempo(seg.start)[:8]}] " if con_tiempos else ""
            lineas_txt.append(marca + texto)
            lineas_srt.append(f"{i}\n{fmt_tiempo(seg.start)} --> {fmt_tiempo(seg.end)}\n{texto}\n")
            if info.duration:
                pct = min(100.0, seg.end / info.duration * 100)
                print(f"\r   {pct:5.1f}%  ({fmt_tiempo(seg.end)[:8]} de {fmt_duracion(info.duration)})",
                      end="", flush=True)
        print()  # cierra la línea de progreso

        if not lineas_txt:
            print("   [aviso] No se reconoció voz en este archivo; queda en Entrada.")
            return False

        base = nombre_salida(archivo.stem)
        (SALIDA / f"{base}.txt").write_text("\n".join(lineas_txt), encoding="utf-8")
        if hacer_srt:
            (SALIDA / f"{base}.srt").write_text("\n".join(lineas_srt), encoding="utf-8")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"\n   [ERROR] No se pudo transcribir, queda en Entrada: {e}")
        return False

    # Mover el original a Hecho (solo llegamos aquí si la transcripción salió bien).
    try:
        shutil.move(str(archivo), str(destino_unico(HECHO, archivo.name)))
    except Exception as e:
        print(f"   [aviso] Transcrito, pero no pude mover a Hecho: {e}")

    extra = f" + {base}.srt" if hacer_srt else ""
    print(f"   Listo: {base}.txt{extra}   ({fmt_duracion(time.time() - t0)})")
    return True


def main() -> int:
    p = argparse.ArgumentParser(description="Transcribe Entrada/ -> Salida/, archiva en Hecho/")
    p.add_argument("--model", default="turbo",
                   help="turbo (rápido, por omisión) | large-v3 (máxima precisión, más lento)")
    p.add_argument("--lang", default="es",
                   help="Idioma del audio: es (por omisión), en, pt... o «auto» para detectarlo")
    p.add_argument("--no-srt", action="store_true", help="Generar solo .txt (sin .srt)")
    p.add_argument("--con-tiempos", action="store_true",
                   help="El .txt lleva la marca [hh:mm:ss] al inicio de cada línea")
    p.add_argument("--dispositivo", default="auto", choices=("auto", "cpu", "gpu"),
                   help="Dónde correr el modelo (por omisión: la tarjeta de video si la hay)")
    a = p.parse_args()

    for c in (ENTRADA, HECHO, SALIDA):
        c.mkdir(parents=True, exist_ok=True)

    todo = [f for f in ENTRADA.iterdir() if f.is_file() and not f.name.startswith(".")]
    archivos = sorted(f for f in todo if f.suffix.lower() in EXTENSIONES)
    ignorados = sorted(f.name for f in todo if f.suffix.lower() not in EXTENSIONES)

    if ignorados:
        print("Se ignoran (no son audio ni video): " + ", ".join(ignorados) + "\n")

    if not archivos:
        print(f"No hay videos ni audios en:\n   {ENTRADA}\n\nMeta archivos ahí y vuelva a correr.")
        return 0

    if a.model not in MODELOS_CONOCIDOS:
        print(f"[aviso] «{a.model}» no es uno de los modelos habituales; se intentará de todos modos.\n")

    lang = None if a.lang.lower() in ("auto", "detectar") else a.lang
    dispositivo, precision = elegir_motor(a.dispositivo)

    print(f"Cargando modelo «{a.model}» en {'la tarjeta de video' if dispositivo == 'cuda' else 'el procesador'}.")
    print("La primera vez se descarga (alrededor de 1 GB) y puede tardar varios minutos.")
    try:
        modelo = WhisperModel(a.model, device=dispositivo, compute_type=precision)
    except Exception as e:
        print(f"\n[ERROR] No se pudo cargar el modelo «{a.model}»: {e}")
        print("Revise que tenga internet la primera vez, o pruebe con  --model small")
        return 1

    print(f"Modelo listo. {len(archivos)} archivo(s) en Entrada.\n" + "-" * 50)

    t0 = time.time()
    ok, fallidos = 0, []
    for f in archivos:
        if procesar(f, modelo, lang, not a.no_srt, a.con_tiempos):
            ok += 1
        else:
            fallidos.append(f.name)

    print("-" * 50)
    print(f"Terminado: {ok} de {len(archivos)} transcrito(s) en {fmt_duracion(time.time() - t0)}.")
    if fallidos:
        print("Quedaron en Entrada para reintentar:")
        for nombre in fallidos:
            print(f"   - {nombre}")
    print(f"Textos en: {SALIDA}")
    return 0 if not fallidos else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelado. Lo que no alcanzó a transcribirse sigue en Entrada.")
        sys.exit(130)
