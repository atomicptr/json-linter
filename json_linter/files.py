""" Gather files """
from pathlib import Path
from typing import List, Optional


def gather_files(
    filename: str,
    extensions: Optional[List[str]] = None,
    recursive: bool = False
) -> List[Path]:
    """ Gather files """
    if extensions is None or len(extensions) == 0:
        extensions = ["json"]

    file_path = Path(Path.cwd(), filename)

    if not file_path.exists():
        return []

    if file_path.is_file():
        return [file_path]

    if file_path.is_dir():
        files: List[Path] = []
        glob = "**/*.%s" if recursive else "*.%s"

        for ext in extensions:
            files.extend(file_path.glob(glob % ext))
        return files

    return []
