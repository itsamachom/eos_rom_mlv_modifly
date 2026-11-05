"""Run the production 600D MLU menu and mode callbacks with hardware I/O stubbed."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
shoot = (root / 'firmware/src/shoot.c').read_text()

def function(marker):
    start = shoot.index(marker)
    opening = shoot.index('{', start)
    end, depth = opening + 1, 1
    while depth:
        depth += (shoot[end] == '{') - (shoot[end] == '}')
        end += 1
    return shoot[start:end]

macros = shoot[shoot.index('#define MLU_ALWAYS_ON'):shoot.index('#ifdef FEATURE_MLU_HANDHELD_DEBUG')]
entry_start = shoot.index('    {\n        // 5DC can\'t do handheld MLU')
entry_end = shoot.index('\n    #endif', shoot.index('            MENU_EOL', entry_start))
entry = shoot[entry_start:entry_end]
program = r'''
#include <assert.h>
#include <string.h>
#include <stdio.h>
#define CONFIG_600D 1
#include "features.h"
#include "menu.h"
#ifdef FEATURE_MLU_HANDHELD
#error 600D must not compile the removed handheld shutter handler
#endif
#define DRIVE_SELFTIMER_2SEC 0x11
#define DRIVE_SELFTIMER_REMOTE 0x10
static int mlu_auto, mlu_mode, drive_mode, lens_mlu_delay;
static int canon_mlu, writes;
static int get_mlu(void) { return canon_mlu; }
static void set_mlu(int value) { assert(value == 0 || value == 1); canon_mlu=value; writes++; }
static MENU_UPDATE_FUNC(mlu_display) { (void)entry; (void)info; }
''' + macros + '\n' + '\n'.join(function(marker) for marker in [
    'static void mlu_normalize_mode(', 'static void mlu_selftimer_update()',
    'static void\nmlu_update()', 'static void\nmlu_toggle_mode(', 'static void\nmlu_toggle('
]) + '\nstatic struct menu_entry mlu_menu[] = {\n' + entry + r'''
};
int main(void) {
    struct menu_entry *mode = mlu_menu[0].children;
    assert(!strcmp(mode->name, "MLU mode") && mode->max == 1);
    assert(!strcmp(mode->choices[0], "Always ON"));
    assert(!strcmp(mode->choices[1], "Self-Timer"));
    assert(!strstr(mode->help2, "Handheld"));
    assert(!strcmp(mode[1].name, "Normal MLU Delay"));
    assert(mode[1].priv == &lens_mlu_delay && mode[2].priv == MENU_EOL_PRIV);
    for (int old=-1; old<=3; old++) {
        mlu_auto=1; mlu_mode=old; drive_mode=0x11; canon_mlu=0;
        mlu_selftimer_update();
        assert(mlu_mode == (old == 0 ? 0 : 1));
        assert(!MLU_HANDHELD);
    }
    mlu_auto=1; mlu_mode=2; drive_mode=0; canon_mlu=1;
    mlu_update(); assert(mlu_mode == 1 && !canon_mlu);
    for (int i=0; i<6; i++) {
        mode->select(NULL,1); assert(mlu_mode == i%2);
    }
    mlu_mode=1; drive_mode=0x10; canon_mlu=0;
    mlu_selftimer_update(); assert(canon_mlu);
    int before=writes;
    mlu_selftimer_update(); assert(writes == before);
    mlu_auto=0; mlu_update(); assert(!canon_mlu);
    puts("PASS 600D MLU menu has two modes and only normal delay; legacy handheld configs migrate; self-timer/ON/OFF remain functional");
}
'''
with tempfile.TemporaryDirectory() as tmp:
    source = Path(tmp) / 'mlu.c'
    binary = Path(tmp) / 'mlu'
    source.write_text(program)
    subprocess.run(['gcc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-Wno-unused-parameter',
                    '-iquote', str(root/'firmware/platform/600D.102'), '-iquote', str(root/'firmware/src'),
                    str(source), '-o', str(binary)], check=True)
    subprocess.run([str(binary)], check=True)
