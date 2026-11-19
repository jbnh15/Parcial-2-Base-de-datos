class NotFoundError(Exception):
    """El recurso pedido no existe."""


class ConflictError(Exception):
    """La operación choca con el estado actual (ej. amistad repetida)."""
