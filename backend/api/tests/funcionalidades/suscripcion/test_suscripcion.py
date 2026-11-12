def test_dos_grupos(cliente, auth):
    assert len(cliente.get("/api/v1/suscripcion/impacto", headers=auth).json()) == 2
