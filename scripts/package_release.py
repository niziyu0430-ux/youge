"""Create a local, reviewable archive of the v0.2 content deliverables."""

from hashlib import sha256
import json
from pathlib import Path
import sys
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]


def main():
    verification=json.loads((ROOT/'reports/verification.json').read_text(encoding='utf-8'))
    if verification['status']!='passed' or verification['failures'] or verification['errors']:
        raise SystemExit('Run the current build and acceptance checks before packaging.')
    directories=['config','docs','youge','scripts','tests','examples','research','reports']
    allowed={'.json','.md','.py','.txt','.svg','.png'}
    files=[ROOT/'README.md',ROOT/'requirements-render.txt',ROOT/'.gitignore']
    for directory in directories:
        files += [p for p in (ROOT/directory).rglob('*') if p.is_file() and p.suffix in allowed and '__pycache__' not in p.parts]
    files=sorted(set(files),key=lambda p:p.relative_to(ROOT).as_posix())
    manifest={'product':'游格','release':'0.2.0','content_status':'原创待试测内容包；样例均为虚构',
              'acceptance_tests_passed':verification['tests_run'],
              'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha256(p.read_bytes()).hexdigest()} for p in files]}
    output=ROOT/'deliverables';output.mkdir(exist_ok=True)
    manifest_bytes=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    (output/'release-manifest.json').write_bytes(manifest_bytes)
    archive=output/'youge-v0.2-content.zip'
    with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as stream:
        for p in files:
            info=ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(2026,10,26,0,0,0))
            info.compress_type=ZIP_DEFLATED
            stream.writestr(info,p.read_bytes())
        info=ZipInfo('release-manifest.json',date_time=(2026,10,26,0,0,0))
        info.compress_type=ZIP_DEFLATED
        stream.writestr(info,manifest_bytes)
    with ZipFile(archive) as stream:
        if stream.testzip() is not None:raise SystemExit('Archive integrity check failed')
        for item in manifest['files']:
            if sha256(stream.read(item['path'])).hexdigest()!=item['sha256']:
                raise SystemExit('Archive content does not match the manifest')
    print(json.dumps({'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,'checks':verification['tests_run']},ensure_ascii=True))


if __name__=='__main__':main()
