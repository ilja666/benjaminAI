# CACS MVP — Basisarchitectuur

**Auteur:** Manus AI  
**Datum:** 2 april 2026

## Doel

Deze eerste **CACS MVP** is ontworpen als een kleine, toetsbare demonstrator van een actief cognitief systeem. De kernvraag is niet of het systeem indrukwekkende taal kan produceren, maar of het een **interne toestand** kan onderhouden, **ervaringen** kan opslaan, **acties** kan uitvoeren in een digitale omgeving en vervolgens zijn gedrag kan **bijstellen op basis van mismatch** tussen verwachting en uitkomst.

De implementatie wordt daarom bewust klein gehouden. Het model werkt in een beperkte sandbox-wereld met objecten, toestanden, doelen en interventies. Binnen die beperking moet het al wel de basis van de CACS-filosofie laten zien.

## Architectuurlagen

| Laag | Functie | Concreet MVP-artefact |
|---|---|---|
| Omgeving | Beschrijft objecten, toestanden, acties en doelcondities | `environment.py` |
| Toestandslaag | Houdt agentstatus, taakdoel, aannames en iteratiegegevens vast | `state.py` |
| Geheugenlaag | Slaat episodes, gebeurtenissen en reflecties op | `memory.py` |
| Planningslaag | Kiest de meest logische volgende actie op basis van toestand en doel | `planner.py` |
| Actielaag | Voert een interventie uit in de sandbox en registreert de uitkomst | `agent.py` + `environment.py` |
| Reflectielaag | Vergelijkt verwachting met uitkomst en schrijft mismatch weg | `reflection.py` |
| Control loop | Orkestreert sense, model, plan, act, reflect | `agent.py` |

## Gegevensmodel

De MVP gebruikt drie soorten interne representatie. De eerste is **wereldtoestand**: welke objecten bestaan er, welke status hebben ze, en welke relaties zijn relevant voor de taak. De tweede is **agenttoestand**: wat is het doel, welke hypothese is actief, welke stap is zojuist gezet, en welke verwachting hoort daarbij. De derde is **episodisch geheugen**: een chronologische opslag van observaties, acties, uitkomsten en reflecties.

| Representatie | Inhoud |
|---|---|
| Wereldtoestand | Objectstatussen, blokkades, beschikbaarheid van acties |
| Agenttoestand | Doel, iteratie, huidige strategie, verwachte uitkomst |
| Episode | Tijdstip, observatie, actie, resultaat, mismatch, reflectie |

## Eerste sandbox-scenario

Het eerste scenario wordt een eenvoudige digitale hersteltaak. Een kleine software-achtige werkruimte bevat enkele objecten met onderlinge afhankelijkheden. Het doel is om een systeem van een fouttoestand naar een werkende toestand te brengen.

Een voorbeeldscenario is dat een service niet kan starten omdat een configuratie onjuist is en een dependency ontbreekt. De agent moet dan leren dat blind herstarten niet volstaat, maar dat de juiste volgorde van interventies nodig is. Juist in die volgorde zit de eerste vorm van causale planning.

## Cognitieve lus

De volledige MVP draait om een expliciete lus van vijf stappen.

| Stap | Functie |
|---|---|
| Sense | Lees de huidige wereldtoestand en relevante signalen |
| Model | Vorm een werkhypothese over wat het probleem veroorzaakt |
| Plan | Kies een volgende actie die richting de doeltoestand beweegt |
| Act | Voer de interventie uit in de sandbox |
| Reflect | Vergelijk verwachting met uitkomst en sla mismatch op |

## Ontwerpkeuzes

De MVP kiest bewust voor **expliciete datastructuren** in plaats van verborgen toestand in losse prompts. Daarmee wordt het mogelijk om later dezelfde architectuur te koppelen aan een taalmodel, maar nu eerst de cognitieve ruggengraat te bouwen zonder semantische mist.

Ook de reflectielaag is klein gehouden. In plaats van complexe meta-learning volstaat in deze fase een mechanisme dat verkeerde aannames zichtbaar maakt en later kan worden gebruikt om planningsregels of heuristieken aan te passen.

## Verwachte uitkomst van deze iteratie

Als de MVP slaagt, levert zij niet meteen algemene intelligentie op. Wat zij wel levert, is een aantoonbare minimale CACS-kern: een agent die **toestand behoudt**, **ervaringen opslaat**, **interventies uitvoert** en **van fouten leert** binnen een afgebakende digitale taakomgeving.

Dat is voldoende om de volgende iteratie te rechtvaardigen, waarin een rijker wereldmodel, semantisch geheugen en tegenfeitelijke planning kunnen worden toegevoegd.
