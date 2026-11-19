from seed import seed


def test_esquema_tiene_las_dos_restricciones_sin_comentarios():
    sentencias = seed.leer_esquema()
    assert len(sentencias) == 2
    assert all(s.startswith("CREATE CONSTRAINT") and "//" not in s for s in sentencias)


def test_cargar_aplica_esquema_antes_que_los_datos(monkeypatch):
    consultas = []
    monkeypatch.setattr(seed, "run_query", lambda q, **p: consultas.append(q) or [])
    seed.cargar()
    assert [q.startswith("CREATE CONSTRAINT") for q in consultas[:2]] == [True, True]
    assert len(consultas) == 4  # 2 restricciones + personas + amistades
