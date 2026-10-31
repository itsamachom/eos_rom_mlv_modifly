"""Execute the production menu registry and Arkanoid init/start on a host.

Only hardware services and unrelated presentation helpers are stubbed. This
checks registration and task dispatch, not playing a game on Canon hardware.
"""
from pathlib import Path
import subprocess
import tempfile
root=Path(__file__).resolve().parents[1]
menu=(root/'firmware/src/menu.c').read_text()
def function(text, marker):
    start=text.index(marker);op=text.index('{',start);depth=1;end=op+1
    while depth:
        depth += (text[end]=='{')-(text[end]=='}');end+=1
    return text[start:end]
registry=function(menu,'void menu_add_internal(')
ark=(root/'firmware/modules/arkanoid/arkanoid.c').read_text()
start=function(ark,'static MENU_SELECT_FUNC(arkanoid_start)')
init=function(ark,'static unsigned int arkanoid_init()')
a=ark.index('static struct menu_entry arkanoid_menu[]');b=ark.index('\n};',a)+3
entries=ark[a:b]
program=r'''
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "menu.h"
#define CONFIG_600D 1
#define streq(a,b) (!strcmp(a,b))
#define ASSERT assert
#define COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define ICON_ML_SUBMENU 100
static int menu_flags_load_dirty,duplicate_check_dirty;
static struct menu all[12];static int nmenus;
static struct menu *menu_find_by_name_internal(const char *name,int icon) {
 for(int i=0;i<nmenus;i++)if(!strcmp(all[i].name,name) && all[i].icon==icon)return &all[i];
 assert(nmenus<12);struct menu *m=&all[nmenus++];m->name=name;m->icon=icon;return m;
}
void menu_open_submenu(void *p,int d){(void)p;(void)d;}
static void menu_update_split_pos(struct menu*m,struct menu_entry*e){(void)m;(void)e;}
static void menu_update_placeholder(struct menu*m,struct menu_entry*e){(void)m;(void)e;}
static void entry_guess_icon_type(struct menu_entry*e){if(e->icon_type==IT_AUTO)e->icon_type=e->select==menu_open_submenu?IT_SUBMENU:IT_ACTION;}
'''+registry+r'''
void menu_add(const char *n,struct menu_entry*e,int c){menu_add_internal(n,e,c);}
static int starts,level,sound;
static void arkanoid_task(void){}
#define DryosDebugMsg(...) ((void)0)
static void task_create(const char*n,int priority,int stack,void(*fn)(void),void *arg){
 assert(!strcmp(n,"arkanoid_task") && priority==0x1c && stack==0x1000 && fn==arkanoid_task && !arg);starts++;
}
static MENU_SELECT_FUNC(level_select){(void)priv;(void)delta;}
'''+start+'\n'+entries+'\n'+init+r'''
int main(void){
 assert(!arkanoid_init());
 struct menu*m=NULL;for(int i=0;i<nmenus;i++)if(!strcmp(all[i].name,"Games") && all[i].icon!=ICON_ML_SUBMENU)m=&all[i];
 assert(m && m->children==arkanoid_menu);
 assert(!strcmp(m->children->name,"Arkanoid") && m->children->parent_menu==m);
 assert(m->children->icon_type==IT_ACTION && m->children->select);
 assert(!strcmp(m->children->children->name,"Level") && m->children->children->next);
 m->children->select(m->children->priv,1);assert(starts==1);
 puts("PASS production Arkanoid init registers Games/Arkanoid and actual start creates its game task");
}
'''
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'registry.c';path.write_text(program)
    subprocess.run(['gcc','-std=c11','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-I',str(root/'firmware/src'),str(path),'-o',tmp+'/registry'],check=True)
    subprocess.run([tmp+'/registry'],check=True)
