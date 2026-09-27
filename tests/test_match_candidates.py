"""Candidate foreign counterparts: hard filters (kind, convertible unit) and topic scoring."""
from vnsoc.match import candidates as c


def _atom(**kw):
    a = {"atom_id": "A-2760_2023-001", "guideline": "2760/2023", "condition": "sốc sốt xuất huyết Dengue",
         "intervention": "tốc độ truyền dịch tinh thể giờ đầu", "population": {"age": "người lớn"},
         "value_kind": "num", "unit": "ml/kg/h", "vn": [{"lo": 15, "hi": 15, "unit": "ml/kg/h"}]}
    a.update(kw)
    return a


def _rec(rid, topic, values):
    return {"record_id": rid, "topic": topic, "values": values}


def test_filters_and_ranking():
    recs = {"dengue_hfmd": [
        _rec("F-1", "tốc độ truyền dịch tinh thể giờ đầu, sốc dengue, người lớn", [{"lo": 5, "hi": 7, "unit": "ml/kg/h"}]),
        _rec("F-2", "tốc độ truyền dịch, sốc dengue", [{"lo": 20, "hi": 20, "unit": "mg"}]),        # unit not convertible
        _rec("F-3", "liều paracetamol hạ sốt", [{"lo": 10, "hi": 15, "unit": "ml/kg/h"}])]}           # off topic
    out = c.candidates([_atom()], recs, {"2760/2023": "dengue_hfmd"})
    ids = [x["record_id"] for x in out[0]["candidates"]]
    assert ids[0] == "F-1" and "F-2" not in ids
    assert c.candidates([_atom(guideline="9999/2026")], recs, {"2760/2023": "dengue_hfmd"}) == []


def test_drug_records_do_not_need_a_shared_drug():
    a = _atom(value_kind="drugs", unit=None, intervention="thuốc đầu tay sốt rét", vn=[{"key_drugs": ["dihydroartemisinin-piperaquine"]}])
    r = _rec("F-9", "thuốc đầu tay sốt rét", [{"key_drugs": ["artemether-lumefantrine"]}])
    assert c.compatible(a, r) and c.score(a, r) > 0.5
