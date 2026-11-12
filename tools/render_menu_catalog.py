"""Capture the production Photo UI on the host, with an explicit source-only registry.

No camera values, native editors, or hardware-dependent callbacks are emulated.
The committed Thai atlas and RBF font glyphs are used without regenerating them.
Requires gcc and Pillow. Outputs a local gallery, PNGs, manifest and ZIP.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import html
import json
import os
import re
import subprocess
import tempfile
import zipfile
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = ['shoot.c', 'focus.c', 'picstyle.c', 'zebra.c', 'cropmarks.c',
                'movtweaks.c', 'bitrate.c', 'menu.c', 'debug.c', 'photo-camera-info-600d.h']
REGISTRATIONS = {
    'Shoot': [('shoot.c', 'shoot_menus')],
    'Focus': [('focus.c', 'trap_focus_menu'), ('focus.c', 'focus_menu')],
    'Expo': [('shoot.c', 'expo_menus'), ('picstyle.c', 'picstyle_features_menu')],
    'Overlay': [('zebra.c', 'zebra_menus'), ('cropmarks.c', 'cropmarks_menu')],
    'Movie': [('bitrate.c', 'mov_menus'), ('movtweaks.c', 'mov_menus'), ('movtweaks.c', 'movie_tweaks_menus')],
    'Movie Tweaks': [('bitrate.c', 'mov_tweak_menus')],
    'Prefs': [('menu.c', 'customize_menu')],
    'Help': [('photo-camera-info-600d.h', 'photo_camera_info_menu')],
    'Debug': [('debug.c', 'debug_menus')],
    'Modules': [], 'Display': [], 'Games': [], 'Scripts': [],
}
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\n]*|.', re.S)
STRING = re.compile(r'"(?:\\.|[^"\\])*"')


def strings(s):
    return ''.join(ast.literal_eval(m.group()) for m in STRING.finditer(s))


def split_top(s):
    """Split C initializer fields, retaining strings and nested initializers."""
    result = []; start = 0; depth = 0
    for m in TOKEN.finditer(s):
        t = m.group()
        if t.startswith(('"', '//', '/*')): continue
        if t in '({[': depth += 1
        elif t in ')}]': depth -= 1
        elif t == ',' and depth == 0:
            result.append(s[start:m.start()].strip()); start = m.end()
    result.append(s[start:].strip())
    return result


def brace(s, start):
    assert s[start] == '{'
    depth = 0
    for m in TOKEN.finditer(s, start):
        t = m.group()
        if t == '{': depth += 1
        elif t == '}':
            depth -= 1
            if not depth: return s[start + 1:m.start()], m.end()
    raise ValueError('Unclosed C initializer')


def parse_entries(body, source):
    result = []
    for part in split_top(body):
        if not part.startswith('{'): continue
        entry_body, _ = brace(part, 0)
        fields = {}
        for field in split_top(entry_body):
            m = re.match(r'\.(\w+)\s*=\s*(.*)', field, re.S)
            if m: fields[m[1]] = m[2].strip()
        if not fields.get('name', '').startswith('"'): continue
        node = {'name': strings(fields['name']), 'fields': fields, 'source': source}
        child = fields.get('children', '')
        if '{' in child:
            node['children'] = parse_entries(brace(child, child.index('{'))[0], source)
        else: node['children_ref'] = child
        result.append(node)
    return result


def preprocess(filename):
    source = (ROOT / 'firmware/src' / filename).read_text()
    text = re.sub(r'^\s*#\s*include\b.*$', '', source, flags=re.M)
    cmd = ['gcc', '-E', '-P', '-x', 'c', '-DCONFIG_600D=1', '-I' + str(ROOT / 'firmware/src'),
           '-include', str(ROOT / 'firmware/platform/600D.102/internals.h'),
           '-include', str(ROOT / 'firmware/platform/600D.102/features.h'), '-']
    out = subprocess.run(cmd, input=text, text=True, capture_output=True, check=True).stdout
    arrays = {}
    for m in re.finditer(r'(?:static\s+)?struct\s+menu_entry\s+(\w+)\s*\[\s*\]\s*=\s*\{', out):
        arrays[m[1]] = parse_entries(brace(out, m.end() - 1)[0], 'firmware/src/' + filename)
    return arrays


def cstring(s): return json.dumps(s, ensure_ascii=True)


def make_registry(arrays, targets):
    all_arrays = {name: entries for table in arrays.values() for name, entries in table.items()}
    def children(node): return node.get('children', all_arrays.get(node.get('children_ref'), []))
    declarations = []; calls = []
    def emit(node):
        ident = 'catalog_entry_' + str(len(calls))
        calls.append(ident)
        child_ids = [emit(child) for child in children(node)]
        f = node['fields']; name = node['name']
        # Most firmware callbacks require actual Canon state. Do not fake those values.
        callback = f.get('update', '')
        trusted = callback.startswith('photo_') and callback.endswith('_display')
        update = callback if trusted else 'catalog_unavailable'
        fields = [f'.name={cstring(name)}', f'.update={update}']
        if f.get('priv'): fields.append('.priv=&catalog_fixture_marker')
        if f.get('select'):
            fields.append('.select=' + ('menu_open_submenu' if f['select'] == 'menu_open_submenu' else 'catalog_no_action'))
        if f.get('icon_type', '').startswith('IT_'): fields.append('.icon_type=' + f['icon_type'])
        if f.get('help', '').startswith('"'): fields.append('.help=' + cstring(strings(f['help'])))
        if child_ids: fields.append('.children=&' + child_ids[0])
        declarations.append('static struct menu_entry ' + ident + '={' + ','.join(fields) + '};')
        for a, b in zip(child_ids, child_ids[1:]): init.append(f'{a}.next=&{b};')
        return ident
    init = []; menu_declarations = []; records = []
    for i, (menu, registrations) in enumerate(REGISTRATIONS.items()):
        entries = []
        for file, array in registrations:
            assert array in arrays[file], (file, array)
            entries += arrays[file][array]
        # Only the front end's exact bound root entries are needed here.
        entries = [e for e in entries if (menu, e['name']) in targets]
        ids = [emit(e) for e in entries]
        for a, b in zip(ids, ids[1:]): init.append(f'{a}.next=&{b};')
        mid = f'catalog_menu_{i}'
        menu_declarations.append(f'static struct menu {mid}={{.name={cstring(menu)}' + (f',.children=&{ids[0]}' if ids else '') + '};')
        if i: init.append(f'catalog_menu_{i-1}.next=&{mid};')
        for ident, node in zip(ids, entries):
            # Assign detail parent pointers; the front end only reads the registry.
            def parent_tree(ident):
                init.append(f'catalog_parent_tree(&{ident},&{mid});')
            parent_tree(ident)
            records.append(node)
    init.append('menus=&catalog_menu_0;')
    return '\n'.join(declarations + menu_declarations), '\n'.join(init), records


HOST_EXTRA = r'''
static void catalog_parent_tree(struct menu_entry *e,struct menu *parent) {
    for(;e;e=e->next) { e->parent_menu=parent;catalog_parent_tree(e->children,parent); }
}
static unsigned char * catalog_rbf(int font) {
    static unsigned char * buffers[5];int id=FONT_ID(font);
    if(!buffers[id]) {
        char path[1024];snprintf(path,sizeof(path),"%s/argnor%d.rbf",getenv("PHOTO_PROOF_RBF_DIR"),id==2?23:id==3?28:32);
        FILE * f=fopen(path,"rb");assert(f);assert(!fseek(f,0,SEEK_END));long size=ftell(f);rewind(f);
        buffers[id]=malloc(size);assert(buffers[id]);assert(fread(buffers[id],1,size,f)==(size_t)size);fclose(f);
    }return buffers[id];
}
static int catalog_width(int font,const char *s) {
    unsigned char * b=catalog_rbf(font);int h[11];memcpy(h,b+72,sizeof(h));int w=0;
    for(const unsigned char *p=(const unsigned char*)s;*p;p++) {
        assert(*p>=h[4] && *p<=h[5]);w+=b[h[7]+*p-h[4]];
    }return w;
}
static int catalog_fixture_marker;
static void catalog_no_action(void *priv,int delta) { (void)priv;(void)delta;assert(!"Capture must never execute a camera action"); }
static MENU_UPDATE_FUNC(catalog_unavailable) { (void)entry;MENU_SET_VALUE("Unavailable"); }
'''
HOST_MAIN = r'''
int main(void) {
    catalog_init();
    snprintf(build_version,sizeof(build_version),"PHOTO-UI-%s.600D.102",getenv("PHOTO_CATALOG_VERSION"));
    shutter_count_valid=0;
    FILE *meta=fopen(getenv("PHOTO_CATALOG_META"),"w");assert(meta);
    fprintf(meta,"[\n");int serial=0;
    for(int lang=0;lang<=1;lang++) {
        photo_thai_enabled=lang;
        for(int p=0;p<(int)COUNT(photo_pages);p++) {
            for(int item=0;item<photo_pages[p].count;item++) {
                photo_page_index=p;photo_selection[p]=item;photo_pane=PHOTO_ITEMS;
                photo_detail_index=0;photo_classic=submenu_level=edit_mode=0;photo_invalidate();
                struct menu *parent;struct menu_entry *root=photo_resolve(&photo_pages[p].items[item],&parent);
                int count=0;photo_detail_entry(root,-1,&count);
                for(int pane=0;pane<2;pane++) {
                    /* Every item view, then each available detail page. */
                    if(pane && !count)continue;
                    int pages=pane?(count+PHOTO_DETAIL_ROWS-1)/PHOTO_DETAIL_ROWS:1;
                    for(int page=0;page<pages;page++) {
                        photo_pane=pane?PHOTO_DETAILS:PHOTO_ITEMS;photo_detail_index=page*PHOTO_DETAIL_ROWS;
                        output[0]=0;assert(photo_menu_draw());
                        char name[128];snprintf(name,sizeof(name),"%s-%02d-%02d-%s-%02d",lang?"th":"en",p+1,item+1,pane?"options":"item",page+1);
                        save_proof(name);
                        char textpath[1024];snprintf(textpath,sizeof(textpath),"%s/%s.txt",getenv("PHOTO_PROOF_OUT"),name);
                        FILE *t=fopen(textpath,"w");assert(t);fputs(output,t);fclose(t);
                        if(serial++)fprintf(meta,",\n");
                        fprintf(meta,"{\"id\":\"%s\",\"language\":\"%s\",\"category\":%d,\"item\":%d,\"pane\":\"%s\",\"option_page\":%d,\"detail_count\":%d,\"root_registered\":%s}",name,lang?"th":"en",p,item,pane?"options":"item",page+1,count,root?"true":"false");
                    }
                }
            }
        }
    }
    fprintf(meta,"\n]\n");fclose(meta);puts("PASS production Photo UI captured all bound items/detail pages in both languages");return 0;
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    release = (ROOT / 'scripts/photo-ui-version.txt').read_text().strip()
    out = (args.output or ROOT / 'docs/menu-previews' / release).resolve(); out.mkdir(parents=True, exist_ok=True)
    assert re.fullmatch(r'v[0-9][A-Za-z0-9._-]*', release)
    front = (ROOT / 'firmware/src/photo-menu-600d.h').read_text()
    sections = []
    for m in re.finditer(r'static const struct photo_item (\w+)\[\] = \{(.*?)\n\};', front, re.S):
        rows = []
        for row in re.finditer(r'\{"([^"]+)", "([^"]+)", ("([^"]+)"|NULL)\}', m[2]):
            rows.append({'label': row[1], 'menu': row[2], 'entry': row[4]})
        sections.append(rows)
    assert len(sections) == 7
    targets = {(v['menu'], v['entry']) for page in sections for v in page if v['entry']}
    arrays = {file: preprocess(file) for file in SOURCE_FILES}
    declarations, init, records = make_registry(arrays, targets)
    harness = (ROOT / 'tests/photo_menu_test.c').read_text()
    # Keep the production renderer unchanged. Replace only host drawing adapters.
    harness = harness.replace('static int bmp_string_width(int font,const char * s) { return (int)strlen(s)*((font&255)==FONT_SMALL?8:(font&255)==FONT_MED?12:(font&255)==FONT_MED_LARGE?14:16); }',
                              'static int catalog_width(int font,const char *s);\nstatic int bmp_string_width(int font,const char *s) { return catalog_width(font,s); }')
    harness = harness.replace('(void)color;assert(x>=0 && xx<720 && y>=0 && yy<480);',
                              'assert(x>=0 && xx<720 && y>=0 && yy<480);assert(y==yy);for(int i=x;i<=xx;i++)framebuffer[y*720+i]=color;')
    assert 'return catalog_width(font,s)' in harness
    harness = harness.replace('int main(void)', 'int behavioral_test_main(void)', 1)
    harness = harness.replace('#include "../firmware/src/', '#include "' + str(ROOT / 'firmware/src') + '/')
    with tempfile.TemporaryDirectory(prefix='photo-menu-catalog-') as tmp:
        tmp = Path(tmp); c = tmp / 'capture.c'; binary = tmp / 'capture'
        c.write_text(harness + HOST_EXTRA + declarations + '\nstatic void catalog_init(void) {\n' + init + '\n}\n' + HOST_MAIN)
        subprocess.run(['gcc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-pthread', '-fsanitize=address,undefined', '-g', str(c), '-o', str(binary)], check=True)
        env = dict(os.environ, PHOTO_TEST_ATLAS=str(ROOT / 'firmware/data/photo_thai/PHOTO_TH.BIN'),
                   PHOTO_PROOF_RBF_DIR=str(ROOT / 'firmware/data/fonts'), PHOTO_PROOF_OUT=str(tmp),
                   PHOTO_CATALOG_META=str(tmp / 'screens.json'), PHOTO_CATALOG_VERSION=release,
                   ASAN_OPTIONS='detect_leaks=0')
        subprocess.run([str(binary)], env=env, check=True)
        screens = json.loads((tmp / 'screens.json').read_text())
        palette = {0: (0, 0, 0), 1: (255, 255, 255), 2: (20, 75, 150), 3: (255, 160, 50), 4: (80, 220, 255)}
        for i in range(10, 41): palette[i] = (max(0, (i - 10) * 7),) * 3
        for screen in screens:
            ident = screen['id']; image = Image.open(tmp / (ident + '.pgm'))
            assert image.size == (720, 480)
            raw = image.tobytes(); assert set(raw) <= palette.keys()
            image = Image.frombytes('RGB', (720, 480), b''.join(bytes(palette[x]) for x in raw))
            # Keep disclosure inside every standalone PNG, outside the original framebuffer.
            labeled = Image.new('RGB', (720, 510), '#111111'); labeled.paste(image, (0, 30))
            ImageDraw.Draw(labeled).text((10, 8), f'HOST RENDER {release} | source-only registry | camera values unavailable', fill='white')
            folder = out / screen['language']; folder.mkdir(exist_ok=True)
            path = folder / (ident + '.png'); labeled.save(path)
            item = sections[screen['category']][screen['item']]
            screen.update(item)
            screen['png'] = path.relative_to(out).as_posix()
            screen['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            screen['drawn_ascii'] = (tmp / (ident + '.txt')).read_text().splitlines()
    manifest = {'release': release, 'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'kind': 'production-renderer-host-capture', 'framebuffer': [720, 480], 'png_including_disclosure': [720, 510],
                'limitations': ['Not a Canon hardware or QEMU screenshot.', 'Palette is an illustrative host palette; actual camera colors may differ.',
                    'Camera-dependent callbacks and all editable values are replaced by Unavailable, not inferred.',
                    'Only real read-only project/build/camera-info callbacks run; model/Canon firmware are target fixtures, not camera readings.',
                    'Modules and game scripts are not registered: their unavailable state is intentional, not evidence of a missing feature.',
                    'Static 600D-enabled names/help/children are extracted with GCC preprocessing. Runtime row hiding/renaming/warnings are not emulated.',
                    'Classic/native editors opened with Q/SET, module lists, and game screens are not captured.'],
                'source_registry': records, 'screens': screens}
    (out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    lexicon = json.loads((ROOT / 'translations/photo_th.json').read_text())
    groups = ['S · Shoot', 'F · Focus', 'E · Expo', 'O · Overlay', 'V · Movie', '+ · Setup', 'G · Games']
    def title(s):
        key = s['label']; localized = lexicon.get(key, {}).get('th', key) if s['language'] == 'th' else key
        return localized + (' · ตัวเลือก ' if s['pane'] == 'options' else ' · เมนู ') + str(s['option_page'])
    body = ''
    for lang in ['th', 'en']:
        body += f'<section id="{lang}"><h2>{"ภาษาไทย" if lang == "th" else "English"}</h2>'
        for i, name in enumerate(groups):
            subset = [s for s in screens if s['language'] == lang and s['category'] == i]
            body += '<h3>' + html.escape(name) + '</h3><div class="grid">'
            for s in subset:
                text = html.escape(title(s)); path = html.escape(s['png'])
                body += f'<figure><a href="{path}" target="_blank" rel="noopener noreferrer"><img loading="lazy" width="720" height="510" src="{path}" alt="{text}"></a><figcaption>{text}</figcaption></figure>'
            body += '</div>'
        body += '</section>'
    gallery = '''<!doctype html><html lang="th"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thai-Menu — ภาพเมนูจากโค้ด</title><style>body{margin:0;background:#101512;color:#f3f5eb;font:18px system-ui;line-height:1.65}main{max-width:1520px;margin:auto;padding:24px}h1,h2,h3{color:#c7fb73}a{color:#74d7f7}.notice{border-left:4px solid #ffb99a;padding:16px;background:#18201b}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,540px),1fr));gap:22px}figure{margin:0}img{display:block;width:100%;height:auto}figcaption{padding:8px}nav{display:flex;gap:24px;flex-wrap:wrap}section{margin-top:48px}</style><main><h1>Thai-Menu ''' + release + ''' — ภาพเมนูจากโค้ด</h1><div class="notice"><strong>ภาพจำลองจากตัววาดเมนูจริงบนคอมพิวเตอร์ ไม่ใช่ภาพจับจากกล้อง</strong><p>ใช้ตำแหน่ง ข้อความไทย และฟอนต์จากโค้ดรุ่นนี้โดยตรง สีใช้พาเลตจำลอง ค่า “ยังใช้งานไม่ได้ / Unavailable” ใช้แทนค่าที่ต้องอ่านจากกล้อง ไม่ใช่ข้อผิดพลาดของกล้อง รุ่นกล้องและ Canon firmware เป็นค่าตัวอย่างของรุ่นเป้าหมาย ไม่ได้อ่านจากกล้องของคุณ</p><p>ชุดนี้ครอบคลุมรายการ 44 เมนูใน Photo UI และหน้าตัวเลือกที่กำหนดไว้ในโค้ดสำหรับ 600D โมดูลเสริมและเกมแสดงสถานะยังไม่โหลด ไม่รวมหน้าต่าง Classic/ตัวแก้ไขเดิม/รายการโมดูล/หน้าจอเกม และไม่จำลองการซ่อนแถวหรือคำเตือนตามสถานะกล้องจริง</p></div><nav><a href="#th">ภาษาไทย</a><a href="#en">English</a><a href="manifest.json">ข้อมูลภาพและแหล่งที่มา</a><a href="README.md">รายละเอียด</a><a href="../Thai-Menu-''' + release + '''-menu-captures.zip">ดาวน์โหลด ZIP ทั้งชุด</a></nav>''' + body + '<footer><p><a href="../../">FIRMWARE ADD-ON · Thai-Menu</a> · ผู้พัฒนา: <a href="https://www.youtube.com/@Online2easy" target="_blank" rel="noopener noreferrer">YouTube</a> · <a href="https://www.facebook.com/online2easy" target="_blank" rel="noopener noreferrer">Facebook</a> · <a href="https://online2hobby.blogspot.com/" target="_blank" rel="noopener noreferrer">Blog</a></p></footer></main></html>'
    (out / 'index.html').write_text(gallery)
    # One overview per language, one representative screen per category.
    for lang in ['th', 'en']:
        overview = Image.new('RGB', (1440, 4 * 540), '#101512'); d = ImageDraw.Draw(overview)
        for i in range(7):
            s = next(s for s in screens if s['language'] == lang and s['category'] == i and s['pane'] == 'item')
            x = (i % 2) * 720; y = (i // 2) * 540
            d.text((x + 10, y + 8), groups[i], fill='#c7fb73'); overview.paste(Image.open(out / s['png']), (x, y + 30))
        overview.save(out / ('overview-' + lang + '.png'))
    readme = f'''# Thai-Menu {release}: source-based menu captures\n\nGenerated with `python3 tools/render_menu_catalog.py`.\n\n- {len(screens)} PNGs: all 44 bound Photo UI items in Thai and English, plus all available source-defined immediate detail pages.\n- Open `index.html` after extracting the ZIP. No server or internet required.\n- Every PNG has a disclosure strip outside the unchanged 720×480 framebuffer.\n- Production renderer and Thai blitter: `firmware/src/photo-menu-600d.h`, `photo-thai-600d.h`; committed PHOTO_TH.BIN and argnor RBF glyphs.\n- Menu registry extracted from the real source with the 600D internals/features preprocessor configuration.\n- Source commit: `{manifest['source_commit']}`.\n\n## ข้อจำกัด / Limitations\n\n''' + '\n'.join('- ' + s for s in manifest['limitations']) + '''\n\nค่าจำนวนชัตเตอร์แสดงว่ายังใช้งานไม่ได้ ไม่ใส่จำนวนชัตเตอร์สมมุติ ภาพเป็นข้อมูลอ้างอิงโค้ด ไม่ใช่หลักฐานการทดสอบบนกล้องจริง\n\nภาพเมนูเกม/โมดูลที่ยังไม่ลงทะเบียนตรงกับสถานะยังไม่โหลด โดยไม่ได้รันเกมหรือ firmware updater\n\nDeveloper: https://itsamachom.github.io/eos_rom_mlv_modifly/\n\nCode and captures retain the firmware's GPL notices. Noto-derived Thai masks retain their OFL notices; see `assets/fonts/noto-sans-thai/OFL.txt` in the repository.\n'''
    (out / 'README.md').write_text(readme)
    licenses = out / 'licenses'; licenses.mkdir(exist_ok=True)
    for origin, filename in [('firmware/COPYING', 'GPL-2.0.txt'), ('assets/fonts/noto-sans-thai/OFL.txt', 'OFL.txt'), ('assets/fonts/noto-sans-thai/SOURCE.md', 'Noto-SOURCE.md')]:
        (licenses / filename).write_bytes((ROOT / origin).read_bytes())
    (licenses / 'NOTICE.md').write_text('Photo UI captures use Magic Lantern GPL-2.0-or-later rendering code and OFL Noto Sans Thai-derived phrase masks. The illustrated host palette and fixture registry do not change firmware. See the project source and included license notices.\n')
    archive = out.parent / f'Thai-Menu-{release}-menu-captures.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(out.parent))
    (archive.parent / (archive.name + '.sha256')).write_text(hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')
    print(f'{len(screens)} screenshots; gallery {out / "index.html"}; ZIP {archive}')


if __name__ == '__main__': main()
