import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest


@pytest.fixture
def sample_livre():
    return {
        "titre": "Le Petit Prince",
        "auteur": "Antoine de Saint-Exupéry",
        "categorie": "Fiction",
        "achete": True,
        "disponible": True,
        "note": 4.7,
        "annee": 1943,
        "nb_pages": 96,
        "langue": "fr",
        "isbn": "978-0156012195",
    }


@pytest.fixture
def sample_bibliotheque(sample_livre):
    other = sample_livre.copy()
    other["titre"] = "Python pour les nuls"
    other["auteur"] = "John Doe"
    other["categorie"] = "Technique"
    return [sample_livre, other]


@pytest.fixture
def bibliotheque_json(tmp_path, sample_bibliotheque):

    p = tmp_path / "bibliotheque.json"
    p.write_text(json.dumps(sample_bibliotheque, ensure_ascii=False, indent=2), encoding="utf-8")
    return p