from app.nucleo.limitador import LimitadorIntentos


class Reloj:
    def __init__(self): self.t = 1000.0
    def __call__(self): return self.t


def test_bloquea_al_superar_el_maximo_y_libera_al_vencer():
    reloj = Reloj()
    lim = LimitadorIntentos(maximo=3, ventana=60, reloj=reloj)
    for _ in range(2):
        lim.registrar_fallo("ip")
    assert lim.segundos_de_espera("ip") == 0
    lim.registrar_fallo("ip")
    assert lim.segundos_de_espera("ip") == 60
    reloj.t += 59
    assert lim.segundos_de_espera("ip") == 1
    reloj.t += 1
    assert lim.segundos_de_espera("ip") == 0


def test_claves_independientes_y_olvidar():
    lim = LimitadorIntentos(maximo=1, ventana=60, reloj=Reloj())
    lim.registrar_fallo("a")
    assert lim.segundos_de_espera("a") > 0 and lim.segundos_de_espera("b") == 0
    lim.olvidar("a")
    assert lim.segundos_de_espera("a") == 0
