/* Independent native JPEG picker. GPL-2.0-or-later.
 * Recipe values credited in photo-tone-recipes-600d.h; graphics/UI written for this fork.
 * Included after photo_text; all UI state is protected by menu_sem. */
#include "photo-tone-engine.h"
static int photo_tone_opened,photo_tone_group,photo_tone_selected[4],photo_tone_confirm;
static int photo_tone_working,photo_tone_step,photo_tone_steps;
static const char *photo_tone_message="JPEG / RAW+JPEG in Canon";
static struct photo_tone_session photo_tone_session={.active=-1};
#ifndef PHOTO_TONE_TEST_ADAPTER
static volatile int photo_tone_wb[6],photo_tone_wb_seen;
#define TONE_WB_HANDLER(prop,index) \
    PROP_HANDLER(prop) { if(len==4){photo_tone_wb[index]=index>=4?*(int8_t*)buf:*(int*)buf;photo_tone_wb_seen|=1<<(index);} }
TONE_WB_HANDLER(PROP_WB_MODE_PH,0)
TONE_WB_HANDLER(PROP_WB_MODE_LV,1)
TONE_WB_HANDLER(PROP_WB_KELVIN_PH,2)
TONE_WB_HANDLER(PROP_WB_KELVIN_LV,3)
TONE_WB_HANDLER(PROP_WBS_GM,4)
TONE_WB_HANDLER(PROP_WBS_BA,5)
#undef TONE_WB_HANDLER
static int photo_tone_platform_ready(void *ctx) {
    (void)ctx;
    unsigned jpeg=(unsigned)pic_quality>>24;
    return !RECORDING && !is_movie_mode() && shooting_mode>=0 && shooting_mode<=3 &&
        job_state_ready_to_take_pic() && (jpeg==2 || jpeg==3);
}
static int photo_tone_platform_read(void *ctx,struct photo_tone_state *state) {
    (void)ctx;
    if(photo_tone_wb_seen!=63)return 0;
    state->active=lens_info.raw_picstyle;
    if(!((state->active>=0x81 && state->active<=0x87) || (state->active>=0x21 && state->active<=0x23)))return 0;
    const int ids[]={0x81,0x83,0x86};
    for(int i=0;i<3;i++)if(!photo_jpeg_style_read(ids[i],&state->style[i]))return 0;
    for(int i=0;i<6;i++)state->wb[i]=photo_tone_wb[i];
    return state->wb[0]>=0 && state->wb[0]<=9 && state->wb[1]>=0 && state->wb[1]<=9 &&
        state->wb[2]>=2500 && state->wb[2]<=10000 && state->wb[3]>=2500 && state->wb[3]<=10000 &&
        state->wb[4]>=-9 && state->wb[4]<=9 && state->wb[5]>=-9 && state->wb[5]<=9;
}
static int photo_tone_platform_write(void *ctx,int op,const struct photo_tone_state *state) {
    (void)ctx;
    if(op==0 || (op>=10 && op<=12)) {
        const int ids[]={0x81,0x83,0x86};
        int value=op==0?state->active:ids[op-10];
        prop_request_change_wait(PROP_PICTURE_STYLE,&value,4,350);
        return lens_info.raw_picstyle==value;
    }
    if(op>=1 && op<=3) {
        const int ids[]={0x81,0x83,0x86};
        return photo_jpeg_style_write(ids[op-1],&state->style[op-1]);
    }
    if(op>=4 && op<=9) {
        const unsigned props[]={PROP_WB_MODE_PH,PROP_WB_MODE_LV,PROP_WB_KELVIN_PH,PROP_WB_KELVIN_LV,PROP_WBS_GM,PROP_WBS_BA};
        int value=state->wb[op-4];
        prop_request_change_wait(props[op-4],&value,4,350);
        return photo_tone_wb[op-4]==value;
    }
    return 0;
}
#endif
static int photo_tone_ids(int group,int out[PHOTO_TONE_COUNT]) {
    int n=0;for(int i=0;i<PHOTO_TONE_COUNT;i++)if(photo_tone_recipes[i].group==group)out[n++]=i;return n;
}
static int photo_tone_current(void) {
    int ids[PHOTO_TONE_COUNT],n=photo_tone_ids(photo_tone_group,ids);
    photo_tone_selected[photo_tone_group]=MOD(photo_tone_selected[photo_tone_group],n);
    return ids[photo_tone_selected[photo_tone_group]];
}
static void photo_tone_progress(void *ctx,int step,int total) {
    (void)ctx;take_semaphore(menu_sem,0);
    photo_tone_step=step;photo_tone_steps=total;
    give_semaphore(menu_sem);menu_redraw();
}
static const struct photo_tone_io photo_tone_io={NULL,photo_tone_platform_ready,photo_tone_platform_read,photo_tone_platform_write,photo_tone_progress};
static void photo_tone_perform(int action) {
    /* Property callbacks may acquire other locks; never execute with menu_sem held. */
    take_semaphore(menu_sem,0);
    struct photo_tone_session local=photo_tone_session;int index=photo_tone_current();
    give_semaphore(menu_sem);
    int result=action==1?photo_tone_apply(&local,&photo_tone_io,index):photo_tone_restore(&local,&photo_tone_io);
    take_semaphore(menu_sem,0);
    photo_tone_session=local;photo_tone_working=0;photo_tone_confirm=0;
    photo_tone_message=result==1?(action==1?"Tone ready - take a JPEG":"Original settings restored"):
        result==-1?"Failed - changes rolled back":result==-2?"Recovery needed - Q Restore":photo_tone_platform_ready(NULL)?"Settings not ready - retry":"Use P/Tv/Av/M and enable JPEG";
    give_semaphore(menu_sem);menu_redraw();
}
static void photo_tone_canister(int x,int index,int selected) {
    const struct photo_tone_recipe *r=&photo_tone_recipes[index];
    int frame=selected?COLOR_ORANGE:COLOR_GRAY(12);
    bmp_fill(COLOR_GRAY(3),x,102,212,238);bmp_draw_rect(frame,x,102,212,238);
    photo_text(FONT(FONT_MED_LARGE,selected?COLOR_ORANGE:COLOR_WHITE,COLOR_GRAY(3)),x+8,108,196,r->name);
    /* Steel caps, shaded cylinder, label band, light trap and perforated leader. */
    bmp_fill(COLOR_GRAY(32),x+28,154,140,16);bmp_fill(COLOR_GRAY(12),x+22,166,152,138);
    for(int i=0;i<6;i++)bmp_fill(COLOR_GRAY(6+i*4),x+26+i*24,170,24,130);
    bmp_fill(COLOR_GRAY(35),x+28,304,140,10);bmp_fill(COLOR_BLACK,x+174,184,6,114);
    bmp_fill(COLOR_GRAY(19),x+180,202,24,91);
    for(int y=208;y<289;y+=14){bmp_fill(COLOR_BLACK,x+182,y,4,6);bmp_fill(COLOR_BLACK,x+198,y,4,6);}
    int band=r->group==3?COLOR_GRAY(22):r->group==1?COLOR_BLUE:r->group==2?COLOR_GRAY(10):COLOR_ORANGE;
    int ink=r->group==0?COLOR_BLACK:COLOR_WHITE;
    bmp_fill(band,x+26,210,144,62);
    photo_text(FONT(FONT_MED,ink,band),x+32,213,132,"THAI-MENU");
    bmp_printf(FONT(FONT_MED,ink,band),x+32,244,"JPEG %02d",index+1);
    if(photo_tone_working && selected) {
        /* A winding indicator advances on acknowledged settings, not a fake timer. */
        int pos=photo_tone_step%4;
        bmp_draw_rect(COLOR_WHITE,x+84,170,24,24);
        bmp_fill(COLOR_CYAN,x+86+(pos&1)*11,172+(pos>>1)*11,9,9);
    }
}
static int photo_tone_draw(void) {
    photo_thai_prepare();
    bmp_fill(COLOR_BLACK,0,0,720,480);bmp_fill(COLOR_GRAY(5),0,0,720,48);
    photo_text(FONT(FONT_LARGE,COLOR_WHITE,COLOR_GRAY(5)),16,2,570,"JPEG Tones");
    for(int g=0;g<4;g++) {
        int bg=g==photo_tone_group?COLOR_BLUE:COLOR_BLACK;
        bmp_fill(bg,8+g*178,54,170,40);
        photo_text(FONT(FONT_MED,g==photo_tone_group?COLOR_WHITE:COLOR_CYAN,bg),14+g*178,60,158,photo_tone_groups[g]);
    }
    int ids[PHOTO_TONE_COUNT],n=photo_tone_ids(photo_tone_group,ids),selected=photo_tone_selected[photo_tone_group];
    int first=selected/3*3;
    for(int i=0;i<3 && first+i<n;i++)photo_tone_canister(24+i*234,ids[first+i],first+i==selected);
    const struct photo_tone_recipe *r=&photo_tone_recipes[photo_tone_current()];
    bmp_printf(FONT(FONT_MED,COLOR_WHITE,COLOR_BLACK),16,350,"%d/%d   K%d   C%d S%d Sat%d Tone%d",selected+1,n,r->kelvin,r->contrast,r->sharpness,r->saturation,r->color_tone);
    const char *message=photo_tone_working?"Setting tone - please wait":photo_tone_confirm==1?"Apply tone? SET confirms":photo_tone_confirm==2?"Restore session settings? SET":photo_tone_message;
    if(!photo_tone_working && !photo_tone_confirm && photo_tone_session.active>=0 && streq(photo_tone_message,"Tone ready - take a JPEG")) {
        struct photo_tone_state actual;
        const struct photo_tone_recipe *active=&photo_tone_recipes[photo_tone_session.active];
        int slot=photo_tone_style_slot(active->style);
        int matches=photo_tone_platform_read(NULL,&actual) && actual.active==active->style &&
            actual.style[slot].contrast==active->contrast && actual.style[slot].sharpness==active->sharpness &&
            (active->style==0x86 || (actual.style[slot].saturation==active->saturation && actual.style[slot].color_tone==active->color_tone)) &&
            actual.wb[0]==9 && actual.wb[1]==9 && actual.wb[2]==active->kelvin && actual.wb[3]==active->kelvin && actual.wb[4]==active->gm && actual.wb[5]==active->ba;
        if(matches){
            photo_text(FONT(FONT_MED_LARGE,COLOR_CYAN,COLOR_BLACK),16,390,250,"Active JPEG tone");
            photo_text(FONT(FONT_MED_LARGE,COLOR_WHITE,COLOR_BLACK),280,390,424,active->name);
        }else photo_text(FONT(FONT_MED_LARGE,COLOR_CYAN,COLOR_BLACK),16,390,688,"Settings changed in Canon");
    }else photo_text(FONT(FONT_MED_LARGE,COLOR_CYAN,COLOR_BLACK),16,390,688,message);
    photo_text(FONT(FONT_MED,COLOR_CYAN,COLOR_BLACK),16,442,688,"L/R Tone  U/D Group  SET Apply  Q Restore  MENU Back");
    return 1;
}
/* Called with menu_sem held. Returns a pending action, dispatched outside it. */
static int photo_tone_key(int key) {
    if(photo_tone_working)return 0;
    if(key==BGMT_MENU){if(photo_tone_confirm)photo_tone_confirm=0;else photo_tone_opened=0;return 0;}
    if(key==BGMT_PRESS_LEFT || key==BGMT_WHEEL_LEFT || key==BGMT_PRESS_RIGHT || key==BGMT_WHEEL_RIGHT) {
        int ids[PHOTO_TONE_COUNT],n=photo_tone_ids(photo_tone_group,ids);
        int d=key==BGMT_PRESS_LEFT || key==BGMT_WHEEL_LEFT?-1:1;
        photo_tone_selected[photo_tone_group]=MOD(photo_tone_selected[photo_tone_group]+d,n);photo_tone_confirm=0;return 0;
    }
    if(key==BGMT_PRESS_UP || key==BGMT_WHEEL_UP || key==BGMT_PRESS_DOWN || key==BGMT_WHEEL_DOWN) {
        photo_tone_group=MOD(photo_tone_group+(key==BGMT_PRESS_UP || key==BGMT_WHEEL_UP?-1:1),4);photo_tone_confirm=0;return 0;
    }
    if(key==BGMT_Q){photo_tone_confirm=photo_tone_session.saved?2:0;photo_tone_message="No session backup";return 0;}
    if(key==BGMT_PRESS_SET) {
        if(!photo_tone_confirm){photo_tone_confirm=1;return 0;}
        int action=photo_tone_confirm;photo_tone_confirm=0;photo_tone_working=1;photo_tone_step=0;photo_tone_steps=8;return action;
    }
    return 0;
}
