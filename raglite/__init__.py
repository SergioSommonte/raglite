"""Application factory per RAGlite."""

from __future__ import annotations

import os

from flask import Flask

def create_app(test_config: dict | None = None) -> Flask:
    """Crea e configura l'istanza Flask.

    Args:
        test_config: dizionario di configurazione usato nei test
                     per sovrascrivere i valori di default.
                     Se None, viene caricato instance/config.py (se esiste).
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "raglite.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    print(app.instance_path)

    from . import rag
    app.register_blueprint(rag.bp)

    return app