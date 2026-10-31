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
#define IS_ML_PTR(p) ((p) != NULL)
#define COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define MOD(a,b) ((((int)(a)%(int)(b))+(int)(b))%(int)(b))
#define streq(a,b) (!strcmp(a,b))
#define ICON_ML_SUBMENU 100
#define FONT_BG(f) (((f)>>16)&255)
#define FONT_FG(f) (((f)>>8)&255)
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
static int recording,locks,close_requests,actions,last_mode,run_actions;
static struct menu * menus;
static struct menu_entry * last_entry;
static const int menu_sem=1,gui_sem=2;
#define SUBMENU_OR_EDIT (submenu_level || edit_mode)
#define RECORDING recording
static char output[30000];
static int text_count;
static int bmp_string_width(int font,const char * s) { return (int)strlen(s)*((font&255)==FONT_SMALL?8:(font&255)==FONT_MED?12:(font&255)==FONT_MED_LARGE?14:16); }
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
void menu_open_submenu(void * priv, int delta) { (void)priv; (void)delta; submenu_level++; }
static void menu_entry_select(struct menu * m,int mode)
{
    assert(locks==0);assert(m->selected || IS_SUBMENU(m));actions++;last_mode=mode;
    for(struct menu_entry * e=m->children;e;e=e->next)if(e->selected)
    {
        last_entry=e;
        if(mode==0 || mode==1)
        {
            if(e->select)e->select(e->priv, mode==0?1:-1);
            else if(e->priv)*(int*)e->priv=MOD(*(int*)e->priv-e->min+(mode==0?1:-1),e->max-e->min+1)+e->min;
        }
        if(mode==3 && e->icon_type==IT_ACTION)run_actions++;
        if((mode==3 && e->select==menu_open_submenu) || (mode==2 && e->children))submenu_level++;
        return;
    }
    assert(!"No selected entry");
}
#include "../firmware/src/photo-menu-600d.h"

static int on=1,threshold_value=10;
static struct menu_entry wrong={.name="Unrelated",.selected=1};
static struct menu_entry action={.name="Run focus stack",.icon_type=IT_ACTION};
static struct menu_entry threshold={.name="Threshold",.priv=&threshold_value,.min=1,.max=50};
static void peak_update(struct menu_entry * e,struct menu_display_info * info)
{
    (void)e;assert(info->can_custom_draw==0);
    snprintf(info->warning,MENU_MAX_WARNING_LEN,"Enable Global Draw first");
}
static struct menu_entry peak={.name="Focus Peak",.priv=&on,.max=1,.icon_type=IT_BOOL,
    .children=&threshold,.update=peak_update};
static struct menu overlay={.name="Overlay",.children=&wrong,.selected=1};
static struct menu options={.name="Focus Peak",.children=&threshold,.icon=ICON_ML_SUBMENU,
    .parent_menu=&overlay,.parent_entry=&peak};
static struct menu prefs={.name="Prefs"};

static void reset(void)
{
    memset(photo_selection,0,sizeof(photo_selection));photo_page_index=0;photo_menu_reset();
    submenu_level=edit_mode=menu_help_active=menu_lv_transparent_mode=recording=0;
    actions=last_mode=close_requests=run_actions=0;last_entry=NULL;locks=0;
    on=1;threshold_value=10;
    peak.hidden=peak.shidden=peak.placeholder=0;peak.selected=0;
    threshold.hidden=threshold.shidden=0;threshold.selected=0;threshold.next=&action;
    threshold.parent_menu=action.parent_menu=&options;
    action.selected=0;wrong.next=&peak;wrong.selected=1;
    overlay.next=&prefs;prefs.next=&options;options.next=NULL;menus=&overlay;
    overlay.selected=1;prefs.selected=0;output[0]=0;text_count=0;
}
static void render(void) { output[0]=0;assert(photo_menu_draw());assert(locks==0); }
static void press(int key) { assert(photo_menu_key(key));if(photo_home_active())render(); }
static void go_peak(void)
{
    photo_page_index=3;photo_selection[3]=1;photo_pane=PHOTO_ITEMS;render();
    press(BGMT_PRESS_RIGHT);assert(photo_pane==PHOTO_DETAILS);
}
int main(void)
{
    reset();render();
    press(BGMT_PRESS_UP);assert(photo_page_index==5);
    press(BGMT_PRESS_DOWN);assert(photo_page_index==0);
    press(BGMT_PRESS_DOWN);assert(photo_page_index==1);
    press(BGMT_PRESS_RIGHT);assert(photo_pane==PHOTO_ITEMS && actions==0);
    press(BGMT_PRESS_UP);assert(photo_selection[1]==6);
    assert(strstr(output,"Page 2/2"));
    press(BGMT_PRESS_DOWN);assert(photo_selection[1]==0);
    press(BGMT_PRESS_LEFT);assert(photo_pane==PHOTO_CATEGORIES && photo_page_index==1);
    puts("PASS vertical category/item navigation and horizontal pane focus without setting changes");

    reset();go_peak();
    assert(strstr(output,"Enable Global Draw first") && strstr(output,"Threshold"));
    assert(actions==0);press(BGMT_PRESS_SET);assert(photo_editing && actions==0);
    press(BGMT_PRESS_LEFT);assert(on==0 && actions==1 && last_mode==1 && last_entry==&peak);
    press(BGMT_PRESS_RIGHT);assert(on==1 && actions==2 && last_mode==0);
    press(BGMT_PRESS_SET);assert(!photo_editing && photo_pane==PHOTO_DETAILS);
    press(BGMT_PRESS_LEFT);assert(photo_pane==PHOTO_ITEMS && on==1 && actions==2);
    puts("PASS inline status editing, SET finish and Left back have separate states");

    reset();go_peak();press(BGMT_PRESS_DOWN);assert(photo_detail_index==1);
    press(BGMT_PRESS_SET);assert(photo_editing && actions==0);
    press(BGMT_PRESS_RIGHT);assert(threshold_value==11 && last_entry==&threshold && last_mode==0);
    assert(submenu_level==0);press(BGMT_WHEEL_DOWN);assert(threshold_value==12);
    press(BGMT_MENU);assert(!photo_editing && close_requests==0 && threshold_value==12);
    assert(photo_pane==PHOTO_DETAILS);press(BGMT_PRESS_LEFT);assert(photo_pane==PHOTO_ITEMS && actions==2);
    puts("PASS child values edit through original submenu ownership and stay inside Photo UI");

    reset();go_peak();press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);
    threshold.shidden=1; /* slot now resolves to an action instead of the shown numeric setting */
    assert(photo_menu_key(BGMT_PRESS_RIGHT));assert(actions==0 && run_actions==0 && !photo_editing);
    puts("PASS dynamically hidden or shifted options never execute a different stale target");

    reset();go_peak();wrong.next=NULL;assert(photo_menu_key(BGMT_PRESS_SET));
    assert(actions==0 && !photo_editing);render();assert(photo_display_target[0]==0);
    puts("PASS unloaded modules cannot activate stale settings");

    reset();go_peak();press(BGMT_PRESS_DOWN);press(BGMT_PRESS_DOWN);
    press(BGMT_PRESS_SET);assert(photo_confirm && actions==0);
    press(BGMT_MENU);assert(!photo_confirm && run_actions==0 && close_requests==0);
    press(BGMT_PRESS_SET);assert(photo_confirm);press(BGMT_PRESS_SET);
    assert(run_actions==1 && last_entry==&action && !photo_confirm);
    puts("PASS action rows require confirmation and MENU cancels without running");

    reset();go_peak();press(BGMT_Q);assert(last_mode==2 && submenu_level==1);
    assert(!photo_menu_draw() && !photo_menu_key(BGMT_PRESS_DOWN));
    assert(photo_menu_key(BGMT_INFO));assert(!photo_classic && submenu_level==0);
    assert(photo_menu_key(BGMT_INFO));assert(photo_classic);
    assert(photo_menu_key(BGMT_INFO));assert(!photo_classic);
    puts("PASS Q keeps original advanced editors and INFO returns to Photo UI");

    reset();photo_page_index=5;photo_selection[5]=1;render();
    press(BGMT_PRESS_RIGHT);assert(photo_pane==PHOTO_ITEMS);
    press(BGMT_PRESS_SET);assert(photo_classic && prefs.selected && actions==0);
    press(BGMT_INFO);assert(!photo_classic);press(BGMT_MENU);assert(close_requests==1);
    reset();recording=1;render();press(BGMT_INFO);assert(photo_pane==PHOTO_ITEMS && actions==0);
    puts("PASS system menus, MENU close and recording INFO/Q navigation");

    reset();
    struct menu_entry timer={.name="Time Indicator",.priv=&on,.max=3};
    struct menu_entry tweaks={.name="Movie Tweaks",.children=&timer};
    struct menu movie={.name="Movie",.children=&tweaks};
    struct menu nested={.name="Movie Tweaks",.children=&timer,.icon=ICON_ML_SUBMENU,
        .parent_menu=&movie,.parent_entry=&tweaks};
    options.next=&movie;movie.next=&nested;timer.parent_menu=&nested;
    photo_page_index=4;photo_selection[4]=1;photo_pane=PHOTO_ITEMS;render();
    press(BGMT_PRESS_RIGHT);press(BGMT_PRESS_SET);press(BGMT_PRESS_RIGHT);
    assert(actions==1 && last_entry==&timer && submenu_level==0);
    options.next=NULL;
    puts("PASS nested Time Indicator changes inline without leaving a native submenu active");

    reset();submenu_level=1;assert(!photo_menu_draw());assert(!photo_menu_key(BGMT_PRESS_DOWN));
    submenu_level=0;edit_mode=1;assert(!photo_menu_draw());assert(!photo_menu_key(BGMT_PRESS_RIGHT));
    edit_mode=0;menu_lv_transparent_mode=1;assert(!photo_menu_draw());
    menu_lv_transparent_mode=0;menu_help_active=1;assert(!photo_menu_draw());
    puts("PASS original native editors retain their renderer and controls");

    reset();
    struct menu_entry more[6];memset(more,0,sizeof(more));
    for(int i=0;i<6;i++){more[i].name="Long option label for clipping";more[i].priv=&threshold_value;
        more[i].max=50;more[i].parent_menu=&options;if(i<5)more[i].next=&more[i+1];}
    threshold.next=more;
    go_peak();for(int i=0;i<5;i++)press(BGMT_PRESS_DOWN);
    assert(strstr(output,"Opts 2/2"));
    puts("PASS detail options paginate at four enlarged two-line rows");

    reset();
    for(unsigned p=0;p<COUNT(photo_pages);p++)for(int i=0;i<photo_pages[p].count;i++)
    for(int pane=PHOTO_CATEGORIES;pane<=PHOTO_DETAILS;pane++)
    {
        photo_page_index=p;photo_selection[p]=i;photo_pane=pane;render();
    }
    assert(actions==0);
    puts("PASS all enlarged-font pages/panes remain inside the framebuffer without running actions");
    return 0;
}
