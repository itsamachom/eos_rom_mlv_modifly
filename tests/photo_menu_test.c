/* Host-side behavioral tests of the production 600D menu front end.
 * Camera I/O and ML editing are stubbed; these tests do not validate hardware.
 */
#include <assert.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include "../firmware/src/menu.h"

#define CONFIG_600D 1
#define COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define MOD(a,b) ((((int)(a)%(int)(b))+(int)(b))%(int)(b))
#define streq(a,b) (!strcmp(a,b))
#define ICON_ML_SUBMENU 100
#define FONT_SMALL 1
#define FONT_MED 2
#define FONT_MED_LARGE 3
#define FONT_LARGE 4
#define COLOR_BLACK 0
#define COLOR_WHITE 1
#define COLOR_BLUE 2
#define COLOR_ORANGE 3
#define COLOR_CYAN 4
#define COLOR_GRAY(a) ((a)+10)
#define FONT(font,fg,bg) ((font)|((fg)<<8)|((bg)<<16))
enum { BGMT_INFO=1, BGMT_PRESS_LEFT, BGMT_WHEEL_LEFT, BGMT_PRESS_RIGHT,
       BGMT_WHEEL_RIGHT, BGMT_PRESS_UP, BGMT_WHEEL_UP, BGMT_PRESS_DOWN,
       BGMT_WHEEL_DOWN, BGMT_MENU, BGMT_PRESS_SET, BGMT_Q, BGMT_PLAY };
static int submenu_level,edit_mode,menu_lv_transparent_mode,menu_help_active;
static int recording,locks,close_requests,actions,last_mode;
static struct menu * menus;
static struct menu_entry * last_entry;
static const int menu_sem=1,gui_sem=2;
#define SUBMENU_OR_EDIT (submenu_level || edit_mode)
#define RECORDING recording
static char output[30000];
static int text_count;
static int bmp_string_width(int font,const char * s) { return (int)strlen(s)*((font&255)==FONT_SMALL?8:12); }
static void bmp_printf(int font,int x,int y,const char * fmt,...)
{
    char text[512];
    va_list ap;va_start(ap,fmt);vsnprintf(text,sizeof(text),fmt,ap);va_end(ap);
    assert(x>=0 && y>=0 && x+bmp_string_width(font,text)<=720 && y<480);
    assert(strlen(output)+strlen(text)+2<sizeof(output));
    strcat(output,text);strcat(output,"\n");text_count++;
}
static void bmp_fill(int color,int x,int y,int w,int h)
{
    (void)color;assert(x>=0 && y>=0 && w>0 && h>0 && x+w<=720 && y+h<=480);
}
static void bmp_draw_rect(int color,int x,int y,int w,int h) { bmp_fill(color,x,y,w,h); }
static void draw_line(int x,int y,int xx,int yy,int color)
{
    (void)color;assert(x>=0 && xx<720 && y>=0 && yy<480);
}
static void take_semaphore(int sem,int timeout) { (void)timeout;assert(sem==menu_sem && locks==0);locks++; }
static void give_semaphore(int sem) { if(sem==gui_sem)close_requests++;else{assert(locks==1);locks--;} }
static int is_visible(struct menu_entry * e) { return !e->shidden && !e->hidden && !e->placeholder; }
static void entry_default_display_info(struct menu_entry * e,struct menu_display_info * info)
{
    static char name[35],value[35],help[100],warning[100];
    memset(info,0,sizeof(*info));
    snprintf(name,sizeof(name),"%s",e->name);snprintf(value,sizeof(value),"%s",e->priv?(*(int*)e->priv?"ON":"OFF"):"");
    help[0]=warning[0]=0;
    info->name=name;info->value=value;info->help=help;info->warning=warning;
}
static void menu_entry_select(struct menu * m,int mode)
{
    assert(locks==0);assert(m->selected || IS_SUBMENU(m));actions++;last_mode=mode;
    for(struct menu_entry * e=m->children;e;e=e->next)if(e->selected){last_entry=e;return;}
    assert(!"No selected entry");
}
#include "../firmware/src/photo-menu-600d.h"

static int on=1;
static struct menu_entry wrong={.name="Unrelated",.selected=1};
static struct menu_entry threshold={.name="Threshold",.priv=&on};
static void peak_update(struct menu_entry * e,struct menu_display_info * info)
{
    (void)e;assert(info->can_custom_draw==0);
    snprintf(info->warning,MENU_MAX_WARNING_LEN,"Enable Global Draw first");
}
static struct menu_entry peak={.name="Focus Peak",.priv=&on,.children=&threshold,.update=peak_update};
static struct menu overlay={.name="Overlay",.children=&wrong,.selected=1};
static struct menu prefs={.name="Prefs"};

static void reset(void)
{
    memset(photo_selection,0,sizeof(photo_selection));photo_page_index=0;photo_classic=0;
    submenu_level=edit_mode=menu_help_active=menu_lv_transparent_mode=recording=0;
    actions=last_mode=close_requests=0;last_entry=NULL;locks=0;
    peak.hidden=peak.shidden=peak.placeholder=0;peak.selected=0;
    wrong.next=&peak;wrong.selected=1;overlay.next=&prefs;menus=&overlay;
    overlay.selected=1;prefs.selected=0;output[0]=0;text_count=0;
}
int main(void)
{
    reset();
    photo_menu_key(BGMT_PRESS_LEFT);assert(photo_page_index==5);
    photo_menu_key(BGMT_PRESS_RIGHT);assert(photo_page_index==0);
    photo_menu_key(BGMT_PRESS_UP);assert(photo_selection[0]==6);
    photo_menu_key(BGMT_PRESS_DOWN);assert(photo_selection[0]==0);
    photo_page_index=3;
    for(int i=0;i<7;i++)photo_menu_key(BGMT_PRESS_DOWN);
    assert(photo_selection[3]==7);
    assert(photo_menu_draw()==1);assert(strstr(output,"Page 2/2"));assert(strstr(output,"Global Draw"));
    assert(actions==0 && locks==0);
    puts("PASS navigation wraps and Overlay pagination follows selected item");

    reset();photo_page_index=3;photo_selection[3]=1;
    assert(photo_menu_draw());assert(strstr(output,"Enable Global Draw first"));
    assert(strstr(output,"Threshold"));assert(strstr(output,"ON"));assert(actions==0);
    assert(photo_menu_key(BGMT_PRESS_SET));assert(actions==1 && last_entry==&peak && last_mode==3);
    assert(!wrong.selected && peak.selected);
    assert(photo_menu_key(BGMT_Q));assert(actions==2 && last_entry==&peak && last_mode==2);
    puts("PASS real value preview, preserved warning, exact SET/Q target, no draw-time actions");

    reset();photo_page_index=3;photo_selection[3]=1;
    assert(photo_menu_draw());wrong.next=NULL; /* unloaded between redraw and key */
    assert(photo_menu_key(BGMT_PRESS_SET));assert(actions==0);
    output[0]=0;assert(photo_menu_draw());assert(strstr(output,"Unavailable"));assert(actions==0);
    puts("PASS unloaded module cannot activate a stale selection");

    reset();photo_page_index=3;photo_selection[3]=1;peak.shidden=1;
    photo_menu_key(BGMT_Q);assert(actions==0);
    peak.shidden=0;peak.hidden=1;photo_menu_key(BGMT_PRESS_SET);assert(actions==0);
    puts("PASS hidden and unavailable entries do not execute");

    reset();submenu_level=1;assert(!photo_menu_draw());assert(!photo_menu_key(BGMT_PRESS_DOWN));
    submenu_level=0;edit_mode=1;assert(!photo_menu_draw());assert(!photo_menu_key(BGMT_PRESS_RIGHT));
    edit_mode=0;menu_lv_transparent_mode=1;assert(!photo_menu_draw());
    menu_lv_transparent_mode=0;menu_help_active=1;assert(!photo_menu_draw());
    puts("PASS submenus, editing, Live View preview and help retain original renderer and controls");

    reset();photo_page_index=5;photo_selection[5]=1;
    photo_menu_key(BGMT_PRESS_SET);assert(photo_classic && prefs.selected && actions==0);
    photo_menu_key(BGMT_INFO);assert(!photo_classic && !submenu_level && !edit_mode);
    photo_menu_key(BGMT_MENU);assert(close_requests==1);
    recording=1;assert(!photo_menu_key(BGMT_INFO));
    puts("PASS system menu access, INFO return, MENU close, recording INFO/Q mapping preserved");

    reset();
    struct menu_entry timer={.name="Time Indicator",.priv=&on};
    struct menu_entry tweaks={.name="Movie Tweaks",.children=&timer};
    struct menu movie={.name="Movie",.children=&tweaks};
    struct menu nested={.name="Movie Tweaks",.children=&timer,.icon=ICON_ML_SUBMENU,
        .parent_menu=&movie,.parent_entry=&tweaks};
    prefs.next=&movie;movie.next=&nested;
    photo_page_index=4;photo_selection[4]=0;
    assert(photo_menu_draw());assert(movie.selected && tweaks.selected && timer.selected);
    assert(submenu_level==0); /* preview must not accidentally enter edit mode */
    assert(photo_menu_key(BGMT_PRESS_SET));
    assert(actions==1 && last_entry==&timer && submenu_level==1);
    prefs.next=NULL;
    puts("PASS nested Time Indicator routes through the original Movie Tweaks submenu");

    reset();
    for(unsigned p=0;p<COUNT(photo_pages);p++)for(int i=0;i<photo_pages[p].count;i++)
    {
        photo_page_index=p;photo_selection[p]=i;output[0]=0;
        assert(photo_menu_draw() && locks==0);
    }
    char long_text[200];memset(long_text,'X',sizeof(long_text)-1);long_text[sizeof(long_text)-1]=0;
    photo_text(FONT(FONT_MED,1,0),600,100,100,long_text);
    assert(actions==0);
    puts("PASS all page/item renders and long text stay within framebuffer bounds");
    return 0;
}
