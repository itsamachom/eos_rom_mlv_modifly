# SPDX-License-Identifier: GPL-2.0-or-later
"""Compare an external dietlibc source candidate with inherited ARM objects.

This is a provenance experiment, not a firmware build or a correspondence claim.
It writes only to an explicitly selected audit output directory. It never patches
v3r2 or updates the release readiness gate. Python standard library only.
"""
import argparse
from collections import Counter
import datetime
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

root = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--cc', type=Path, default=Path('/workspace/ml-env/toolchain/usr/bin/arm-none-eabi-gcc'))
a = p.parse_args()
source = a.source.resolve(); out = a.output.resolve()
if out.is_relative_to(source) or out.is_relative_to(root/'firmware'):
    raise SystemExit('Audit output must be outside the candidate source and firmware trees.')
if out.exists(): raise SystemExit('Choose a new output directory to preserve earlier evidence.')
out.mkdir(parents=True)
archive = root/'firmware/src/libs/dietlib-0.33-none-eabi-Os/dietlibc.a'
sha = lambda b: hashlib.sha256(b).hexdigest()

def ar_members(data):
    assert data[:8] == b'!<arch>\n'
    pos=8; names=b''; result={}
    while pos+60 <= len(data):
        h=data[pos:pos+60]; assert h[58:60]==b'`\n'
        length=int(h[48:58]); body=data[pos+60:pos+60+length]
        name=h[:16].decode().strip()
        if name=='//': names=body
        elif name!='/':
            if name.startswith('/') and name[1:].isdigit():
                name=names[int(name[1:]):].split(b'/\n',1)[0].decode()
            else: name=name.rstrip('/')
            assert name not in result, 'Duplicate member name: '+name
            result[name]={'data':body,'mtime':int(h[16:28] or b'0')}
        pos += 60+length+(length%2)
    assert pos==len(data)
    return result

def elf(data):
    assert data[:6]==b'\x7fELF\x01\x01'
    h=struct.unpack_from('<16sHHIIIIIHHHHHH',data)
    assert h[2]==40,'Not ARM'
    ss=[struct.unpack_from('<10I',data,h[6]+i*h[11]) for i in range(h[12])]
    raw=lambda s:data[s[4]:s[4]+s[5]]
    strings=raw(ss[h[13]])
    def cs(table,pos):return table[pos:].split(b'\0',1)[0].decode(errors='replace')
    sn=[cs(strings,s[0]) for s in ss]
    alloc={sn[i]:{'type':s[1],'flags':s[2],'alignment':s[8],'size':s[5],'sha256':sha(raw(s)) if s[1]!=8 else None}
           for i,s in enumerate(ss) if s[2]&2 and s[5]}
    tables={}; files=[]; exports=[]
    for i,s in enumerate(ss):
        if s[1]!=2:continue
        st=raw(ss[s[6]]); entries=[]
        for off in range(s[4],s[4]+s[5],s[9]):
            no,val,size,info,other,idx=struct.unpack_from('<IIIBBH',data,off)
            name=cs(st,no);entries.append(name)
            if info&15==4:files.append(name)
            if info>>4 in [1,2] and idx and name:
                exports.append((name,sn[idx] if idx<len(sn) else idx,val,size,info&15))
        tables[i]=entries
    relocs=[]
    for s in ss:
        if s[1]!=9:continue
        for off in range(s[4],s[4]+s[5],s[9]):
            pos,info=struct.unpack_from('<II',data,off)
            relocs.append((sn[s[7]],pos,info&255,tables[s[6]][info>>8]))
    return {'alloc':alloc,'relocations':sorted(relocs),'exports':sorted(exports),'source_files':files}

core=(root/'firmware/platform/Makefile').read_text()
lua=(root/'firmware/modules/lua/Makefile').read_text()
def object_list(text,name):
    match=re.search(r'^'+name+r'\s*=\s*\\\n(.*?)(?:\n\s*\n)',text,re.M|re.S)
    assert match,name
    return list(dict.fromkeys(re.findall(r'([A-Za-z0-9_]+\.o)',match[1])))
core_objects=object_list(core,'DIET_OBJS');lua_objects=object_list(lua,'DIET_OBJ_00')
needed=sorted(set(core_objects+lua_objects))
original=archive.read_bytes()
assert sha(original)=='21c61d561fbd852f46eb891052efaa8cd3c634261803793ffe600eac67861d9a', 'Unexpected v3r2 inherited archive'
members=ar_members(original)
# Isolated compile-time configuration experiment. The canonical source stays intact.
overlay=out/'small-strings-config';overlay.mkdir()
features=(source/'dietfeatures.h').read_bytes()
needle=b'#define WANT_FASTER_STRING_ROUTINES'
assert needle in features
(overlay/'dietfeatures.h').write_bytes(features.replace(needle,b'/* audit experiment: WANT_FASTER_STRING_ROUTINES disabled */',1))
flags=['-c','-Os','-mcpu=arm7tdmi','-marm','-nostdinc','-I'+str(overlay),'-I'+str(source),
       '-isystem',str(source/'include'),'-D__dietlibc__','-std=gnu89','-fomit-frame-pointer','-fstrict-aliasing']
version=subprocess.check_output([str(a.cc),'--version'],text=True).splitlines()[0]
rows=[]
vpath=['arm','syscalls.s','lib','libstdio','libugly','libcruft','libcrypt','libshell','liblatin1','libcompat','libdl','librpc','libregex','libm','profiling']
for obj in needed:
    inherited=members[obj]; dest=out/('inherited-'+obj); dest.write_bytes(inherited['data'])
    before=elf(inherited['data']);stem=obj[:-2]
    candidates=[source/d/(stem+ext) for d in vpath for ext in ['.S','.c'] if (source/d/(stem+ext)).is_file()]
    c=candidates[0] if candidates else None
    row={'object':obj,'consumers':[x for x,items in [('core',core_objects),('lua',lua_objects)] if obj in items],
         'archive_member_sha256':sha(inherited['data']),
         'archive_member_mtime_utc':datetime.datetime.fromtimestamp(inherited['mtime'],datetime.timezone.utc).isoformat(),
         'inherited_source_file_symbols':before['source_files'],
         'candidate_source':c.relative_to(source).as_posix() if c else None,
         'candidate_source_sha256':sha(c.read_bytes()) if c else None}
    if c:
        target=out/('candidate-'+obj)
        cmd=[str(a.cc),*flags,str(c),'-o',str(target)]
        run=subprocess.run(cmd,cwd=source,capture_output=True,text=True)
        (out/(obj+'.compile.log')).write_text(run.stdout+run.stderr)
        row['compile_exit_code']=run.returncode
        if run.returncode==0:
            after=elf(target.read_bytes())
            row['text_bytes_equal']=before['alloc'].get('.text')==after['alloc'].get('.text') if before['alloc'].get('.text') else None
            row['has_allocated_content']=bool(before['alloc'])
            row['all_alloc_sections_equal']=before['alloc']==after['alloc']
            row['relocations_equal']=before['relocations']==after['relocations']
            row['export_symbols_equal']=before['exports']==after['exports']
            row['allocated_image_and_relocations_equal']=row['all_alloc_sections_equal'] and row['relocations_equal'] and row['export_symbols_equal']
            row['inherited_alloc_sections']=before['alloc'];row['candidate_alloc_sections']=after['alloc']
    rows.append(row)
    print(obj, row.get('candidate_source'), 'compiled='+str(row.get('compile_exit_code')),
          'image_equal='+str(row.get('allocated_image_and_relocations_equal')))
headers=[]
for f in sorted((root/'firmware/modules/lua/dietlibc/include').rglob('*')):
    if not f.is_file():continue
    rel=f.relative_to(root/'firmware/modules/lua/dietlibc/include');candidate=source/'include'/rel
    headers.append({'path':rel.as_posix(),'inherited_sha256':sha(f.read_bytes()),
                    'candidate_sha256':sha(candidate.read_bytes()) if candidate.is_file() else None,
                    'identical':candidate.is_file() and f.read_bytes()==candidate.read_bytes()})
summary={'objects_used_by_core':len(core_objects),'objects_used_by_lua':len(lua_objects),'unique_objects':len(rows),
         'mapped_sources':sum(bool(r['candidate_source']) for r in rows),
         'compiled':sum(r.get('compile_exit_code')==0 for r in rows),
         'equal_text_sections':sum(r.get('text_bytes_equal') is True for r in rows),
         'equal_allocated_images_relocations_exports':sum(r.get('allocated_image_and_relocations_equal') is True for r in rows),
         'equal_nonempty_allocated_images_relocations_exports':sum(r.get('allocated_image_and_relocations_equal') is True and r.get('has_allocated_content') for r in rows),
         'equal_empty_objects':sum(r.get('allocated_image_and_relocations_equal') is True and not r.get('has_allocated_content') for r in rows),
         'headers_compared':len(headers),'identical_headers':sum(r['identical'] for r in headers)}
report={'archive_path':str(archive.relative_to(root)),'archive_sha256':sha(original),
        'source_candidate_directory':str(source),'compiler':version,'compile_flags':flags,
        'configuration_experiment':'Disable WANT_FASTER_STRING_ROUTINES in an isolated header overlay; do not alter inherited or source candidate files.',
        'source_correspondence_verified':False,'summary':summary,'objects':rows,'headers':headers}
assert archive.read_bytes()==original
(out/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(summary,indent=2))
