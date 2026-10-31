"""Audit actual zipped game files, Lua helpers and ELF imports against core exports."""
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile
root=Path(__file__).resolve().parents[1]
package=Path(sys.argv[1]) if len(sys.argv)>1 else root/'firmware/platform/600D.102/build/magiclantern.zip'
with zipfile.ZipFile(package) as z, tempfile.TemporaryDirectory() as tmp:
    assert z.testzip() is None
    for path in ['ML/modules/arkanoid.mo','ML/modules/lua.mo','ML/scripts/pong.lua','ML/scripts/sokoban.lua','ML/scripts/lib/keys.lua','ML/scripts/lib/config.lua']:
        assert z.read(path),path
    core={line.split()[-1] for line in z.read('ML/modules/600D_102.sym').decode().splitlines() if line.strip()}
    for mod in ['arkanoid','lua']:
        path=Path(tmp)/(mod+'.mo');path.write_bytes(z.read('ML/modules/'+mod+'.mo'))
        symbols=subprocess.check_output(['readelf','-Ws',str(path)],text=True)
        imports={line.split()[-1] for line in symbols.splitlines() if ' UND ' in line and len(line.split())>7}
        assert not imports-core,(mod,sorted(imports-core))
        assert ('__module_info_'+mod) in symbols
        print(f'PASS packaged {mod}.mo: {len(imports)} imports resolve against packaged 600D_102.sym')
    for name,title in [('pong','Pong Game'),('sokoban','Sokoban Game')]:
        script=z.read('ML/scripts/'+name+'.lua')
        assert script==(root/'firmware/scripts'/(name+'.lua')).read_bytes()
        assert script.decode().split('--[[',1)[1].strip().splitlines()[0].strip()==title
    print('PASS Pong/Sokoban scripts and keys/config helpers are present in the actual ZIP')
