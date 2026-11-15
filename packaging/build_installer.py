"""Build the Windows Setup EXE from a fresh, checked application payload."""
import argparse
import hashlib
from pathlib import Path
import subprocess

from build_windows import ROOT, VERSION, assemble, build_app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iscc', required=True, type=Path, help='Path to the Inno Setup ISCC.exe compiler')
    compiler = parser.parse_args().iscc.resolve()
    if not compiler.is_file():
        parser.error('ISCC.exe was not found at the specified path.')

    payload = assemble(build_app(), portable=False)
    output = ROOT / 'local-data/releases'
    output.mkdir(parents=True, exist_ok=True)
    name = f'GW2-VLM-COPILOT-v{VERSION}-windows-x64-Setup'
    subprocess.run(
        [str(compiler), f'/DAppVersion={VERSION}', f'/DPayload={payload}',
         f'/O{output}', f'/F{name}', str(ROOT / 'packaging/windows_installer.iss')],
        check=True,
        cwd=ROOT,
    )
    installer = output / f'{name}.exe'
    with installer.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    installer.with_suffix('.exe.sha256').write_text(f'{digest}  {installer.name}\n', encoding='utf-8')
    print(installer)


if __name__ == '__main__':
    main()
