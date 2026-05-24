import pytest
from pathlib import Path
from promptdoc import (
    IgnoreEngine,
    build_tree_representation,
    get_language_tag,
    is_binary,
    bundle_files,
    call_gemini_api,
)


def test_ignore_engine_global_exclusions(tmp_path):
    # Create files/dirs that should be globally ignored
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("dummy", encoding="utf-8")

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "package.json").write_text("dummy", encoding="utf-8")

    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "bin" / "python").mkdir(parents=True, exist_ok=True)

    promptdoc_out = tmp_path / "promptdoc_output"
    promptdoc_out.mkdir()
    (promptdoc_out / "prompt_payload.md").write_text("payload", encoding="utf-8")

    normal_dir = tmp_path / "src"
    normal_dir.mkdir()
    normal_file = normal_dir / "main.py"
    normal_file.write_text("print('hello')", encoding="utf-8")

    pyc_file = normal_dir / "main.pyc"
    pyc_file.write_text("binary", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    
    assert ignore_engine.is_ignored(git_dir) is True
    assert ignore_engine.is_ignored(git_dir / "config") is True
    assert ignore_engine.is_ignored(node_modules) is True
    assert ignore_engine.is_ignored(venv_dir) is True
    assert ignore_engine.is_ignored(promptdoc_out) is True
    assert ignore_engine.is_ignored(promptdoc_out / "prompt_payload.md") is True
    assert ignore_engine.is_ignored(pyc_file) is True
    assert ignore_engine.is_ignored(normal_file) is False

def test_ignore_engine_gitignore_patterns(tmp_path):
    # Write .gitignore
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("""
# This is a comment
*.log
/config
build/
    """, encoding="utf-8")

    # Files to check
    log_file = tmp_path / "app.log"
    log_file.write_text("log", encoding="utf-8")

    nested_log = tmp_path / "src" / "debug.log"
    nested_log.parent.mkdir(exist_ok=True)
    nested_log.write_text("log", encoding="utf-8")

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "settings.json"
    config_file.write_text("{}", encoding="utf-8")

    nested_config_dir = tmp_path / "src" / "config"
    nested_config_dir.mkdir(exist_ok=True)
    nested_config_file = nested_config_dir / "settings.json"
    nested_config_file.write_text("{}", encoding="utf-8")

    build_dir = tmp_path / "build"
    build_dir.mkdir()
    build_file = build_dir / "output.txt"
    build_file.write_text("output", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)

    assert ignore_engine.is_ignored(log_file) is True
    assert ignore_engine.is_ignored(nested_log) is True
    assert ignore_engine.is_ignored(config_dir) is True
    assert ignore_engine.is_ignored(config_file) is True
    assert ignore_engine.is_ignored(nested_config_file) is False  # /config only matches root config
    assert ignore_engine.is_ignored(build_file) is True

def test_build_tree_representation(tmp_path):
    # Setup folders
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "src" / "utils.py").write_text("def run(): pass", encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.json").write_text("{}", encoding="utf-8")
    (tmp_path / "README.md").write_text("Read me", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    tree_str = build_tree_representation(tmp_path, ignore_engine, max_depth=3)

    assert "." in tree_str
    assert "src/" in tree_str
    assert "main.py" in tree_str
    assert "config/" in tree_str
    assert "settings.json" in tree_str
    assert "README.md" in tree_str

def test_get_language_tag():
    assert get_language_tag(Path("main.py")) == "python"
    assert get_language_tag(Path("script.sh")) == "bash"
    assert get_language_tag(Path("config.json")) == "json"
    assert get_language_tag(Path("unknown.xyz")) == "text"

def test_is_binary(tmp_path):
    txt_file = tmp_path / "text.txt"
    txt_file.write_text("Normal printable text", encoding="utf-8")
    
    bin_file = tmp_path / "binary.bin"
    bin_file.write_bytes(b"\x00\x01\x02\x03\x04\x05")

    assert is_binary(txt_file) is False
    assert is_binary(bin_file) is True

def test_bundle_files_and_size_threshold(tmp_path):
    # Normal file
    normal_file = tmp_path / "main.py"
    normal_file.write_text("print('hello')", encoding="utf-8")

    # Large file (> 500KB)
    large_file = tmp_path / "large.txt"
    large_file.write_text("A" * (501 * 1024), encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    warnings = []
    bundled_str, count, bytes_saved = bundle_files(tmp_path, ignore_engine, warnings)

    assert count == 2
    assert "### main.py" in bundled_str
    assert "print('hello')" in bundled_str
    assert "### large.txt" in bundled_str
    assert "[PromptDoc Warning: File size exceeds 500KB threshold. Raw code excluded to prevent token window overflow.]" in bundled_str
    assert bytes_saved > 0
    assert any("Excluded large file contents" in w for w in warnings)

def test_call_gemini_api():
    from unittest.mock import patch
    import io
    
    mock_response = io.BytesIO(b'{"candidates": [{"content": {"parts": [{"text": "Mocked response text"}]}}]}')
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_response
        res = call_gemini_api("dummy_key", "hello", "system instructions")
        assert res == "Mocked response text"

