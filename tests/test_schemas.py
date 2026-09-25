import pytest
from pydantic import ValidationError

from vnsoc.schemas import Atom, ManifestRow

BASE = dict(atom_id="a1", guideline="2760/2023", section="C.2.1", page=12, span="…15 ml/kg/giờ…", disease="dengue",
            condition="sốc", population={"age": ">=16"}, slot_type="dose", intervention="dịch truyền",
            value_kind="num", unit="ml/kg/h", vn=[{"lo": 15, "hi": 15}])


def test_atom_ok():
    Atom.model_validate(BASE)


def test_atom_rejects_bad_items():
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "vn": [{"seq": [0, 3]}]})
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "unit": None})
    with pytest.raises(ValidationError):
        Atom.model_validate({**BASE, "extra_field": 1})


def test_manifest_forbids_tvpl():
    with pytest.raises(ValidationError):
        ManifestRow.model_validate(dict(doc_key="1/2020", number="1", year=2020, title="x", disease="x", status="current",
                                        source_url="https://thuvienphapluat.vn/x"))


def test_foreign_record_requires_provenance():
    from vnsoc.schemas import ForeignRecord
    ok = dict(record_id="f1", disease="dengue", topic="sốc người lớn: dịch đầu", system="WHO_global", source="WHO 2009",
              version_date="2009", url="https://www.ncbi.nlm.nih.gov/books/NBK143161/", locator="ch. 2",
              fetched_at="2026-10-10", page_sha256="ab" * 32, values=[{"lo": 5, "hi": 10, "unit": "ml/kg/h"}])
    ForeignRecord.model_validate(ok)
    with pytest.raises(ValidationError):
        ForeignRecord.model_validate({k: v for k, v in ok.items() if k != "page_sha256"})
