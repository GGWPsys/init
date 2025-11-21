import json
import csv


def test_read_bibliotheque_json(bibliotheque_json):
	p = bibliotheque_json
	data = json.loads(p.read_text(encoding="utf-8"))
	assert isinstance(data, list)
	assert len(data) == 2
	# vérifier quelques champs
	first = data[0]
	assert first["titre"] == "Le Petit Prince"
	assert "isbn" in first


def test_write_and_read_json(tmp_path, sample_bibliotheque):
	out = tmp_path / "out_biblio.json"
	out.write_text(json.dumps(sample_bibliotheque, ensure_ascii=False), encoding="utf-8")
	loaded = json.loads(out.read_text(encoding="utf-8"))
	assert loaded == sample_bibliotheque


def test_export_csv_structure(tmp_path, sample_bibliotheque):
	out = tmp_path / "catalogue.csv"
	# exporter sample_bibliotheque en CSV (simuler behaviour attendu)
	fieldnames = ["titre", "auteur", "categorie", "achete", "disponible", "note", "annee", "nb_pages", "langue", "isbn"]
	with out.open("w", encoding="utf-8", newline="") as fh:
		writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter=";")
		writer.writeheader()
		for item in sample_bibliotheque:
			writer.writerow(item)

	# lecture et vérification
	with out.open("r", encoding="utf-8", newline="") as fh:
		reader = csv.DictReader(fh, delimiter=";")
		rows = list(reader)
	assert len(rows) == len(sample_bibliotheque)
	assert set(reader.fieldnames) == set(fieldnames)