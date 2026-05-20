"""Frågor och kortlek för Rundan."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Category(str, Enum):
    TRUTH = "sanning"
    DARE = "utmaning"
    DRINK = "drick"
    VOTE = "rösta"
    WILD = "vild"


CATEGORY_LABELS: dict[Category, str] = {
    Category.TRUTH: "Sanning",
    Category.DARE: "Utmaning",
    Category.DRINK: "Drick",
    Category.VOTE: "Rösta",
    Category.WILD: "Vild",
}

CATEGORY_EMOJI: dict[Category, str] = {
    Category.TRUTH: "💬",
    Category.DARE: "🔥",
    Category.DRINK: "🥂",
    Category.VOTE: "👉",
    Category.WILD: "✨",
}


@dataclass(frozen=True)
class Question:
    id: int
    text: str
    category: Category


# 100 kort — blandning av sanning, utmaning, drick, rösta & vild
_QUESTION_DATA: list[tuple[Category, str]] = [
    # Sanning (1–20)
    (Category.TRUTH, "Vad var din mest pinsamma dansrörelse på en fest?"),
    (Category.TRUTH, "Vem i rummet skulle du vilja ha som wingman/wingwoman ikväll?"),
    (Category.TRUTH, "Vad är det dummaste du skickat till fel person?"),
    (Category.TRUTH, "Vilken låt på din spellista avslöjar dig mest?"),
    (Category.TRUTH, "När var du senast riktigt starstruck?"),
    (Category.TRUTH, "Vad är din guilty pleasure-snack innan utgång?"),
    (Category.TRUTH, "Vem här känner du dig minst förberedd inför att träffa IRL?"),
    (Category.TRUTH, "Vad är det modigaste du gjort en kväll innan ni gick ut?"),
    (Category.TRUTH, "Vilken trend följde du som du ångrar?"),
    (Category.TRUTH, "Vad skulle ditt dröm-scenario för kvällen vara?"),
    (Category.TRUTH, "Vem här tror du kommer hamna sist hemma — och varför?"),
    (Category.TRUTH, "Vad är det snyggaste kompliment du fått på en fest?"),
    (Category.TRUTH, "Vilken app har du gömt på telefonen som ingen får se?"),
    (Category.TRUTH, "Vad var din första tank när du kom in ikväll?"),
    (Category.TRUTH, "Vem i rummet har bäst energi just nu?"),
    (Category.TRUTH, "Vad är det mest spontana du sagt ja till på fest?"),
    (Category.TRUTH, "Vilken outfit-detail är du mest stolt över ikväll?"),
    (Category.TRUTH, "Vad skulle du aldrig posta på stories — men kanske gör ikväll?"),
    (Category.TRUTH, "Vem här skulle du lita på med din telefon i 2 minuter?"),
    (Category.TRUTH, "Vad är din hemliga superkraft på dansgolvet?"),
    # Utmaning (21–45)
    (Category.DARE, "Visa din bästa 10-sekunders dans utan musik."),
    (Category.DARE, "Ring någon i kontaktlistan och säg 'vi är på väg ut' — på högtalare."),
    (Category.DARE, "Läs upp din senaste DM högt (du får välja vilken)."),
    (Category.DARE, "Byt en accessoar med personen till vänster om dig."),
    (Category.DARE, "Gör din bästa imitation av någon i rummet — gruppen gissar vem."),
    (Category.DARE, "Ta en selfie med alla och posta med caption gruppen väljer."),
    (Category.DARE, "Prata med brittisk accent tills nästa kort."),
    (Category.DARE, "Visa senaste foto i kamerarullen — snabbt, inget scrollande."),
    (Category.DARE, "Ge en äkta komplimang till varje person i rummet."),
    (Category.DARE, "Stå på en stol och håll 15 sekunders toast för kvällen."),
    (Category.DARE, "Byt plats med någon du nästan inte pratat med ikväll."),
    (Category.DARE, "Sjung refrängen på låten som spelas — eller din favoritlåt."),
    (Category.DARE, "Gör 5 squats medan du håller blickkontakt med någon."),
    (Category.DARE, "Skicka ett hjärta till någon du inte pratat med på en vecka."),
    (Category.DARE, "Visa hur du ser ut när du försöker vara cool på bar."),
    (Category.DARE, "Låt gruppen välja din nästa drink (eller mocktail)."),
    (Category.DARE, "Berätta en vit lögn om dig själv — någon ska gissa att det är falskt."),
    (Category.DARE, "Gör en catwalk från dörren till soffan."),
    (Category.DARE, "Spela 'finns i sjön' med något i rummet på 20 sek."),
    (Category.DARE, "Byt skor med någon i 1 runda (strumpor OK)."),
    (Category.DARE, "Håll plank i 20 sekunder eller ta 2 klunkar."),
    (Category.DARE, "Rita en emoji på kinden med läppstift/penna — behåll tills nästa runda."),
    (Category.DARE, "Låt någon skriva en mening du måste säga innan ni går."),
    (Category.DARE, "Gör en dramatisk filmtrailer-intro av dig själv."),
    (Category.DARE, "Whisper challenge: viska en mening, gruppen gissar."),
    # Drick (46–65) — alltid med möjlighet att hoppa över
    (Category.DRINK, "Alla som drack senaste timmen — ta en klunk."),
    (Category.DRINK, "Den som kom sist ikväll — ta en klunk (eller ge bort till någon)."),
    (Category.DRINK, "Om du har svarta klädesplagg på dig — ta en klunk."),
    (Category.DRINK, "Den med kortast hår — välj vem som ska dricka med dig."),
    (Category.DRINK, "Skål för kvällen — alla dricker."),
    (Category.DRINK, "Den som skrattade senast — ta en klunk."),
    (Category.DRINK, "Om du redan planerat morgondagens outfit hem — ta en klunk."),
    (Category.DRINK, "Vattendrickare: drick ett glas vatten och ge någon annan en klunk."),
    (Category.DRINK, "Den som har flest notiser olästa — ta en klunk."),
    (Category.DRINK, "Skapa en skål-tema (t.ex. 'för vädret') — alla dricker."),
    (Category.DRINK, "Om du dansat ikväll — ta en klunk."),
    (Category.DRINK, "Den som sitter längst från dörren — dricker med den närmast."),
    (Category.DRINK, "Byt drink med någon för nästa klunk (smaka får de själva)."),
    (Category.DRINK, "Alla som har en dating-app — ta en klunk."),
    (Category.DRINK, "Den som tar snyggast selfies — välj två som dricker."),
    (Category.DRINK, "Om du glömt ladda telefonen — ta en klunk."),
    (Category.DRINK, "Skål för personen till höger om dig."),
    (Category.DRINK, "Den som pratat mest ikväll — ta en klunk."),
    (Category.DRINK, "Om du dricker alkoholfritt — alla andra tar en klunk."),
    (Category.DRINK, "Den yngsta i rummet väljer vem som skålar."),
    # Rösta (66–83)
    (Category.VOTE, "Rösta: vem kommer bli kvällens DJ?"),
    (Category.VOTE, "Rösta: vem har bäst outfit?"),
    (Category.VOTE, "Rösta: vem är mest trolig att bli kär ikväll?"),
    (Category.VOTE, "Rösta: vem skulle överleva längst på dansgolvet?"),
    (Category.VOTE, "Rösta: vem har mest 'main character energy'?"),
    (Category.VOTE, "Rösta: vem är mest trolig att beställa vatten på klubben?"),
    (Category.VOTE, "Rösta: vem skulle du vilja ha i samma taxibil?"),
    (Category.VOTE, "Rösta: vem har bäst skratt?"),
    (Category.VOTE, "Rösta: vem kommer skicka flest bilder i gruppen i natt?"),
    (Category.VOTE, "Rösta: vem är mest trolig att glömma något hemma?"),
    (Category.VOTE, "Rösta: vem hade klarat reality-TV bäst?"),
    (Category.VOTE, "Rösta: vem är mest trolig att starta afterparty hemma?"),
    (Category.VOTE, "Rösta: vem ser mest ut som sin profilbild?"),
    (Category.VOTE, "Rösta: vem skulle du lita på med väskan på klubben?"),
    (Category.VOTE, "Rösta: vem har mest kaos-energi?"),
    (Category.VOTE, "Rösta: vem är mest trolig att bli kompis med bartendern?"),
    (Category.VOTE, "Rösta: vem hade vunnit i charmtävling?"),
    (Category.VOTE, "Rösta: vem kommer du vilja höra av dig imorgon bitti?"),
    # Vild (84–100)
    (Category.WILD, "Alla byter plats — sitt där någon annan satt."),
    (Category.WILD, "Skapa en ny regel för resten av kvällen (max 1 mening)."),
    (Category.WILD, "Nästa kort gäller dubbelt för den som drog det."),
    (Category.WILD, "Gruppen väljer en 'måltavla' — alla pekar på den vid nästa rösta-kort."),
    (Category.WILD, "Byt telefon med någon i 1 minut (inga lösenord)."),
    (Category.WILD, "Alla säger sin 'ton för kvällen' i ett ord."),
    (Category.WILD, "Starta en kedja: gör en rörelse — nästa person upprepar + lägger till."),
    (Category.WILD, "Den som drog kortet väljer nästa låt (30 sek preview räcker)."),
    (Category.WILD, "Spela två sanningar och en lögn — gruppen gissar."),
    (Category.WILD, "Alla stänger ögonen — peka på vem du tror vinner kvällen."),
    (Category.WILD, "Skapa ett lag-namn för er ikväll."),
    (Category.WILD, "Gruppen får ställa EN fråga till dig — inget filter."),
    (Category.WILD, "Alla som har jobb imorgon — visa reaktion med emoji-hand."),
    (Category.WILD, "Planera er exit-strategi till klubben/bar på 30 sek."),
    (Category.WILD, "Ta en gruppbild som blir er officiella kvällsbild."),
    (Category.WILD, "Den som drog kortet blir spelledare nästa 3 kort."),
    (Category.WILD, "Alla skålar för något de är tacksamma för idag."),
]

QUESTIONS: list[Question] = [
    Question(id=i + 1, text=text, category=cat)
    for i, (cat, text) in enumerate(_QUESTION_DATA)
]


class QuestionDeck:
    """Blandad kortlek utan upprepning tills leken tar slut."""

    def __init__(self, categories: set[Category] | None = None) -> None:
        pool = QUESTIONS if categories is None else [q for q in QUESTIONS if q.category in categories]
        self._pool = list(pool)
        self._remaining: list[Question] = []
        self.drawn_count = 0
        self.reshuffle()

    def reshuffle(self) -> None:
        self._remaining = list(self._pool)
        random.shuffle(self._remaining)

    @property
    def total(self) -> int:
        return len(self._pool)

    @property
    def left(self) -> int:
        return len(self._remaining)

    def draw(self) -> Question | None:
        if not self._pool:
            return None
        if not self._remaining:
            self.reshuffle()
        question = self._remaining.pop()
        self.drawn_count += 1
        return question
