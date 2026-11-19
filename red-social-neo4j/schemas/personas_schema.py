from datetime import date
from typing import Annotated, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

Texto80 = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]
Interes = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)]


class PersonaIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Texto80
    edad: int = Field(ge=13, le=120)
    ciudad: Texto80
    intereses: list[Interes] = Field(default_factory=list, max_length=20)

    @field_validator("intereses")
    @classmethod
    def sin_repetidos(cls, valor: list[str]) -> list[str]:
        return list(dict.fromkeys(valor))


class PersonaUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Texto80 | None = None
    edad: int | None = Field(default=None, ge=13, le=120)
    ciudad: Texto80 | None = None

    @model_validator(mode="after")
    def al_menos_un_campo(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Manda al menos un campo para actualizar")
        # null en Neo4j borraría la propiedad, así que no se acepta
        if any(getattr(self, campo) is None for campo in self.model_fields_set):
            raise ValueError("Los campos enviados no pueden ser null")
        return self


class InteresIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: Interes


class AmistadIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    persona_a_id: Texto80
    persona_b_id: Texto80
    desde: date = Field(default_factory=date.today)

    @model_validator(mode="after")
    def no_a_si_misma(self) -> Self:
        if self.persona_a_id == self.persona_b_id:
            raise ValueError("Una persona no puede ser amiga de sí misma")
        return self
