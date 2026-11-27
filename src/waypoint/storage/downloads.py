"""Verified, resumable first-run downloads into app-owned resource folders."""
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import msvcrt
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
from urllib.request import HTTPRedirectHandler, Request, build_opener
import zipfile


@dataclass(frozen=True)
class Resource:
    key: str
    label: str
    url: str
    source: str
    filename: str
    folder: str
    size: int
    sha256: str
    expected: tuple = ()


LLAMA_RELEASE = 'https://github.com/ggml-org/llama.cpp/releases/tag/b12387'
LLAMA_ASSETS = 'https://github.com/ggml-org/llama.cpp/releases/download/b12387/'
QWEN_SOURCE = 'https://huggingface.co/unsloth/Qwen3.5-4B-GGUF'
GEMMA_SOURCE = 'https://huggingface.co/lmstudio-community/gemma-4-12B-it-QAT-GGUF'
RESOURCES = (
    Resource('server', 'llama.cpp Windows x64 server (CUDA 12.4)',
             LLAMA_ASSETS+'llama-b12387-bin-win-cuda-12.4-x64.zip', LLAMA_RELEASE,
             'llama-b12387-bin-win-cuda-12.4-x64.zip', 'runtime/llama-b12387',
             319407424, '939c94e827c8bc74e2841c5b05643cf35a81b46ec01c6fb0d2732ed41970c2e7',
             ('llama-server.exe', 'llama-server-impl.dll')),
    Resource('cuda', 'Matching NVIDIA CUDA 12.4 DLLs',
             LLAMA_ASSETS+'cudart-llama-bin-win-cuda-12.4-x64.zip', LLAMA_RELEASE,
             'cudart-llama-bin-win-cuda-12.4-x64.zip', 'runtime/llama-b12387',
             391443627, '8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6',
             ('cudart64_12.dll', 'cublas64_12.dll', 'cublasLt64_12.dll')),
    Resource('qwen', 'Qwen 3.5 4B Q4_K_M',
             QWEN_SOURCE+'/resolve/e87f176479d0855a907a41277aca2f8ee7a09523/Qwen3.5-4B-Q4_K_M.gguf',
             QWEN_SOURCE, 'Qwen3.5-4B-Q4_K_M.gguf', 'Models', 2740937888,
             '00fe7986ff5f6b463e62455821146049db6f9313603938a70800d1fb69ef11a4'),
    Resource('gemma', 'Gemma 4 12B QAT Q4_0',
             GEMMA_SOURCE+'/resolve/aaec3dd9d1012557147a627142759994d1fd8d37/gemma-4-12B-it-QAT-Q4_0.gguf',
             GEMMA_SOURCE, 'gemma-4-12B-it-QAT-Q4_0.gguf', 'Models', 6975879008,
             'f568ac5de71c8fcac5d5794494388ad94db9e18b4368ca897e21b30d2448eeec'),
    Resource('projector', 'Gemma vision companion (for screen vision)',
             GEMMA_SOURCE+'/resolve/aaec3dd9d1012557147a627142759994d1fd8d37/mmproj-gemma-4-12B-it-QAT-BF16.gguf',
             GEMMA_SOURCE, 'mmproj-gemma-4-12B-it-QAT-BF16.gguf', 'Models', 175115328,
             'd027f45ce5522f0e4dd2f777049c9a0cd3abbfddf7f4efe5ade22610d9b9ab54'),
)


class DownloadCancelled(Exception):
    pass


class HTTPSRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, url):
        if not url.lower().startswith('https://'):
            raise ValueError('The download redirected to an insecure connection.')
        return super().redirect_request(request, fp, code, message, headers, url)


def check_cancel(cancel):
    if cancel.is_set():
        raise DownloadCancelled('Download cancelled. Click Download selected to resume.')


def safe_path(root, relative):
    """Reject archive traversal and existing links before creating any target."""
    root = Path(root).absolute()
    name = PurePosixPath(str(relative).replace('\\', '/'))
    if name.is_absolute() or not name.parts or any(part in ('.', '..') or ':' in part for part in name.parts):
        raise ValueError('Unsafe resource file path.')
    target = root.joinpath(*name.parts)
    for ancestor in (target, *target.parents):
        if ancestor.is_symlink() or ancestor.is_junction():
            raise ValueError('Resource folders cannot contain links or junctions.')
    return target


@contextmanager
def download_lock(cache):
    lock_path = safe_path(cache, 'setup.lock')
    with lock_path.open('a+b') as lock:
        if lock.tell() == 0:
            lock.write(b'0')
            lock.flush()
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as error:
            raise RuntimeError('Another Setup window is downloading. Let it finish and try again.') from error
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def file_hash(path, cancel, progress):
    digest = hashlib.sha256()
    size = path.stat().st_size
    completed = 0
    with path.open('rb') as stream:
        while chunk := stream.read(1024*1024):
            check_cancel(cancel)
            digest.update(chunk)
            completed += len(chunk)
            progress('Verifying', completed, size)
    return digest.hexdigest()


def download_file(resource, target, cancel, progress, opener):
    offset = target.stat().st_size if target.exists() else 0
    if offset > resource.size:
        target.unlink()
        offset = 0
    if shutil.disk_usage(target.parent).free < resource.size-offset:
        raise OSError('There is not enough disk space for this resource.')
    if offset < resource.size:
        headers = {'User-Agent': 'GW2-VLM-COPILOT-Setup/0.1'}
        if offset:
            headers['Range'] = f'bytes={offset}-'
        request = Request(resource.url, headers=headers)
        with opener.open(request, timeout=20) as response:
            if response.status == 200:
                offset = 0
            elif response.status != 206 or response.headers.get('Content-Range') != f'bytes {offset}-{resource.size-1}/{resource.size}':
                raise ValueError('The server returned an unexpected download range.')
            with target.open('ab' if offset else 'wb') as stream:
                progress('Downloading', offset, resource.size)
                while True:
                    check_cancel(cancel)
                    chunk = response.read(1024*1024)
                    if not chunk:
                        break
                    offset += len(chunk)
                    if offset > resource.size:
                        raise ValueError('The downloaded resource exceeds its expected size.')
                    stream.write(chunk)
                    progress('Downloading', offset, resource.size)
    if target.stat().st_size != resource.size:
        raise OSError('The download was interrupted. Click Download selected to resume.')
    if file_hash(target, cancel, progress) != resource.sha256:
        target.unlink()
        raise ValueError('Checksum verification failed. Click Download selected to download a fresh copy.')


def extract_archive(resource, archive_path, folder, cache, cancel, progress):
    """Stage and validate every ZIP entry, then publish complete individual files."""
    with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(dir=cache) as temporary:
        staging = Path(temporary)
        entries = [entry for entry in archive.infolist() if not entry.is_dir()]
        total = sum(entry.file_size for entry in entries)
        if len(entries) > 1000 or total > 4*1024**3:
            raise ValueError('The archive exceeds its extraction limit.')
        if shutil.disk_usage(cache).free < total:
            raise OSError('There is not enough disk space to extract this resource.')
        names = set()
        for entry in archive.infolist():
            safe_path(staging, entry.filename)
            if stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError('The archive contains a symbolic link.')
            if entry.is_dir():
                continue
            name = entry.filename.casefold()
            if name in names:
                raise ValueError('The archive contains duplicate file paths.')
            names.add(name)
        if not all(name.casefold() in names for name in resource.expected):
            raise ValueError('The archive is missing required runtime files.')
        manifest = {}
        completed = 0
        for entry in entries:
            check_cancel(cancel)
            target = safe_path(staging, entry.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256()
            with archive.open(entry) as source, target.open('wb') as destination:
                while chunk := source.read(1024*1024):
                    check_cancel(cancel)
                    destination.write(chunk)
                    digest.update(chunk)
                    completed += len(chunk)
                    progress('Extracting', completed, total)
            manifest[entry.filename] = digest.hexdigest()
        for name in manifest:
            check_cancel(cancel)
            target = safe_path(folder, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(safe_path(staging, name), target)
        return manifest


def install_resource(resource, root, cancel, progress, opener=None):
    root = Path(root)
    cache = safe_path(root, 'local-data/resource-downloads')
    cache.mkdir(parents=True, exist_ok=True)
    folder = safe_path(root, resource.folder)
    folder.mkdir(parents=True, exist_ok=True)
    result = safe_path(folder, resource.expected[0] if resource.expected else resource.filename)
    with download_lock(cache):
        check_cancel(cancel)
        manifest_path = safe_path(cache, resource.key+'.json')
        if resource.expected:
            try:
                saved = json.loads(manifest_path.read_text('utf-8'))
                files = saved['files']
                if (isinstance(files, dict) and saved['sha256'] == resource.sha256
                        and all(name in files for name in resource.expected)):
                    if all(safe_path(folder, name).is_file() and file_hash(safe_path(folder, name), cancel, progress) == digest
                           for name, digest in files.items()):
                        return result
            except (OSError, ValueError, KeyError, TypeError):
                pass
        elif result.is_file() and result.stat().st_size == resource.size:
            if file_hash(result, cancel, progress) == resource.sha256:
                return result
        partial = safe_path(cache, resource.filename+'.part')
        download_file(resource, partial, cancel, progress, opener or build_opener(HTTPSRedirect()))
        check_cancel(cancel)
        if resource.expected:
            files = extract_archive(resource, partial, folder, cache, cancel, progress)
            temporary = safe_path(cache, resource.key+'.json.tmp')
            temporary.write_text(json.dumps({'sha256':resource.sha256, 'files':files}), encoding='utf-8')
            os.replace(temporary, manifest_path)
            partial.unlink()
        else:
            os.replace(partial, result)
        return result
