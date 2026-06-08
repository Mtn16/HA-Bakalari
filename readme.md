# Bakaláři rozvrh hodin
## Nutno mít před instalací

* HACS
* URL veřejného rozvrhu (obvykle `domena.cz/app/Timetable/Public`)

## Instalace
Pro instalaci stačí přidat integraci do Home Assistant HACS prostřednictvím tlačítka níže. Poté stačí v HACS vyhledat "Bakaláři", nainstalovat integraci a restartovat Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mtn16&repository=ha-bakalari&category=integration)

## Přidání rozvrhu
Pro přidání samotného rozvrhu otevřete sekci integrací, vyhledejte "Bakaláři" a vyplňte potřebné informace.

* **Název:** Slouží pouze k odlišení v rámci lovelace, vyplňte jakýkoliv chcete použít
* **URL:** Samotná adresa veřejného rozvrhu. Může jít jak o aktuální, tak stálý.
* **Ignorované skupiny:** Skupiny, které se z rozvrhu mají vyjmout a nebudou zohledňovány

## Poskytovaná data
Integrace do Home Assistant přidá následující data z rozvrhu:
* Začátek dnešní výuky
* Konec dnešní výuky
* Konec aktuální hodiny
* Aktuální předmět
* Aktuální učitel
* Aktuální učebna
* Další předmět