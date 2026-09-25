import json

import pytest

from vnsoc.freeze import freeze
from vnsoc.paths import paths
from test_schemas import BASE


def test_freeze_atoms(proj):
    P = paths(proj)
    (proj / "data" / "interim").mkdir(parents=True)
    src = proj / "data" / "interim" / "atoms.jsonl"
    src.write_text(json.dumps(BASE, ensure_ascii=False) + "\n", encoding="utf-8")
    a = freeze("atoms", proj)
    b = freeze("atoms", proj)
    assert a[0].name == "atoms_v1.jsonl" and b[0].name == "atoms_v2.jsonl"
    assert "atoms_v1.jsonl" in (proj / "data" / "frozen" / "SHA256SUMS").read_text()
    assert "Đóng băng atoms" in P.decisions.read_text()
    src.write_text(json.dumps({**BASE, "vn": []}) + "\n{bad json\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        freeze("atoms", proj)
