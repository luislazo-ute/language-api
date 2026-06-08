#!/usr/bin/env python3
"""
Seeder remoto para la API de idiomas.

Apunta a https://lazo-idiomas.uaeftt-ute.site, hace login como admin y crea
toda la jerarquia Language -> Level -> Lesson -> Exercise vía la API REST.

Uso:
    python3 scripts/seed_remote.py
"""
import json
import random
import sys
import urllib.request
import urllib.error

BASE = "https://lazo-idiomas.uaeftt-ute.site/api"
USER = "admin"
PASSWORD = "admin"

TOKEN = None


def call(method, path, payload=None, auth=True):
    url = f"{BASE}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if auth and TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode()
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ERROR {e.code} en {method} {path}: {body[:300]}")
        return e.code, None


def login():
    global TOKEN
    status, data = call(
        "POST", "/auth/login/",
        {"username": USER, "password": PASSWORD}, auth=False
    )
    if status != 200:
        print("No se pudo iniciar sesion. Abortando.")
        sys.exit(1)
    TOKEN = data["access"]
    print("Login OK.")


def create(path, payload, label):
    status, data = call("POST", path, payload)
    if status in (200, 201):
        print(f"  + {label} (id={data['id']})")
        return data["id"]
    print(f"  ! Fallo creando {label}")
    return None


# ---------------------------------------------------------------------------
# Contenido del curriculo.
#
# Cada idioma define 3 temas de vocabulario (uno por nivel) y cada tema tiene
# dos lecciones. El vocabulario es una lista de pares (español, objetivo).
# A partir del vocabulario se generan automaticamente los ejercicios.
# ---------------------------------------------------------------------------

LANGUAGES = {
    "en": {
        "nombre": "Inglés",
        "bandera": "🇬🇧",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "hello"), ("adiós", "goodbye"),
                    ("gracias", "thank you"), ("por favor", "please"),
                    ("buenos días", "good morning"), ("sí", "yes"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "one"), ("dos", "two"), ("tres", "three"),
                    ("rojo", "red"), ("azul", "blue"), ("verde", "green"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "mother"), ("padre", "father"),
                    ("hermano", "brother"), ("hermana", "sister"),
                    ("hijo", "son"), ("hija", "daughter"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "water"), ("pan", "bread"), ("leche", "milk"),
                    ("manzana", "apple"), ("café", "coffee"), ("queso", "cheese"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "airport"), ("hotel", "hotel"),
                    ("billete", "ticket"), ("equipaje", "luggage"),
                    ("estación", "station"), ("mapa", "map"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "work"), ("reunión", "meeting"),
                    ("ordenador", "computer"), ("jefe", "boss"),
                    ("horario", "schedule"), ("oficina", "office"),
                ]),
            ],
        },
    },
    "fr": {
        "nombre": "Francés",
        "bandera": "🇫🇷",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "bonjour"), ("adiós", "au revoir"),
                    ("gracias", "merci"), ("por favor", "s'il vous plaît"),
                    ("buenas noches", "bonsoir"), ("sí", "oui"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "un"), ("dos", "deux"), ("tres", "trois"),
                    ("rojo", "rouge"), ("azul", "bleu"), ("verde", "vert"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "mère"), ("padre", "père"),
                    ("hermano", "frère"), ("hermana", "sœur"),
                    ("hijo", "fils"), ("hija", "fille"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "eau"), ("pan", "pain"), ("leche", "lait"),
                    ("manzana", "pomme"), ("café", "café"), ("queso", "fromage"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "aéroport"), ("hotel", "hôtel"),
                    ("billete", "billet"), ("equipaje", "bagages"),
                    ("estación", "gare"), ("mapa", "carte"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "travail"), ("reunión", "réunion"),
                    ("ordenador", "ordinateur"), ("jefe", "patron"),
                    ("horario", "horaire"), ("oficina", "bureau"),
                ]),
            ],
        },
    },
    "de": {
        "nombre": "Alemán",
        "bandera": "🇩🇪",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "hallo"), ("adiós", "tschüss"),
                    ("gracias", "danke"), ("por favor", "bitte"),
                    ("buenos días", "guten Morgen"), ("sí", "ja"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "eins"), ("dos", "zwei"), ("tres", "drei"),
                    ("rojo", "rot"), ("azul", "blau"), ("verde", "grün"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "Mutter"), ("padre", "Vater"),
                    ("hermano", "Bruder"), ("hermana", "Schwester"),
                    ("hijo", "Sohn"), ("hija", "Tochter"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "Wasser"), ("pan", "Brot"), ("leche", "Milch"),
                    ("manzana", "Apfel"), ("café", "Kaffee"), ("queso", "Käse"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "Flughafen"), ("hotel", "Hotel"),
                    ("billete", "Fahrkarte"), ("equipaje", "Gepäck"),
                    ("estación", "Bahnhof"), ("mapa", "Karte"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "Arbeit"), ("reunión", "Besprechung"),
                    ("ordenador", "Computer"), ("jefe", "Chef"),
                    ("horario", "Zeitplan"), ("oficina", "Büro"),
                ]),
            ],
        },
    },
    "it": {
        "nombre": "Italiano",
        "bandera": "🇮🇹",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "ciao"), ("adiós", "arrivederci"),
                    ("gracias", "grazie"), ("por favor", "per favore"),
                    ("buenos días", "buongiorno"), ("sí", "sì"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "uno"), ("dos", "due"), ("tres", "tre"),
                    ("rojo", "rosso"), ("azul", "blu"), ("verde", "verde"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "madre"), ("padre", "padre"),
                    ("hermano", "fratello"), ("hermana", "sorella"),
                    ("hijo", "figlio"), ("hija", "figlia"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "acqua"), ("pan", "pane"), ("leche", "latte"),
                    ("manzana", "mela"), ("café", "caffè"), ("queso", "formaggio"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "aeroporto"), ("hotel", "albergo"),
                    ("billete", "biglietto"), ("equipaje", "bagaglio"),
                    ("estación", "stazione"), ("mapa", "mappa"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "lavoro"), ("reunión", "riunione"),
                    ("ordenador", "computer"), ("jefe", "capo"),
                    ("horario", "orario"), ("oficina", "ufficio"),
                ]),
            ],
        },
    },
    "pt": {
        "nombre": "Portugués",
        "bandera": "🇧🇷",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "olá"), ("adiós", "tchau"),
                    ("gracias", "obrigado"), ("por favor", "por favor"),
                    ("buenos días", "bom dia"), ("sí", "sim"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "um"), ("dos", "dois"), ("tres", "três"),
                    ("rojo", "vermelho"), ("azul", "azul"), ("verde", "verde"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "mãe"), ("padre", "pai"),
                    ("hermano", "irmão"), ("hermana", "irmã"),
                    ("hijo", "filho"), ("hija", "filha"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "água"), ("pan", "pão"), ("leche", "leite"),
                    ("manzana", "maçã"), ("café", "café"), ("queso", "queijo"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "aeroporto"), ("hotel", "hotel"),
                    ("billete", "bilhete"), ("equipaje", "bagagem"),
                    ("estación", "estação"), ("mapa", "mapa"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "trabalho"), ("reunión", "reunião"),
                    ("ordenador", "computador"), ("jefe", "chefe"),
                    ("horario", "horário"), ("oficina", "escritório"),
                ]),
            ],
        },
    },
    "ja": {
        "nombre": "Japonés",
        "bandera": "🇯🇵",
        "lessons": {
            "A1": [
                ("Saludos y cortesía", "👋", [
                    ("hola", "こんにちは"), ("adiós", "さようなら"),
                    ("gracias", "ありがとう"), ("por favor", "お願いします"),
                    ("buenos días", "おはよう"), ("sí", "はい"),
                ]),
                ("Números y colores", "🔢", [
                    ("uno", "いち"), ("dos", "に"), ("tres", "さん"),
                    ("rojo", "あか"), ("azul", "あお"), ("verde", "みどり"),
                ]),
            ],
            "A2": [
                ("La familia", "👨‍👩‍👧", [
                    ("madre", "はは"), ("padre", "ちち"),
                    ("hermano", "あに"), ("hermana", "あね"),
                    ("hijo", "むすこ"), ("hija", "むすめ"),
                ]),
                ("Comida y bebida", "🍎", [
                    ("agua", "みず"), ("pan", "パン"), ("leche", "ぎゅうにゅう"),
                    ("manzana", "りんご"), ("café", "コーヒー"), ("queso", "チーズ"),
                ]),
            ],
            "B1": [
                ("Viajes", "✈️", [
                    ("aeropuerto", "くうこう"), ("hotel", "ホテル"),
                    ("billete", "きっぷ"), ("equipaje", "にもつ"),
                    ("estación", "えき"), ("mapa", "ちず"),
                ]),
                ("Trabajo y rutina", "💼", [
                    ("trabajo", "しごと"), ("reunión", "かいぎ"),
                    ("ordenador", "コンピューター"), ("jefe", "じょうし"),
                    ("horario", "スケジュール"), ("oficina", "オフィス"),
                ]),
            ],
        },
    },
}

LEVELS = [
    ("A1", "Principiante", 1),
    ("A2", "Básico", 2),
    ("B1", "Intermedio", 3),
]


def build_exercises(lang_nombre, vocab):
    """Genera un ejercicio por cada palabra del vocabulario de la leccion.

    Alterna opcion multiple y traduccion, y baraja las opciones para que la
    respuesta correcta no quede siempre en la misma posicion.
    """
    exercises = []
    todas = [v[1] for v in vocab]
    for es, target in vocab:
        # Todos de opcion multiple: 3 distractores + la correcta, barajadas.
        distractors = [t for t in todas if t != target]
        random.shuffle(distractors)
        options = distractors[:3] + [target]
        random.shuffle(options)
        exercises.append({
            "tipo": "multiple_choice",
            "pregunta": f"¿Cómo se dice «{es}» en {lang_nombre.lower()}?",
            "opciones": options,
            "respuesta_correcta": target,
            "puntos": 10,
        })
    return exercises


def wipe_languages():
    """Borra todos los idiomas (cascada elimina niveles/lecciones/ejercicios)."""
    status, data = call("GET", "/languages/?page_size=1000", auth=False)
    results = data.get("results", data) if data else []
    if not results:
        print("No hay idiomas previos que borrar.")
        return
    for lang in results:
        st, _ = call("DELETE", f"/languages/{lang['id']}/")
        marca = "ok" if st in (200, 204) else f"FALLO {st}"
        print(f"  - borrado {lang['nombre']} ({marca})")


def main():
    login()
    print("\n--- Limpiando catálogo anterior ---")
    wipe_languages()
    totals = {"lang": 0, "level": 0, "lesson": 0, "ex": 0}

    for codigo, info in LANGUAGES.items():
        print(f"\n=== {info['bandera']} {info['nombre']} ({codigo}) ===")
        lang_id = create("/languages/", {
            "nombre": info["nombre"],
            "codigo": codigo,
            "bandera_emoji": info["bandera"],
            "activo": True,
        }, f"Idioma {info['nombre']}")
        if not lang_id:
            continue
        totals["lang"] += 1

        for cefr, level_nombre, orden in LEVELS:
            level_id = create("/levels/", {
                "language": lang_id,
                "nombre": level_nombre,
                "codigo_cefr": cefr,
                "orden": orden,
            }, f"Nivel {level_nombre} ({cefr})")
            if not level_id:
                continue
            totals["level"] += 1

            lessons = info["lessons"][cefr]
            for l_orden, (titulo, icono, vocab) in enumerate(lessons, start=1):
                lesson_id = create("/lessons/", {
                    "level": level_id,
                    "titulo": titulo,
                    "descripcion": f"Aprende vocabulario de {titulo.lower()}.",
                    "orden": l_orden,
                    "icono": icono,
                }, f"Lección {titulo}")
                if not lesson_id:
                    continue
                totals["lesson"] += 1

                for e_orden, ex in enumerate(
                    build_exercises(info["nombre"], vocab), start=1
                ):
                    ex_payload = dict(ex)
                    ex_payload["lesson"] = lesson_id
                    ex_payload["orden"] = e_orden
                    ok = create(
                        "/exercises/", ex_payload,
                        f"Ejercicio {e_orden} [{ex['tipo']}]"
                    )
                    if ok:
                        totals["ex"] += 1

    print("\n========== RESUMEN ==========")
    print(f"Idiomas:    {totals['lang']}")
    print(f"Niveles:    {totals['level']}")
    print(f"Lecciones:  {totals['lesson']}")
    print(f"Ejercicios: {totals['ex']}")


if __name__ == "__main__":
    main()
