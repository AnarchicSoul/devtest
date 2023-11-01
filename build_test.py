import os
from script import get_hosting_type, create_output_dir, copy_files

# Crée un répertoire temporaire pour les tests
def temp_output_dir(tmp_path):
    return tmp_path / "output"

def test_get_hosting_type():
    config = {"hosting": {"onpremise": False, "cloud": True}}
    assert get_hosting_type(config) == "cloud"

def test_create_output_dir(temp_output_dir):
    assert create_output_dir("onpremise") == os.path.join(temp_output_dir, "onpremise")

def test_copy_files(temp_output_dir):
    config = {
        "hosting_type": "onpremise",
        "app1": {"enable": True, "version": "1.0", "ingresshost": "example.com"},
    }
    copy_files(config)

    # Vérifie si les fichiers ont été copiés correctement
    assert os.path.exists(os.path.join(temp_output_dir, "onpremise", "main.tf"))
    assert os.path.exists(os.path.join(temp_output_dir, "onpremise", "app1.tf"))
    assert os.path.exists(os.path.join(temp_output_dir, "onpremise", "app1.value"))

    # Vérifie si le contenu des fichiers a été correctement modifié
    with open(os.path.join(temp_output_dir, "onpremise", "app1.tf"), "r") as f:
        content = f.read()
        assert "version = '1.0'" in content

    with open(os.path.join(temp_output_dir, "onpremise", "app1.value"), "r") as f:
        content = f.read()
        assert "ingresshost = 'example.com'" in content
