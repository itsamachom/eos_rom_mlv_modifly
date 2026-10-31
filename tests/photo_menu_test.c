/* Host-side behavioral tests of the production 600D menu front end.
 * Camera I/O and ML editing are stubbed; these tests do not validate hardware.
 */
#include <assert.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <pthread.h>
#include <time.h>
#include <errno.h>
#include <limits.h>
#include "../firmware/src/menu.h"

#define CONFIG_600D 1
#define IS_ML_PTR(p) ((p) != NULL)
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
#define FONT_ID(font) ((font)&255)
#define FONT_FG(font) (((font)>>8)&255)
#define O_RDONLY 0
#define O_SYNC 0
#define FONT(font,fg,bg) ((font)|((fg)<<8)|((bg)<<16))
enum { BGMT_INFO=1, BGMT_PRESS_LEFT, BGMT_WHEEL_LEFT, BGMT_PRESS_RIGHT,
       BGMT_WHEEL_RIGHT, BGMT_PRESS_UP, BGMT_WHEEL_UP, BGMT_PRESS_DOWN,
       BGMT_WHEEL_DOWN, BGMT_MENU, BGMT_PRESS_SET, BGMT_Q, BGMT_PLAY };
static int submenu_level,edit_mode,menu_lv_transparent_mode,menu_help_active;
static int recording,locks,close_requests,actions,last_mode,run_actions;
static int menu_redraw_cancel;
static int exercise_native_reentry;
static int photo_menu_draw(void);
static pthread_mutex_t menu_mutex = PTHREAD_MUTEX_INITIALIZER;
static _Thread_local int owns_menu_lock;
static struct menu * menus;
static struct menu_entry * last_entry;
static const int menu_sem=1,gui_sem=2;
#define SUBMENU_OR_EDIT (submenu_level || edit_mode)
#define RECORDING recording
static int photo_thai_enabled;
static int io_missing,io_corrupt,io_short,thai_pixels;
static unsigned char framebuffer[720*480];
static const char * atlas_path(void) { const char * p=getenv("PHOTO_TEST_ATLAS");assert(p);return p; }
static int FIO_GetFileSize(const char * p,unsigned * size)
{
    (void)p;struct stat st;if(io_missing || stat(atlas_path(),&st))return -1;
    *size=(unsigned)st.st_size;return 0;
}
static void * fio_malloc(unsigned n) { assert(n<=512*1024);return malloc(n); }
static void fio_free(void * p) { free(p); }
static FILE * FIO_OpenFile(const char * p,int flags) { (void)p;(void)flags;return fopen(atlas_path(),"rb"); }
static int FIO_ReadFile(FILE * file,void * data,unsigned n)
{
    int got=fread(data,1,n,file);
    if(io_corrupt && got)((unsigned char*)data)[0]^=1;
    return io_short && got ? got-1 : got;
}
static void FIO_CloseFile(FILE * file) { fclose(file); }
static uint8_t * bmp_vram(void) { return framebuffer; }
static void bmp_putpixel_fast(uint8_t * b,int x,int y,int color)
{
    assert(x>=0 && x<720 && y>=0 && y<480);b[y*720+x]=color;thai_pixels++;
}
static char output[30000];
static int text_count;
static int bmp_string_width(int font,const char * s) { return (int)strlen(s)*((font&255)==FONT_SMALL?8:(font&255)==FONT_MED?12:(font&255)==FONT_MED_LARGE?14:16); }
/* Optional host proofs use the shipped RBF glyphs and production Thai blitter.
 * Camera values below are explicit test fixtures, never hardware readings. */
static void proof_ascii(int font,int x,int y,const char * text)
{
    const char * dir=getenv("PHOTO_PROOF_RBF_DIR");if(!dir)return;
    static unsigned char * rbf[5];
    int id=FONT_ID(font);assert(id>=2 && id<=4);
    if(!rbf[id]) {
        char path[512];snprintf(path,sizeof(path),"%s/argnor%d.rbf",dir,id==2?23:id==3?28:32);
        FILE * f=fopen(path,"rb");assert(f);assert(!fseek(f,0,SEEK_END));long size=ftell(f);rewind(f);
        rbf[id]=malloc(size);assert(rbf[id]);assert(fread(rbf[id],1,size,f)==(size_t)size);fclose(f);
    }
    int h[11];memcpy(h,rbf[id]+72,sizeof(h));
    int stride=h[0]/h[2];
    for(const unsigned char * c=(const unsigned char*)text;*c;c++) {
        assert(*c>=h[4] && *c<=h[5]);
        int w=rbf[id][h[7]+*c-h[4]];
        unsigned char * bits=rbf[id]+h[8]+(*c-h[4])*h[0];
        for(int yy=0;yy<h[2];yy++)for(int xx=0;xx<w;xx++) {
            assert(x+xx>=0 && x+xx<720 && y+yy>=0 && y+yy<480);
            framebuffer[(y+yy)*720+x+xx]=(bits[yy*stride+xx/8] & (1<<(xx%8))) ? FONT_FG(font) : (font>>16)&255;
        }
        x+=w;
    }
}
static void save_proof(const char * name)
{
    const char * dir=getenv("PHOTO_PROOF_OUT");if(!dir)return;
    char path[512];snprintf(path,sizeof(path),"%s/%s.pgm",dir,name);
    FILE * f=fopen(path,"wb");assert(f);fprintf(f,"P5\n720 480\n255\n");
    assert(fwrite(framebuffer,1,sizeof(framebuffer),f)==sizeof(framebuffer));fclose(f);
}
static void bmp_printf(int font,int x,int y,const char * fmt,...)
{
    char text[512];
    va_list ap;va_start(ap,fmt);vsnprintf(text,sizeof(text),fmt,ap);va_end(ap);
    assert(x>=0 && y>=0 && x+bmp_string_width(font,text)<=720 && y<480);
    assert(strlen(output)+strlen(text)+2<sizeof(output));
    strcat(output,text);strcat(output,"\n");text_count++;
    proof_ascii(font,x,y,text);
}
static void bmp_fill(int color,int x,int y,int w,int h)
{
    assert(x>=0 && y>=0 && w>0 && h>0 && x+w<=720 && y+h<=480);
    for(int yy=y;yy<y+h;yy++)memset(framebuffer+yy*720+x,color,w);
}
static void bmp_draw_rect(int color,int x,int y,int w,int h)
{
    bmp_fill(color,x,y,w,1);bmp_fill(color,x,y+h-1,w,1);
    bmp_fill(color,x,y,1,h);bmp_fill(color,x+w-1,y,1,h);
}
static void draw_line(int x,int y,int xx,int yy,int color)
{
    (void)color;assert(x>=0 && xx<720 && y>=0 && yy<480);
}
static void take_semaphore(int sem,int timeout)
{
    (void)timeout;assert(sem==menu_sem && !owns_menu_lock);
    assert(!pthread_mutex_lock(&menu_mutex));assert(locks==0);locks++;owns_menu_lock=1;
}
static void give_semaphore(int sem)
{
    if(sem==gui_sem)close_requests++;
    else { assert(locks==1 && owns_menu_lock);locks--;owns_menu_lock=0;assert(!pthread_mutex_unlock(&menu_mutex)); }
}
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
    if(exercise_native_reentry)
    {
        take_semaphore(menu_sem,0);give_semaphore(menu_sem);
        int before=text_count;menu_redraw_cancel=0;
        assert(photo_menu_draw()==1 && menu_redraw_cancel && text_count==before);
        menu_redraw_cancel=0;
    }
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
static char camera_model[32]="Canon EOS 600D", firmware_version[32]="1.0.2";
static int shutter_count_valid,shutter_count,shutter_count_plus_lv_actuations;
#include "../firmware/src/photo-camera-info-600d.h"
static void observe_snapshot(void);
#define PHOTO_MENU_SNAPSHOT_OBSERVER() observe_snapshot()
#include "../firmware/src/photo-menu-600d.h"

static pthread_mutex_t race_mutex=PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t race_condition=PTHREAD_COND_INITIALIZER;
static pthread_t race_thread;
static int race_enabled,race_attempted,race_done,race_blocked;
static void * category_key_thread(void * unused)
{
    (void)unused;
    assert(!pthread_mutex_lock(&race_mutex));race_attempted=1;
    assert(!pthread_cond_broadcast(&race_condition));assert(!pthread_mutex_unlock(&race_mutex));
    assert(photo_menu_key(BGMT_PRESS_UP));
    assert(!pthread_mutex_lock(&race_mutex));race_done=1;
    assert(!pthread_cond_broadcast(&race_condition));assert(!pthread_mutex_unlock(&race_mutex));
    return NULL;
}
static void observe_snapshot(void)
{
    if(!race_enabled)return;
    race_enabled=0;
    assert(owns_menu_lock && locks==1);
    assert(!pthread_create(&race_thread,NULL,category_key_thread,NULL));
    assert(!pthread_mutex_lock(&race_mutex));
    while(!race_attempted)assert(!pthread_cond_wait(&race_condition,&race_mutex));
    struct timespec deadline;assert(timespec_get(&deadline,TIME_UTC)==TIME_UTC);
    deadline.tv_nsec+=250000000;
    if(deadline.tv_nsec>=1000000000){deadline.tv_sec++;deadline.tv_nsec-=1000000000;}
    int rc=0;
    while(!race_done && rc!=ETIMEDOUT)rc=pthread_cond_timedwait(&race_condition,&race_mutex,&deadline);
    assert(!rc || rc==ETIMEDOUT);
    race_blocked=!race_done;
    assert(!pthread_mutex_unlock(&race_mutex));
    assert(race_blocked && photo_page_index==4 && photo_selection[4]==0);
}

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
    actions=last_mode=close_requests=run_actions=exercise_native_reentry=menu_redraw_cancel=0;
    last_entry=NULL;locks=0;
    on=1;threshold_value=10;
    peak.hidden=peak.shidden=peak.placeholder=0;peak.selected=0;
    threshold.hidden=threshold.shidden=0;threshold.selected=0;threshold.next=&action;
    threshold.parent_menu=action.parent_menu=&options;
    action.selected=action.shidden=action.hidden=0;action.next=NULL;
    wrong.next=&peak;wrong.selected=1;
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
    reset();photo_page_index=4;photo_selection[3]=7;
    race_enabled=1;race_attempted=race_done=race_blocked=0;
    render();assert(!pthread_join(race_thread,NULL));
    assert(race_blocked && photo_page_index==3 && photo_selection[3]==7);
    render();assert(strstr(output,"Page") && strstr(output,"2/2"));
    puts("PASS key task waits for the redraw snapshot lock and uses the correct category bounds");

    reset();photo_page_index=-1;photo_selection[0]=999;photo_detail_index=-10;photo_pane=99;
    render();assert(photo_page_index==0 && photo_selection[0]==0 && photo_detail_index==0 && photo_pane==PHOTO_CATEGORIES);
    photo_page_index=999;assert(photo_menu_key(BGMT_PRESS_DOWN));
    assert(photo_page_index==1);assert(!photo_menu_key(123456));
    reset();go_peak();photo_detail_index=INT_MAX;
    assert(photo_menu_key(BGMT_PRESS_DOWN));assert(photo_detail_index>=0 && photo_detail_index<3);
    puts("PASS invalid category/item/pane indices recover before any array access");

    reset();go_peak();
    int other_value=20;
    struct menu_entry other={.name="Other numeric option",.priv=&other_value,.min=1,.max=50,.parent_menu=&options,.next=&action};
    threshold.next=&other;
    press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);assert(photo_editing);
    threshold.shidden=1;render();assert(!photo_editing && !photo_confirm);
    press(BGMT_PRESS_RIGHT);assert(other_value==20 && actions==0);
    press(BGMT_PRESS_SET);assert(photo_editing);press(BGMT_PRESS_RIGHT);
    assert(other_value==21 && last_entry==&other);
    puts("PASS redraw cancels an armed edit after a hidden row shifts a different value into its slot");

    reset();go_peak();
    struct menu_entry next_action={.name="Different capture action",.icon_type=IT_ACTION,.parent_menu=&options};
    action.next=&next_action;
    press(BGMT_PRESS_DOWN);press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);assert(photo_confirm);
    action.shidden=1;render();assert(!photo_confirm && run_actions==0);
    press(BGMT_PRESS_SET);assert(photo_confirm && run_actions==0);
    press(BGMT_PRESS_SET);assert(run_actions==1 && last_entry==&next_action);
    puts("PASS redraw requires a fresh confirmation after the target action is replaced");

    reset();go_peak();press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);
    struct menu_entry same_name=threshold;same_name.selected=0;
    peak.children=&same_name;options.children=&same_name;render();
    assert(!photo_editing);press(BGMT_PRESS_RIGHT);assert(actions==0 && threshold_value==10);
    peak.children=options.children=&threshold;
    puts("PASS same-name replacement objects cannot inherit the old edit identity");

    reset();go_peak();press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);
    photo_menu_reset();photo_classic=0;photo_pane=PHOTO_ITEMS;photo_page_index=3;photo_selection[3]=1;render();
    assert(!photo_editing && !photo_confirm);
    puts("PASS menu reset clears armed and displayed identities under the shared lock");

    reset();go_peak();press(BGMT_PRESS_DOWN);press(BGMT_PRESS_SET);
    exercise_native_reentry=1;press(BGMT_PRESS_RIGHT);exercise_native_reentry=0;
    assert(threshold_value==11 && last_entry==&threshold && !photo_native_busy && locks==0);
    puts("PASS native callbacks may reenter menu locking while redraw preserves their selected target");

    reset();render();
    press(BGMT_PRESS_UP);assert(photo_page_index==6);
    press(BGMT_PRESS_DOWN);assert(photo_page_index==0);
    press(BGMT_PRESS_DOWN);assert(photo_page_index==1);
    press(BGMT_PRESS_RIGHT);assert(photo_pane==PHOTO_ITEMS && actions==0);
    press(BGMT_PRESS_UP);assert(photo_selection[1]==6);
    assert(strstr(output,"Page") && strstr(output,"2/2"));
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
    assert(actions==0 && !photo_editing);render();assert(strstr(output,"Unavailable"));
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

    reset();photo_page_index=5;photo_selection[5]=2;render();
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
    assert(strstr(output,"Options") && strstr(output,"2/2"));
    puts("PASS detail options paginate at four enlarged two-line rows");

    reset();
    for(unsigned p=0;p<COUNT(photo_pages);p++)for(int i=0;i<photo_pages[p].count;i++)
    for(int pane=PHOTO_CATEGORIES;pane<=PHOTO_DETAILS;pane++)
    {
        photo_page_index=p;photo_selection[p]=i;photo_pane=pane;render();
    }
    assert(actions==0);
    puts("PASS all enlarged-font pages/panes remain inside the framebuffer without running actions");
    reset();photo_thai_enabled=1;
    recording=1;
    assert(!photo_thai_prepare() && !photo_thai_attempted);
    recording=0;
    assert(photo_thai_prepare() && photo_thai_active());
    for(unsigned i=0;i<COUNT(photo_thai_phrases);i++)for(int style=0;style<3;style++)
    {
        int font=FONT(style+2,COLOR_WHITE,COLOR_BLACK);
        const struct photo_thai_mask * m=&photo_thai_phrases[i].masks[style];
        assert(m->offset+m->encoded_size<=PHOTO_TH_BYTES);
        int before=thai_pixels;
        assert(photo_thai_text(font,1,1,m->width,photo_thai_phrases[i].key));
        assert(thai_pixels>before);
    }
    puts("PASS every generated Thai phrase/size decodes and paints bounded pixels");
    reset();photo_thai_enabled=1;go_peak();
    assert(PHOTO_DETAIL_ROWS==3 && thai_pixels>0);
    for(unsigned p=0;p<COUNT(photo_pages);p++)for(int i=0;i<photo_pages[p].count;i++)
    for(int pane=PHOTO_CATEGORIES;pane<=PHOTO_DETAILS;pane++)
    { photo_page_index=p;photo_selection[p]=i;photo_pane=pane;render(); }
    assert(actions==0);
    assert(photo_thai_text(FONT(FONT_LARGE,1,0),10,10,318,"ON,2.0,R"));
    assert(!photo_thai_text(FONT(FONT_LARGE,1,0),10,10,318,"Untranslated original warning"));
    photo_thai_enabled=0;assert(!photo_thai_active());
    puts("PASS Thai layouts, compound numeric values and unchanged English fallback");
    for (int thai=0;thai<=1;thai++)
    {
        reset();photo_thai_enabled=thai;
        struct menu_entry * camera=&photo_camera_info_menu[0];
        struct menu helpmenu={.name="Help",.children=camera};
        options.next=&helpmenu;
        struct menu_entry * model=&camera->children[0], * fw=&camera->children[1];
        model->next=fw;fw->next=NULL;model->parent_menu=fw->parent_menu=&helpmenu;
        photo_page_index=5;photo_selection[5]=6;photo_pane=PHOTO_DETAILS;render();
        assert(strstr(output,"Canon EOS 600D") && strstr(output,"1.0.2") && !strstr(output,"..."));
        if(thai)save_proof("camera-info");
        assert(!photo_can_edit(model) && !photo_can_edit(fw));
        struct menu_display_info info;photo_read_info(model,&info);assert(!strcmp(info.value,"Canon EOS 600D"));
        photo_read_info(fw,&info);assert(!strcmp(info.value,"1.0.2"));
        camera_model[0]=firmware_version[0]=0;
        photo_read_info(model,&info);assert(!strcmp(info.value,"Unavailable"));
        photo_read_info(fw,&info);assert(!strcmp(info.value,"Unavailable"));
        strcpy(camera_model,"Canon EOS 600D");strcpy(firmware_version,"1.0.2");
        struct menu_entry counter={.name="Shutter Count",.children=photo_shutter_details,.select=menu_open_submenu};
        struct menu debugmenu={.name="Debug",.children=&counter};
        options.next=&debugmenu;
        for(int i=0;i<3;i++) { photo_shutter_details[i].parent_menu=&debugmenu;photo_shutter_details[i].next=i<2?&photo_shutter_details[i+1]:NULL; }
        photo_selection[5]=7;photo_detail_index=0;
        shutter_count_valid=0;render();
        for(int i=0;i<3;i++) { photo_read_info(&photo_shutter_details[i],&info);assert(!strcmp(info.value,"Unavailable"));assert(!photo_can_edit(&photo_shutter_details[i])); }
        shutter_count_valid=1;shutter_count=12345;shutter_count_plus_lv_actuations=12445;render();
        if(thai)save_proof("shutter-details-fixture");
        const char * expected[]={"12345","100","12445"};
        for(int i=0;i<3;i++) { photo_read_info(&photo_shutter_details[i],&info);assert(!strcmp(info.value,expected[i])); }
        assert(!strstr(output,"..."));
        camera->children[0].next=NULL;options.next=NULL;
    }
    puts("PASS production camera model/firmware rows fit uncut and remain read-only in Thai and English");
    puts("PASS three production shutter detail rows distinguish unavailable, mechanical, Live View and combined values");
    reset();photo_page_index=6;photo_pane=PHOTO_ITEMS;render();
    assert(!strcmp(photo_pages[6].name,"Games"));press(BGMT_PRESS_RIGHT);press(BGMT_PRESS_SET);
    save_proof("games");
    assert(actions==0 && !photo_editing && !photo_confirm);
    reset();photo_thai_enabled=1;photo_page_index=0;photo_selection[0]=1;photo_pane=PHOTO_ITEMS;render();save_proof("shoot");
    puts("PASS separate Games category stays unavailable until its actual game modules register");
    reset();photo_page_index=6;photo_pane=PHOTO_ITEMS;
    struct menu_entry game_start={.name="Arkanoid",.icon_type=IT_ACTION,.select=NULL};
    struct menu game_menu={.name="Games",.children=&game_start};
    game_start.parent_menu=&game_menu;options.next=&game_menu;
    render();press(BGMT_PRESS_RIGHT);press(BGMT_PRESS_SET);
    assert(photo_confirm && run_actions==0);
    press(BGMT_PRESS_SET);assert(run_actions==1 && last_entry==&game_start && last_mode==3);
    puts("PASS loaded Arkanoid reaches its real root action only after two SET confirmations");
    reset();photo_thai_enabled=0;photo_page_index=6;photo_selection[6]=1;photo_pane=PHOTO_ITEMS;
    render();assert(strstr(output,"Load lua; reboot."));
    struct menu_entry run_game={.name="Run Script",.icon_type=IT_ACTION};
    struct menu_entry script={.name="Pong Game",.icon_type=IT_ACTION,.select=menu_open_submenu,.priv=&on,.children=&run_game};
    struct menu script_menu={.name="Scripts",.children=&script};
    struct menu script_submenu={.name="Pong Game",.children=&run_game,.icon=ICON_ML_SUBMENU,.parent_menu=&script_menu,.parent_entry=&script};
    script_menu.next=&script_submenu;options.next=&script_menu;
    script.parent_menu=&script_menu;run_game.parent_menu=&script_submenu;
    render();press(BGMT_PRESS_RIGHT);
    assert(!strcmp(photo_display_target,"Run Script"));
    press(BGMT_PRESS_SET);assert(photo_confirm && run_actions==0);
    press(BGMT_PRESS_SET);assert(run_actions==1 && last_entry==&run_game && last_mode==3);
    puts("PASS Lua game containers lead directly to Run Script and never execute or enable Autorun automatically");

    reset();photo_thai_enabled=1;
    struct menu_entry language={.name="Photo UI Language",.priv=&photo_thai_enabled,.max=1,.icon_type=IT_DICE};
    prefs.children=&language;
    photo_page_index=5;photo_pane=PHOTO_ITEMS;render();
    press(BGMT_PRESS_RIGHT);press(BGMT_PRESS_SET);press(BGMT_PRESS_RIGHT);
    assert(photo_thai_enabled==0 && !photo_thai_active() && PHOTO_DETAIL_ROWS==4);
    press(BGMT_PRESS_SET);press(BGMT_PRESS_SET);press(BGMT_PRESS_RIGHT);
    assert(photo_thai_enabled==1 && photo_thai_active() && PHOTO_DETAIL_ROWS==3 && run_actions==0);
    prefs.children=NULL;
    puts("PASS language switch edits the real setting without changing shooting controls");
    for(int kind=0;kind<3;kind++)
    {
        fio_free(photo_thai_atlas);photo_thai_atlas=NULL;photo_thai_attempted=0;photo_thai_enabled=1;
        io_missing=kind==0;io_corrupt=kind==1;io_short=kind==2;
        assert(!photo_thai_prepare() && !photo_thai_active());
        assert(!photo_thai_text(FONT(FONT_LARGE,1,0),10,10,318,"Focus Peak"));
        render();assert(strstr(output,"Thai font missing"));
    }
    io_missing=io_corrupt=io_short=0;photo_thai_enabled=0;
    puts("PASS missing, corrupted and short Thai resources safely retain English");
    return 0;
}
