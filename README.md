# MEOntology

[English](#english) | [Русский](#русский)

<a name="english"></a>
## English

MEOntology (MEO) is a semantic ontology (OWL) formalizing the knowledge base of the Mass Effect video game franchise universe. 

Created as a tribute to BioWare's legacy, this project aims to preserve the rich lore of the original trilogy in a machine-readable format using Semantic Web technologies. MEO is being developed as a term project for the "Formal Semantics, Ontologies and Thesauri" course.

### Canon Timeline

To avoid logical paradoxes stemming from player-dependent choices, the MEO universe timeline is strictly fixed:
* **Starting Point:** The beginning of *Mass Effect 1* (prior to the Geth and Reaper "Sovereign" attack on the Eden Prime colony).
* All classes, individuals, and their properties (life status, faction affiliations, current roles) reflect the galactic status quo exactly at this moment in time.

### Project Goals

1. Developing an in-depth TBox in Protégé to describe races, factions, technologies, and the astrography of the Milky Way.
2. Designing a complex system of Object and Data Properties utilizing transitivity, symmetry, and inverse characteristics.
3. Automating the collection of ABox data (assertions about individuals) from the Mass Effect Wiki (Fandom) via the MediaWiki API.
4. Mapping the parsed data (approx. 3,000 axioms) into MEO using the Cellfie plugin.
5. Validating the logical consistency of the knowledge base using reasoners (HermiT / Pellet).

### Tech Stack

* **Ontology Editor:** Protégé
* **Format:** OWL / RDF
* **Data Scraping:** Python / R (MediaWiki API)
* **ABox Import:** Cellfie Plugin

---

<a name="русский"></a>
## Русский

MEOntology (MEO) — это семантическая онтология (OWL), формализующая знания о вселенной видеоигровой франшизы Mass Effect. 

Проект создается как дань уважения наследию студии BioWare и направлен на сохранение богатого лора оригинальной трилогии в машинно-читаемом виде с использованием технологий Semantic Web. MEO разрабатывается в рамках курсового проекта по дисциплине «Формальная семантика. Онтологии и тезаурусы».

### Состояние вселенной (Canon Timeline)

Для избежания логических парадоксов, связанных с вариативностью решений игрока, таймлайн вселенной в MEO жестко зафиксирован:
* **Точка отсчета:** Начало *Mass Effect 1* (до нападения гетов и Жнеца «Властелин» на колонию Иден Прайм).
* Все классы, индивиды и их свойства (статус жизни, принадлежность к фракциям, занимаемые должности) отражают статус-кво галактики именно на этот момент времени.

### Задачи проекта

1. Разработка глубокого TBox (терминологического словаря) в Protégé, описывающего расы, фракции, технологии и астрографию Млечного Пути.
2. Проектирование сложной системы свойств (Object/Data Properties) с использованием характеристик транзитивности, симметричности и инверсии.
3. Автоматизированный сбор ABox (утверждений об индивидах) с Mass Effect Wiki (Fandom) посредством MediaWiki API.
4. Маппинг спарсенных данных (около 3000 аксиом) в MEO с использованием плагина Cellfie.
5. Проверка логической непротиворечивости базы знаний с помощью ризонеров (HermiT / Pellet).

### Стек технологий

* **Редактор онтологий:** Protégé
* **Формат:** OWL / RDF
* **Скрейпинг данных:** Python / R (MediaWiki API)
* **Импорт ABox:** Cellfie Plugin