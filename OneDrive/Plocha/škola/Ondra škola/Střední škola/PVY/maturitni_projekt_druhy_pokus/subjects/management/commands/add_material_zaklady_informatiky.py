"""
Management command pro přidání materiálu "Základy informatiky" do databáze.
"""
from django.core.management.base import BaseCommand
from subjects.models import Subject, Topic
from materials.models import Material, MaterialType


class Command(BaseCommand):
    help = 'Přidá materiál "Základy informatiky" do databáze'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("PŘIDÁNÍ MATERIÁLU 'ZÁKLADY INFORMATIKY'")
        self.stdout.write("=" * 70)
        self.stdout.write()

        # 1. Získat nebo vytvořit předmět
        subject, created = Subject.objects.get_or_create(
            slug='programove-vybaveni',
            defaults={
                'name': 'Programové vybavení',
                'description': 'Příprava k maturitě z předmětu Programové vybavení'
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen předmět: {subject.name}"))
        else:
            self.stdout.write(f"✓ Použit existující předmět: {subject.name}")

        # 2. Získat nebo vytvořit okruh
        topic, created = Topic.objects.get_or_create(
            subject=subject,
            slug='zaklady-informatiky',
            defaults={
                'name': 'Základy informatiky',
                'description': 'Pojem informatika, informace, data, signál, digitalizace, jednotky, číselné soustavy, kódování, přenos informací a datová komprese.',
                'order': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen okruh: {topic.name}"))
        else:
            self.stdout.write(f"✓ Použit existující okruh: {topic.name}")

        # 3. Obsah materiálu
        content = """1. Pojem informatika, informace, data, signál (analogový, digitální), digitalizace

Co je informatika?

Informatika je vědní obor zabývající se získáváním, zpracováním, ukládáním a přenosem informací.

Zahrnuje teoretické i praktické aspekty výpočetní techniky, programování, algoritmů a databází.

Počátky informatiky sahají do 2. poloviny 20. století, kdy se začaly vyvíjet první počítače. Mezi zakladatele patří Alan Turing, John von Neumann.

Aplikovaná informatika se zabývá využitím počítačů v různých oblastech (ekonomie, medicína, průmysl). K příbuzným oborům patří kybernetika, telekomunikace, robotika.

ICT (Information and Communication Technology) – informační a komunikační technologie (hardware, software, sítě a služby).

Informace, data, signál

Data – surová fakta získaná z reality (čísla, text, obrázky, zvuky), nemají význam sama o sobě.

Informace – zpracovaná data, která mají smysl a hodnotu pro příjemce. Umožňují rozhodování a jednání.

Signál – fyzikální veličina přenášející informaci. V informatice využíváme elektrické napětí (mikroprocesory, paměti, sítě), světlo (optické kabely), elektromagnetické vlny (WiFi, mobilní sítě) nebo magnetické polarity (disky).

Typy signálů:

Analogový signál – spojitý, typický pro zvuk, světlo (např. hlas v telefonu, radiové vlny). Příkladem analogových zařízení jsou starší televize, rádia, gramofony

Digitální signál – nespojitý, reprezentován binárními hodnotami (0 a 1), používá se v počítačích a telekomunikacích. Příkladem digitálních zařízení jsou počítače, mobilní telefony, digitální fotoaparáty.

Digitalizace

Převod analogového signálu na digitální formu. V informatice se digitalizace využívá pro zpracování zvuku, obrazu, videa a dalších dat.

A/D převodník – zařízení pro převod analogového signálu na digitální formu.

D/A převodník – zařízení pro převod digitálního signálu na analogovou podobu.

Klíčové procesy:

Vzorkování – rozčlenění spojitého signálu na sekvenci hodnot. V případě zvuku v CD kvalitě se provádí 44 100× za sekundu (44,1 kHz).

Kvantování – přiřazení konkrétních hodnot vzorkům podle bitové hloubky (např. 16bitové kódování zvuku v CD kvalitě).

Kódování – uložení hodnot v binární podobě (např. pomocí ASCII nebo Unicode pro text).

2. Jednotky v informatice

Základní jednotky pro zpracování dat

Bit (b) – nejmenší jednotka informace (0 nebo 1). Využívá se pro označení architektury počítačů (32bit, 64bit) nebo rychlosti přenosu dat (bps).

Byte (B) – 8 bitů. Používá se pro reprezentaci znaků (ASCII, Unicode) nebo pro velikost pamětí a souborů.

Kilobyte (KB) – 1024 B = 2¹⁰ B (přibližně 1000 B).

Megabyte (MB) – 1024 KB.

Gigabyte (GB) – 1024 MB.

Terabyte (TB) – 1024 GB.

Architektury počítačů

32bitová architektura – procesor zpracovává 32bitová data najednou (4B). Maximální paměťová kapacita je 4 GB.

64bitová architektura – procesor zpracovává 64bitová data najednou (8B). Maximální paměťová kapacita je 16 EB (exabajtů).

Přenosová kapacita

Baud (Bd) – jednotka pro rychlost přenosu dat (počet změn signálu za sekundu). U digitálních signálů se rovná bitu za sekundu (bps).

BPS (Bits Per Second) – počet bitů přenesených za sekundu. Používá se pro rychlost internetového připojení, přenos dat na disku nebo v síti.

3. Číselné soustavy a jejich převody

Základní číselné soustavy

Desítková (dekadická, základ 10) – běžně používaná v matematice.

Dvojková (binární, základ 2) – používá hodnoty 0 a 1, základem výpočtů v počítačích.

Osmičková (oktalová, základ 8) – používá číslice 0–7, méně běžná.

Šestnáctková (hexadecimální, základ 16) – používá číslice 0–9 a písmena A–F, často v programování, vyjádření barev a MAC adres.

Převody mezi soustavami

Převod z desítkové soustavy: - Dělíme desítkové číslo základem požadované soustavy (2, 8, 10) a zapisujeme zbytky zprava doleva.

Převod do desítkové soustavy: - Sčítáme hodnoty jednotlivých pozic vynásobené mocninou základu soustavy.

Rychlý převod mezi binární a hexadecimální soustavou: - Každý čtyřbitový blok binárního čísla odpovídá jedné hexadecimální číslici.

Převod mezi binární a osmičkovou soustavou: - Každý tříbitový blok binárního čísla odpovídá jedné osmičkové číslici.

Číselné soustavy v programování

Binární čísla – začínají na 0b (např. 0b1010).

Osmičková čísla – začínají na 0o (např. 0o12).

Hexadecimální čísla – začínají na 0x (např. 0x1A).

4. Princip kódování informací, kódování znaků, reprezentace čísel v počítači

Kódování informací

Kód je pravidlo pro převod informace z jedné podoby do druhé (znaky, čísla, zvuky).

V informatice se kódování využívá pro reprezentaci znaků, čísel, obrazu, zvuku a dalších dat v binární podobě.

Kromě jednorozměrných kódů (ASCII, Unicode) se používají i dvourozměrné kódy (QR kódy, čárové kódy).

QR kódy jsou čtvercové matice, které obsahují informace v podobě černých a bílých čtverečků. Používají se pro rychlé načítání informací pomocí mobilních telefonů.

Čárové kódy obsahují informace v podobě čárek a mezer různé šířky. Používají se pro označení zboží, knih, letenek a dalších produktů.

Kódování znaků

Pro tento účel se využívají různé kódovací tabulky, které přiřazují znakům binární hodnoty. Tyto kódové tabulky jsou standardizovány a označovány jako CP (Code Page) nebo ISO (International Organization for Standardization).

ASCII (American Standard Code for Information Interchange) – původně 7bitový kód pro anglický text (128 znaků). Později rozšířen na 8 bitů (256 znaků). V počítačové praxi se používá rozšířená verze ASCII s diakritikou a speciálními znaky. Pro reprezentaci znaků používaných v češtině existuje několik různých 8bitových kódování (ISO 8859-2, Windows-1250, Kameničtí).

Unicode – univerzální kódování pro všechny jazyky světa. Obsahuje znaky pro latinku, cyrilici, čínštinu, arabštinu a další.

UTF-8 – proměnná délka kódování znaků Unicode. Umožňuje efektivní reprezentaci anglického textu (1 byte) i jiných jazyků (2–4 byty).

Reprezentace čísel v počítači

Celá čísla (Integer) – uložena jako binární hodnota pevné délky. Může být znaménkové (signed) nebo neznaménkové (unsigned).

Znaménkové čísla – využívají nejvyšší bit pro označení znaménka (0 = kladné, 1 = záporné). Pro záporná čísla se používá doplněk k jedničce.

Reálná čísla (Floating-point) – desetinná čísla jsou binárně tvořena z mantisy, exponentu a znaménka. Problémem jsou omezená přesnost a zaokrouhlovací chyby.

5. Přenos informací a princip datové komprese

Přenos informací

Z pohledu informatiky je přenos informací procesem komunikace mezi odesílatelem a příjemcem prostřednictvím komunikačního kanálu.

V rámci přenosu dochází ke kódování informací do podoby signálu, který je přenášen pomocí fyzikálního média (vodič, optické vlákno, elektromagnetické pole).

Modulace – proces převodu digitálního signálu na analogovou podobu pro přenos po fyzikálním médiu. Příklady modulace jsou AM, FM, QAM, FSK.

Demodulace – proces převodu analogového signálu na digitální podobu pro zpracování v počítači.

Přenos informací podléhá různým druhům chyb (šum, rušení, ztráta dat), které mohou být detekovány a opraveny pomocí kódování a detekce chyb.

Datová komprese

Účel: Zmenšení objemu dat pro rychlejší přenos nebo úsporu místa.

Typy komprese:

Bezztrátová (lossless) – umožňuje zpětnou rekonstrukci dat bez ztráty informace. Používá se u archivačních formátů (ZIP, RAR), grafiky (PNG, GIF), zvuku (FLAC).

Ztrátová (lossy) – odstraňuje nepodstatné informace s cílem dosáhnout větší komprese. Používá se u multimediálních formátů (JPEG, MP3, MP4).

Algoritmy bezztrátové komprese

Run-Length Encoding (RLE) – pro kompresi využívá opakování stejných prvků (barvy, znaky).

Huffmanovo kódování – využívá statistického rozdělení opakovaného výskytu určitých prvků (např. částí textu). Na základě toho přiřazuje kratší kódy častěji se vyskytujícím prvkům.

Lempel-Ziv-Welch (LZW) – využívá slovníkovou kompresi, kdy se opakující se řetězce nahrazují kratšími kódy. V praxi se setkáváme s variantou LZW v GIF a TIFF formátech.

Detekce a oprava chyb při přenosu

Paritní kód – jednoduchý způsob detekce chyb, který využívá sudé nebo liché počty bitů a paritní bit pro kontrolu. Neumožňuje opravu chyb, pouze detekci.

Kontrolní součet (Checksum) – funguje na principu porovnání kontrolního součtu odeslaných dat s kontrolním součtem přijatých dat. Pokud se liší, došlo k chybě.

Kontrolní kód (CRC) – cyklický redundantní kód, který umožňuje detekci a opravu chyb. Používá se například v síťových protokolech (Ethernet, Wi-Fi).

Existuje mnoho dalších metod pro detekci a opravu chyb, které se liší podle konkrétních požadavků na spolehlivost a efektivitu. Používají se například v telekomunikacích, datových úložištích a síťových technologiích."""

        # 4. Vytvořit nebo aktualizovat materiál
        material, created = Material.objects.get_or_create(
            topic=topic,
            title='Základy informatiky',
            defaults={
                'material_type': MaterialType.TEXT,
                'description': 'Pojem informatika, informace, data, signál (analogový, digitální), digitalizace. Jednotky v informatice. Číselné soustavy a jejich převody. Princip kódování informací, kódování znaků, reprezentace čísel v počítači. Přenos informací a princip datové komprese.',
                'content': content,
                'is_published': True,
                'order': 1
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"✓ Vytvořen materiál: {material.title}"))
        else:
            # Aktualizovat obsah, pokud materiál již existuje
            material.content = content
            material.description = 'Pojem informatika, informace, data, signál (analogový, digitální), digitalizace. Jednotky v informatice. Číselné soustavy a jejich převody. Princip kódování informací, kódování znaků, reprezentace čísel v počítači. Přenos informací a princip datové komprese.'
            material.is_published = True
            material.order = 1
            material.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Aktualizován materiál: {material.title}"))

        self.stdout.write()
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("✓ Hotovo! Materiál byl úspěšně přidán/aktualizován."))
        self.stdout.write()
        self.stdout.write(f"Předmět: {subject.name}")
        self.stdout.write(f"Okruh: {topic.name}")
        self.stdout.write(f"Materiál: {material.title}")
        self.stdout.write(f"Typ: {material.get_material_type_display()}")
        self.stdout.write(f"URL: /materials/{material.id}/")
        self.stdout.write("=" * 70)

