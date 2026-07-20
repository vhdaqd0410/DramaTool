from pathlib import Path

from src.core.merger import rename_file, rename_files


def test_same_directory_rename_is_supported(tmp_path):
    source = tmp_path / "S01E01.mkv"
    target = tmp_path / "S01E02.mkv"
    source.write_text("episode")

    result = rename_file(source, target)

    assert result == target
    assert target.exists()
    assert not source.exists()


def test_batch_rename_creates_parent_directories_for_cross_folder_moves(tmp_path):
    source = tmp_path / "old" / "S01E01.mkv"
    target = tmp_path / "new" / "S01E02.mkv"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("episode")

    results = rename_files([(source, target)])

    assert results == [target]
    assert target.exists()
    assert not source.exists()
