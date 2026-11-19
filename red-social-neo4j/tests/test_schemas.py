import pytest
from pydantic import ValidationError

from schemas.personas_schema import AmistadIn, PersonaIn, PersonaUpdate


def test_persona_limpia_espacios_y_repetidos():
    p = PersonaIn(nombre="  Ana ", edad=20, ciudad="Mérida", intereses=["Cine", " Cine ", "Música"])
    assert p.nombre == "Ana"
    assert p.intereses == ["Cine", "Música"]


@pytest.mark.parametrize("campo,valor", [("edad", 5), ("edad", 200), ("nombre", "  "), ("ciudad", "")])
def test_persona_rechaza_valores_invalidos(campo, valor):
    datos = {"nombre": "Ana", "edad": 20, "ciudad": "Mérida", campo: valor}
    with pytest.raises(ValidationError):
        PersonaIn(**datos)


def test_persona_rechaza_campos_extra():
    with pytest.raises(ValidationError):
        PersonaIn(nombre="Ana", edad=20, ciudad="Mérida", id="hack")


def test_update_exige_un_campo_y_no_acepta_null():
    with pytest.raises(ValidationError):
        PersonaUpdate()
    with pytest.raises(ValidationError):
        PersonaUpdate(nombre=None)
    assert PersonaUpdate(edad=30).model_dump(exclude_unset=True) == {"edad": 30}


def test_amistad_no_a_si_misma():
    with pytest.raises(ValidationError):
        AmistadIn(persona_a_id="p01", persona_b_id="p01")
