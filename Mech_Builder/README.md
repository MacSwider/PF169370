# Projekt zaliczeniowy w ramach przedmiotu fakuteltywnego

Projekt aplikacji okienkowej do tworzenia list do systemu bitewnego nad którym pracuje inspirowany takimi tytułami jak Warhammer 40000 oraz Battletech.

## Funkcjonalności

- dodawanie i usuwanie mechów do szwadronu z predefiniowanych danych
- zarządzanie uzbrojeniem i systemami (ang. wargear) poszczególnych mechów
- zapisz i wczytywanie list w postaci plików tekstowych

## Struktura projetku

```
Mech_Builder/
├── data/
│   ├── mech_data/
│   ├── abilities.json
│   ├── back_weapons.json
│   └── keywords.json
│   └── wargear.json
│   └── keywords.json
├── src/
│   ├── main.py
│   ├── gui.py
│   ├── mech_manager.py
│   └── saves.py
├── tests/
│   ├── test_gui.py
│   ├── test_mech_manager.py
│   ├── test_saves.py
└── README.md
└── requirements.txt
```

## Testowanie

python -m unittest discover -s tests -p "*.py"

##


Docstringi i część komentarzy zostały wygenerowane za pomocą Cloud Ai