from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.secret_key = "flowkompass-secret-2024"

QUESTIONS = [
    {
        "id": 1,
        "category": "stärken",
        "text": "Was tust du, wenn du ein schwieriges Problem lösen musst?",
        "options": [
            {"text": "Ich analysiere alles systematisch und suche nach Mustern.", "type": "denker"},
            {"text": "Ich spreche mit anderen und suche gemeinsam nach Lösungen.", "type": "helfer"},
            {"text": "Ich probiere kreative, ungewöhnliche Ansätze.", "type": "schöpfer"},
            {"text": "Ich übernehme die Initiative und organisiere einen Plan.", "type": "anführer"},
        ]
    },
    {
        "id": 2,
        "category": "werte",
        "text": "Was ist dir bei deiner Arbeit am wichtigsten?",
        "options": [
            {"text": "Menschen wirklich helfen und einen Unterschied machen.", "type": "helfer"},
            {"text": "Etwas Neues erschaffen, das es vorher nicht gab.", "type": "schöpfer"},
            {"text": "Tiefes Verstehen und Wissen aufbauen.", "type": "denker"},
            {"text": "Große Visionen verwirklichen und andere mitreißen.", "type": "anführer"},
        ]
    },
    {
        "id": 3,
        "category": "leidenschaft",
        "text": "Wofür verlierst du schnell das Zeitgefühl?",
        "options": [
            {"text": "Wenn ich mit Menschen spreche und ihnen zuhöre.", "type": "helfer"},
            {"text": "Wenn ich etwas gestalte – schreibe, zeichne, baue.", "type": "schöpfer"},
            {"text": "Wenn ich lerne, forsche oder Zusammenhänge verstehe.", "type": "denker"},
            {"text": "Wenn ich ein Projekt plane und ein Team koordiniere.", "type": "anführer"},
        ]
    },
    {
        "id": 4,
        "category": "stärken",
        "text": "Wie reagieren andere Menschen auf dich?",
        "options": [
            {"text": "Sie vertrauen mir ihre Sorgen an und suchen meinen Rat.", "type": "helfer"},
            {"text": "Sie bewundern meine originellen Ideen und meinen Stil.", "type": "schöpfer"},
            {"text": "Sie fragen mich um Rat bei komplexen Fragen.", "type": "denker"},
            {"text": "Sie folgen meiner Führung und meinen Entscheidungen.", "type": "anführer"},
        ]
    },
    {
        "id": 5,
        "category": "werte",
        "text": "Welche Aussage beschreibt dich am besten?",
        "options": [
            {"text": "Ich fühle mich gut, wenn ich anderen wirklich geholfen habe.", "type": "helfer"},
            {"text": "Ich brauche kreative Freiheit, sonst erstick ich.", "type": "schöpfer"},
            {"text": "Ich muss Dinge verstehen – Halbwissen macht mich unruhig.", "type": "denker"},
            {"text": "Ich will etwas bewegen und Verantwortung übernehmen.", "type": "anführer"},
        ]
    },
    {
        "id": 6,
        "category": "leidenschaft",
        "text": "In welchem Umfeld blühst du am meisten auf?",
        "options": [
            {"text": "Im direkten Kontakt mit Menschen, die meine Unterstützung brauchen.", "type": "helfer"},
            {"text": "In einem kreativen Atelier, Studio oder inspirierenden Ort.", "type": "schöpfer"},
            {"text": "In einer ruhigen Umgebung zum Denken, Lesen und Forschen.", "type": "denker"},
            {"text": "Mitten im Geschehen, mit Energie, Dynamik und Gestaltungsspielraum.", "type": "anführer"},
        ]
    },
    {
        "id": 7,
        "category": "stärken",
        "text": "Was ist deine größte Stärke?",
        "options": [
            {"text": "Empathie – ich verstehe, was andere fühlen und brauchen.", "type": "helfer"},
            {"text": "Originalität – ich sehe Dinge anders als die meisten.", "type": "schöpfer"},
            {"text": "Präzision – ich analysiere gründlich und denke logisch.", "type": "denker"},
            {"text": "Entschlossenheit – ich treffe Entscheidungen und handle.", "type": "anführer"},
        ]
    },
    {
        "id": 8,
        "category": "werte",
        "text": "Was soll dein Lebenswerk einmal sein?",
        "options": [
            {"text": "Vielen Menschen geholfen und ihr Leben verbessert haben.", "type": "helfer"},
            {"text": "Etwas geschaffen haben, das die Welt berührt und inspiriert.", "type": "schöpfer"},
            {"text": "Wissen vermehrt und Komplexes verständlich gemacht haben.", "type": "denker"},
            {"text": "Eine Organisation, Bewegung oder Idee in die Welt gebracht haben.", "type": "anführer"},
        ]
    },
]

TYPEN = {
    "helfer": {
        "name": "Der Herzmensch",
        "emoji": "💛",
        "tagline": "Du bist geboren, um anderen Kraft zu geben.",
        "beschreibung": (
            "Deine Berufung liegt im Dienst an Menschen. Du hast eine natürliche Empathie, "
            "spürst, was andere brauchen, und schenkst ihnen das Gefühl, wirklich gesehen zu werden. "
            "Du blühst auf, wenn du einen echten Unterschied im Leben anderer machen kannst."
        ),
        "berufe": [
            "Coach / Therapeutin", "Arzt / Ärztin", "Sozialarbeit", "Lehrerin / Pädagoge",
            "HR & People Development", "Pflegefachkraft", "Mediatorin", "Seelsorge"
        ],
        "nächste_schritte": [
            "Finde eine Person, der du heute zuhörst – wirklich zuhörst.",
            "Überlege: In welchem Bereich leidest du mit anderen mit?",
            "Erkunde Coaching- oder Therapeutenausbildungen.",
            "Frage Menschen in Helfer-Berufen nach ihrer Geschichte."
        ],
        "color": "#F59E0B",
        "gradient": "from-yellow-400 to-orange-400"
    },
    "schöpfer": {
        "name": "Der Schöpfer",
        "emoji": "🎨",
        "tagline": "Du bist geboren, um Neues in die Welt zu bringen.",
        "beschreibung": (
            "Deine Berufung liegt im Erschaffen. Du siehst die Welt als leere Leinwand voller Möglichkeiten. "
            "Ob mit Worten, Bildern, Tönen oder Ideen – du hast den Drang, etwas Einzigartiges zu hinterlassen. "
            "Kreative Freiheit ist für dich kein Luxus, sondern Lebensnotwendigkeit."
        ),
        "berufe": [
            "Designer / UX Designerin", "Schriftstellerin / Autor", "Musikerin / Komponist",
            "Architekt / Architektin", "Filmemacherin", "Markenstratege", "Künstlerin", "Content Creator"
        ],
        "nächste_schritte": [
            "Schaffe heute etwas – egal wie klein. Ein Bild, ein Text, eine Idee.",
            "Finde heraus, welches Medium dich am meisten begeistert.",
            "Zeige deine Werke – Sichtbarkeit ist Teil deiner Berufung.",
            "Suche dir kreative Mentor:innen oder Communities."
        ],
        "color": "#8B5CF6",
        "gradient": "from-purple-400 to-pink-400"
    },
    "denker": {
        "name": "Der Weise",
        "emoji": "🔭",
        "tagline": "Du bist geboren, um Licht ins Dunkel zu bringen.",
        "beschreibung": (
            "Deine Berufung liegt im Verstehen und Erkennen. Du kannst komplexe Zusammenhänge durchdringen, "
            "Muster erkennen, die andere übersehen, und Wissen so aufbereiten, dass es wirklich nützt. "
            "Die Welt braucht Menschen wie dich, die tiefgründig denken und klug handeln."
        ),
        "berufe": [
            "Wissenschaftlerin / Forscher", "Strategieberatung", "Data Scientist", "Philosophin",
            "Ärztin (Forschung)", "Wirtschaftsanalyst", "Professorin", "Systemarchitekt"
        ],
        "nächste_schritte": [
            "Wähle ein Thema, das dich wirklich fasziniert – und tauche tief ein.",
            "Schreibe auf, was du weißt – Schreiben schärft das Denken.",
            "Finde deinen Bereich: Naturwissenschaft, Gesellschaft, Technik, Philosophie?",
            "Suche dir einen Mentor in deinem Interessensgebiet."
        ],
        "color": "#3B82F6",
        "gradient": "from-blue-400 to-cyan-400"
    },
    "anführer": {
        "name": "Der Visionär",
        "emoji": "🔥",
        "tagline": "Du bist geboren, um Bewegung in die Welt zu bringen.",
        "beschreibung": (
            "Deine Berufung liegt im Gestalten großer Dinge. Du siehst, wie die Welt sein könnte, "
            "und hast den Mut und die Energie, andere für diese Vision zu begeistern. "
            "Du lebst auf, wenn du Verantwortung trägst, Entscheidungen triffst und Wirkung siehst."
        ),
        "berufe": [
            "Unternehmerin / Gründer", "Führungskraft / CEO", "Politikerin", "Projektmanager",
            "Eventmanagerin", "Sozialunternehmerin", "NGO-Leiterin", "Produktmanagerin"
        ],
        "nächste_schritte": [
            "Identifiziere ein Problem, das dich wütend macht – und das du lösen willst.",
            "Übernimm in einem Projekt die Leitung – auch im Kleinen.",
            "Finde Mentor:innen, die bereits gebaut haben, was du dir vorstellst.",
            "Lerne die Grundlagen: Finanzen, Kommunikation, Teamaufbau."
        ],
        "color": "#EF4444",
        "gradient": "from-red-400 to-orange-500"
    }
}


def calculate_result(answers: dict) -> dict:
    scores = {"helfer": 0, "schöpfer": 0, "denker": 0, "anführer": 0}
    for answer_type in answers.values():
        if answer_type in scores:
            scores[answer_type] += 1
    winner = max(scores, key=scores.get)
    total = sum(scores.values())
    percentages = {k: round((v / total) * 100) for k, v in scores.items()} if total > 0 else scores
    return {
        "typ": winner,
        "scores": scores,
        "percentages": percentages,
        "profil": TYPEN[winner]
    }


@app.route("/")
def index():
    session.clear()
    return render_template("index.html")


@app.route("/test")
def test():
    return render_template("test.html", questions=QUESTIONS, total=len(QUESTIONS))


@app.route("/ergebnis", methods=["POST"])
def ergebnis():
    answers = {}
    for q in QUESTIONS:
        key = f"q{q['id']}"
        answers[key] = request.form.get(key, "")
    result = calculate_result(answers)
    return render_template("result.html", result=result, typen=TYPEN)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
