"""Reproducible portable Windows build; never include local account data or models."""
import subprocess,sys,shutil,json,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEV_MODULES=('waypoint.storage.vision_review','waypoint.testing','waypoint.ui.player_setup')
DEV_PATHS={'tests','fixtures','text-playtests','vision-review','test-catalog'}
DEV_FILES={'AGENTS.md','run-gw2-vision-review.cmd','run-gw2-wiki-for-training.cmd',
           'run-gw2-wiki-no-account.cmd','stop-gw2-wiki-for-training.cmd',
           'run_text_sessions.py','refresh_gw2_test_catalog.py','benchmark_local.py',
           'playtest_edges.py','playtest_local.py','verify_window_capture.py'}
def main():
    build=ROOT/'local-data/package-build'
    exclusions=[arg for module in DEV_MODULES for arg in ('--exclude-module',module)]
    subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--clean','--onedir','--windowed',*exclusions,'--name','GW2-VLM-COPILOT','--paths',str(ROOT/'src'),'--collect-all','windows_capture','--icon',str(ROOT/'assets/branding/gw2-vlm-copilot.ico'),'--distpath',str(build/'dist'),'--workpath',str(build/'work'),'--specpath',str(build/'spec'),str(ROOT/'tools/run_gui.py')],cwd=ROOT,check=True)
    return assemble(build/'dist/GW2-VLM-COPILOT')
def assemble(folder):
    for name in ('gw2-vlm-copilot-24.png','gw2-vlm-copilot-32.png','gw2-vlm-copilot.ico'):
        target=folder/'assets/branding'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'assets/branding'/name,target)
    target=folder/'assets/ui/slider-thumb.png';target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'assets/ui/slider-thumb.png',target)
    for name in ('LICENSE','README.md','requirements.txt'):shutil.copy2(ROOT/name,folder/name)
    for name in ('Uninstall.cmd','Uninstall.ps1'):shutil.copy2(ROOT/'packaging'/name,folder/name)
    (folder/'Models').mkdir(exist_ok=True)
    for name in ('WINDOWS_PACKAGE.md','SETUP.md','DEVELOPMENT.md','THIRD_PARTY.md','PRIVACY.md'):
        target=folder/'docs'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'docs'/name,target)
    licenses=folder/'THIRD-PARTY-LICENSES';licenses.mkdir(exist_ok=True)
    import importlib.metadata as metadata
    for name in ('windows-capture','numpy','opencv-python','pyinstaller'):
        distribution=metadata.distribution(name)
        for path in distribution.files or []:
            if any(word in str(path).lower() for word in ('license','copying','notice')) and distribution.locate_file(path).is_file():
                target=licenses/name/str(path);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(distribution.locate_file(path),target)
    forbidden=('local-data','credentials','__pycache__')
    manifest=[]
    for path in sorted(folder.rglob('*')):
        if not path.is_file():continue
        if path.name=='PACKAGE-MANIFEST.json':continue
        relative=path.relative_to(folder)
        if DEV_PATHS.intersection(relative.parts) or path.name in DEV_FILES:
            raise RuntimeError('Development artifact in package: '+str(relative))
        if any(part in forbidden for part in relative.parts) or path.suffix in ('.gguf','.dpapi','.log') or path.name.endswith('.local.json'):raise RuntimeError('Private artifact in package: '+str(relative))
        manifest.append({'path':relative.as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (folder/'PACKAGE-MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    output=ROOT/'local-data/releases';output.mkdir(parents=True,exist_ok=True)
    archive=output/'GW2-VLM-COPILOT-v0.1.8-alpha-windows-x64.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as zipped:
        zipped.writestr(folder.name+'/Models/',b'')
        for path in folder.rglob('*'):
            if path.is_file():zipped.write(path,Path(folder.name)/path.relative_to(folder))
    digest=hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
    print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'sha256':digest}));return archive
if __name__=='__main__':main()
