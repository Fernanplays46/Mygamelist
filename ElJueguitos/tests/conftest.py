import pytest
import warnings
@pytest.fixture(autouse=True)
def _silence_resourcewarnings(recwarn):
    recwarn.clear()  # limpia warnings ruidosos en Windows/SQLite
warnings.filterwarnings("ignore", message="unclosed database", category=ResourceWarning)

