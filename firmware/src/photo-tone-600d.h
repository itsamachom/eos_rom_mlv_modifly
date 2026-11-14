/* Independent native JPEG picker. GPL-2.0-or-later.
 * Recipe values credited in photo-tone-recipes-600d.h; graphics/UI written for this fork.
 * Included after photo_text; all UI state is protected by menu_sem. */
#include "photo-tone-engine.h"
#include "photo-film-labels-600d.h"
static int photo_tone_opened,photo_tone_group,photo_tone_selected[4],photo_tone_confirm;
static int photo_tone_working,photo_tone_step,photo_tone_steps;
static const char *photo_tone_message="JPEG / RAW+JPEG in Canon";
static struct photo_tone_session photo_tone_session={.active=-1};
static char photo_tone_read_detail[96];
#ifndef PHOTO_TONE_TEST_ADAPTER
static volatile int photo_tone_wb[6],photo_tone_wb_seen,photo_tone_iso_seen;
PROP_HANDLER(PROP_ISO) { (void)buf;if(len==4)photo_tone_iso_seen=1; }
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
    #ifdef FEATURE_EXPO_OVERRIDE
    if(CONTROL_BV)return 0; /* Native recipes must not drive an ML exposure override. */
    #endif
    return !RECORDING && !is_movie_mode() && shooting_mode>=0 && shooting_mode<=3 &&
        job_state_ready_to_take_pic() && (jpeg==2 || jpeg==3);
}
static int photo_tone_platform_read(void *ctx,struct photo_tone_state *state) {
    (void)ctx;
    memset(state,0,sizeof(*state));
    state->active=lens_info.raw_picstyle;state->raw_iso=lens_info.raw_iso;
    unsigned styles=0;
    const int ids[]={0x81,0x83,0x86};
    for(int i=0;i<3;i++) {
        if(photo_jpeg_style_read(ids[i],&state->style[i]))styles|=1<<i;
        else state->style[i].sharpness=-10;
    }
    for(int i=0;i<6;i++)state->wb[i]=photo_tone_wb[i];
    snprintf(photo_tone_read_detail,sizeof(photo_tone_read_detail),"WB %02X PS %X M%d/%d K%d/%d ISO %d:%d",photo_tone_wb_seen,styles,state->wb[0],state->wb[1],state->wb[2],state->wb[3],photo_tone_iso_seen,state->raw_iso);
    /* Modes and shifts must be observed. Unused Kelvin and unrelated styles need not be. */
    if((photo_tone_wb_seen & 0x33)!=0x33 || !photo_tone_iso_seen)return 0;
    if(state->raw_iso && (state->raw_iso<72 || state->raw_iso>128))return 0;
    if(!((state->active>=0x81 && state->active<=0x87) || (state->active>=0x21 && state->active<=0x23)))return 0;
    return state->wb[0]>=0 && state->wb[0]<=9 && state->wb[1]>=0 && state->wb[1]<=9 &&
        (state->wb[0]!=9 || ((photo_tone_wb_seen & 4) && photo_tone_kelvin_known(state->wb[2]))) &&
        (state->wb[1]!=9 || ((photo_tone_wb_seen & 8) && photo_tone_kelvin_known(state->wb[3]))) &&
        state->wb[4]>=-9 && state->wb[4]<=9 && state->wb[5]>=-9 && state->wb[5]<=9;
}
static int photo_tone_platform_write(void *ctx,int op,const struct photo_tone_state *state) {
    (void)ctx;
    if(op==13) {
        int value=state->raw_iso;
        prop_request_change_wait(PROP_ISO,&value,4,350);
        return lens_info.raw_iso==value;
    }
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
/* Small integer ellipse: rounded metal caps without textures or large allocations. */
static void photo_tone_ellipse(int cx,int cy,int rx,int ry,int color) {
    for(int y=-ry;y<=ry;y++) {
        int x=rx;
        while(x>0 && x*x*ry*ry+y*y*rx*rx>rx*rx*ry*ry)x--;
        bmp_fill(color,cx-x,cy+y,2*x+1,1);
    }
}
/* Original compact lettering for miniature labels and 90-degree side names. */
static const char photo_film_letters[]="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+./ &";
static const unsigned char photo_film_glyphs[][7]={
    {14,17,17,31,17,17,17}, /* A */
    {30,17,17,30,17,17,30}, /* B */
    {15,16,16,16,16,16,15}, /* C */
    {30,17,17,17,17,17,30}, /* D */
    {31,16,16,30,16,16,31}, /* E */
    {31,16,16,30,16,16,16}, /* F */
    {15,16,16,23,17,17,15}, /* G */
    {17,17,17,31,17,17,17}, /* H */
    {31,4,4,4,4,4,31}, /* I */
    {7,2,2,2,18,18,12}, /* J */
    {17,18,20,24,20,18,17}, /* K */
    {16,16,16,16,16,16,31}, /* L */
    {17,27,21,21,17,17,17}, /* M */
    {17,25,25,21,19,19,17}, /* N */
    {14,17,17,17,17,17,14}, /* O */
    {30,17,17,30,16,16,16}, /* P */
    {14,17,17,17,21,18,13}, /* Q */
    {30,17,17,30,20,18,17}, /* R */
    {15,16,16,14,1,1,30}, /* S */
    {31,4,4,4,4,4,4}, /* T */
    {17,17,17,17,17,17,14}, /* U */
    {17,17,17,17,17,10,4}, /* V */
    {17,17,17,21,21,27,17}, /* W */
    {17,17,10,4,10,17,17}, /* X */
    {17,17,10,4,4,4,4}, /* Y */
    {31,1,2,4,8,16,31}, /* Z */
    {14,17,19,21,25,17,14}, /* 0 */
    {4,12,4,4,4,4,14}, /* 1 */
    {14,17,1,2,4,8,31}, /* 2 */
    {30,1,1,14,1,1,30}, /* 3 */
    {2,6,10,18,31,2,2}, /* 4 */
    {31,16,16,30,1,1,30}, /* 5 */
    {14,16,16,30,17,17,14}, /* 6 */
    {31,1,2,4,8,8,8}, /* 7 */
    {14,17,17,14,17,17,14}, /* 8 */
    {14,17,17,15,1,1,14}, /* 9 */
    {0,0,0,31,0,0,0}, /* - */
    {0,4,4,31,4,4,0}, /* + */
    {0,0,0,0,0,6,6}, /* . */
    {1,1,2,4,8,16,16}, /* / */
    {0,0,0,0,0,0,0}, /*   */
    {12,18,20,8,21,18,13}, /* & */
};
static void photo_film_text(int x,int y,const char *text,int scale,int vertical,int color,int max_chars) {
    for(int i=0;text[i] && i<max_chars;i++) {
        char c=text[i];if(c>='a' && c<='z')c-=32;
        const char *p=strchr(photo_film_letters,c);if(!p)continue;
        const unsigned char *glyph=photo_film_glyphs[p-photo_film_letters];
        for(int row=0;row<7;row++)for(int col=0;col<5;col++)if(glyph[row] & (16>>col)) {
            int px=vertical?6-row:i*6+col,py=vertical?i*6+col:row;
            bmp_fill(color,x+px*scale,y+py*scale,scale,scale);
        }
    }
}
static void photo_film_center(int x,int y,int width,const char *text,int scale,int color) {
    int n=strlen(text),max=(width+scale)/(6*scale);if(n>max)n=max;
    photo_film_text(x+(width-(n*6-1)*scale)/2,y,text,scale,0,color,n);
}
static void photo_tone_canister_flat(int x,int index,int selected) {
    const struct photo_tone_recipe *r=&photo_tone_recipes[index];
    const struct photo_film_label *l=&photo_film_labels[index];
    int frame=selected?COLOR_ORANGE:COLOR_GRAY(18);
    bmp_fill(COLOR_GRAY(3),x,102,212,238);bmp_draw_rect(frame,x,102,212,238);
    photo_text(FONT(FONT_MED_LARGE,selected?COLOR_ORANGE:COLOR_WHITE,COLOR_GRAY(3)),x+8,108,196,r->name);
    /* Tall 35mm cartridge: 92px body / 158px height, rounded rims and spool.
     * Stock-specific labels are small GPL-derived data; all geometry/lettering
     * here is independent. No SD reads, bitmap allocation or palette mutation. */
    photo_tone_ellipse(x+105,329,61,5,COLOR_GRAY(1));
    /* Curved perforated leader behind the body. */
    for(int i=0;i<52;i++) {
        int bend=i*i/230;
        bmp_fill(COLOR_GRAY(r->group==3?25:31),x+145+i,184+bend,1,94);
        if(i%12<6){bmp_fill(COLOR_GRAY(3),x+145+i,190+bend,1,7);bmp_fill(COLOR_GRAY(3),x+145+i,264+bend,1,7);}
    }
    bmp_fill(COLOR_BLACK,x+143,178,6,131);
    photo_tone_ellipse(x+100,317,48,9,COLOR_GRAY(40));
    for(int i=0;i<92;i++) {
        int light=i<28?17+i*60/28:77-(i-28)*64/64;
        bmp_fill(COLOR_GRAY(light),x+54+i,166,1,150);
    }
    bmp_fill(l->bg,x+57,175,86,134);
    if(l->pattern==0) {
        bmp_fill(l->band,x+57,201,86,32);bmp_fill(l->accent,x+57,278,86,3);
    }else if(l->pattern==1) {
        bmp_fill(l->band,x+57,175,86,21);bmp_fill(l->accent,x+57,196,86,3);
        bmp_fill(l->band,x+57,278,86,7);
    }else {
        bmp_fill(l->accent,x+57,178,86,3);
        for(int i=0;i<86;i++)for(int j=0;j<2;j++)bmp_fill(l->accent,x+57+i,280+j*6-i/14,1,2);
    }
    int word_color=l->text;
    if(l->pattern==0 && (l->band==COLOR_YELLOW || l->band==COLOR_WHITE) && word_color==COLOR_WHITE)word_color=COLOR_BLACK;
    photo_film_center(x+68,211,62,l->word,1,word_color);
    int num_scale=strlen(l->number)>3?2:3;
    photo_film_center(x+68,243,62,l->number,num_scale,l->num);
    const char *sub=l->sub;
    if(streq(sub,"PROFESSIONAL"))sub="PRO";
    if(streq(sub,"COLOR PRINT"))sub="PRINT";
    if(streq(sub,"SUPER PRESTO"))sub="PRESTO";
    photo_film_center(x+68,288,62,sub,1,l->num);
    photo_film_center(x+68,301,62,r->process,1,l->num);
    /* Side names identify every selected preset, not only its broad category. */
    photo_film_text(x+58,183,r->brand,1,1,l->num,20);
    photo_film_text(x+134,183,r->name,1,1,l->num,20);
    /* Steel edge highlight and crimped black caps remain outside the label. */
    bmp_fill(COLOR_GRAY(86),x+54,172,2,135);bmp_fill(COLOR_GRAY(25),x+144,172,2,135);
    photo_tone_ellipse(x+100,313,47,5,COLOR_BLACK);
    photo_tone_ellipse(x+100,316,47,5,COLOR_GRAY(35));
    photo_tone_ellipse(x+100,163,49,8,COLOR_BLACK);
    photo_tone_ellipse(x+99,160,46,6,COLOR_GRAY(48));
    photo_tone_ellipse(x+100,159,40,4,COLOR_BLACK);
    bmp_fill(COLOR_BLACK,x+87,145,26,14);
    photo_tone_ellipse(x+100,145,13,4,COLOR_GRAY(35));
    photo_tone_ellipse(x+100,144,9,2,COLOR_BLACK);
    if(photo_tone_working && selected) {
        int pos=photo_tone_step%4;
        bmp_draw_rect(COLOR_WHITE,x+91,154,18,11);
        bmp_fill(COLOR_CYAN,x+93+(pos&1)*7,156+(pos>>1)*4,5,3);
    }
}

#include "photo-film-cylinder-600d.h"
/* One bounded, reusable ~19KiB label buffer. Low memory retains the flat renderer. */
static unsigned char *photo_film_texture;
static int photo_film_texture_attempted;
static int photo_film_shade(int color,int light,int spec,int x,int y) {
    static const unsigned char bayer[16]={0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5};
    int q=bayer[(y&3)*4+(x&3)]*16+8;
    int lo=COLOR_GRAY(0),hi=COLOR_GRAY(100);
    if(color==COLOR_BLACK || color==COLOR_WHITE || (color>=lo && color<=hi)) {
        int lum=color==COLOR_BLACK?0:color==COLOR_WHITE?255:(color-lo)*255/(hi-lo);
        lum=(lum*light+spec*(255-lum))/255;if(lum>255)lum=255;
        return COLOR_GRAY(lum*100/255);
    }
    if(spec>q)return COLOR_GRAY(65+spec*35/255);
    if(light>225 || light>q)return color;
    if(light>100) {
        if(color==COLOR_RED)return COLOR_DARK_RED;
        if(color==COLOR_GREEN1)return COLOR_GREEN2;
        if(color==COLOR_YELLOW)return COLOR_ORANGE;
    }
    return COLOR_GRAY(3);
}
static void photo_film_caps(int x) {
    for(int i=0;i<98;i++) {
        int h=photo_film_cap_height[i],v=photo_film_columns[i*92/98].metal;
        for(int y=-h;y<=h;y++)bmp_fill(COLOR_GRAY(y==-h || y==h?85:v),x+51+i,162+y,1,1);
        int b=h*5/7;
        for(int y=-b;y<=b;y++)bmp_fill(COLOR_GRAY(y==-b?75:v*2/3),x+51+i,316+y,1,1);
    }
    photo_tone_ellipse(x+100,160,41,4,COLOR_GRAY(7));
    for(int i=0;i<26;i++)bmp_fill(COLOR_GRAY(5+photo_film_columns[i*92/26].metal/3),x+87+i,145,1,15);
    photo_tone_ellipse(x+100,145,13,4,COLOR_GRAY(42));
    photo_tone_ellipse(x+100,144,10,2,COLOR_BLACK);
}
static void photo_tone_canister(int x,int index,int selected) {
    photo_tone_canister_flat(x,index,selected);
    if(!photo_film_texture_attempted) {
        photo_film_texture_attempted=1;
        photo_film_texture=fio_malloc(144*134);
    }
    if(!photo_film_texture)return;
    const struct photo_tone_recipe *r=&photo_tone_recipes[index];
    const struct photo_film_label *l=&photo_film_labels[index];
    /* Paint a wider label with the shipped RBF letterforms, then wrap it.
     * This temporary plane is erased before the projected cylinder is shown. */
    bmp_fill(l->bg,x+28,175,144,134);
    if(l->pattern==0) {
        bmp_fill(l->band,x+28,197,144,32);bmp_fill(l->accent,x+28,278,144,3);
    }else if(l->pattern==1) {
        bmp_fill(l->band,x+28,175,144,21);bmp_fill(l->accent,x+28,196,144,3);
        bmp_fill(l->band,x+28,278,144,7);
    }else {
        bmp_fill(l->accent,x+28,178,144,3);
        for(int i=0;i<144;i++)for(int j=0;j<2;j++)bmp_fill(l->accent,x+28+i,280+j*6-i/22,1,2);
    }
    int ink=l->text;
    if(l->pattern==0 && (l->band==COLOR_YELLOW || l->band==COLOR_WHITE) && ink==COLOR_WHITE)ink=COLOR_BLACK;
    int fw=bmp_string_width(FONT(FONT_MED,ink,l->bg),l->word);
    bmp_printf(FONT(FONT_MED,ink,l->pattern==0?l->band:l->bg),x+100-fw/2,201,"%s",l->word);
    fw=bmp_string_width(FONT(FONT_LARGE,l->num,l->bg),l->number);
    bmp_printf(FONT(FONT_LARGE,l->num,l->bg),x+100-fw/2,235,"%s",l->number);
    const char *sub=l->sub;
    if(streq(sub,"PROFESSIONAL"))sub="PRO";
    if(streq(sub,"COLOR PRINT"))sub="PRINT";
    if(streq(sub,"SUPER PRESTO"))sub="PRESTO";
    photo_film_center(x+40,270,120,sub,1,l->num);
    photo_film_center(x+40,298,120,r->process,1,l->num);
    photo_film_text(x+32,181,r->brand,1,1,l->num,20);
    photo_film_text(x+161,181,r->name,1,1,l->num,20);
    unsigned char *vram=bmp_vram();
    for(int y=0;y<134;y++)memcpy(photo_film_texture+y*144,vram+(175+y)*BMPPITCH+x+28,144);
    photo_tone_canister_flat(x,index,selected);
    /* Angle-dependent texture projection, curved bands, smooth gray lighting,
     * and ordered dithering for the existing fixed-color camera palette. */
    for(int i=0;i<92;i++) {
        const struct photo_film_column *c=&photo_film_columns[i];
        for(int y=0;y<134;y++) {
            int px=x+54+i,py=175+y+c->dy;
            int color=photo_film_texture[y*144+c->u];
            bmp_putpixel_fast(vram,px,py,photo_film_shade(color,c->light,c->spec,px,py));
        }
    }
    for(int i=0;i<52;i++)for(int y=0;y<94;y++) {
        if(i%12<6 && ((y>=6 && y<13) || (y>=80 && y<87)))continue;
        int px=x+145+i,py=184+i*i/230+y;
        int sheen=28-((y-28)<0?28-y:y-28);if(sheen<0)sheen=0;
        int color=r->group==3?COLOR_GRAY(35):COLOR_ORANGE;
        bmp_putpixel_fast(vram,px,py,photo_film_shade(color,70+i, sheen,px,py));
    }
    photo_film_caps(x);
    if(photo_tone_working && selected) {
        int k=photo_tone_step%4;
        bmp_draw_rect(COLOR_WHITE,x+91,154,18,11);
        bmp_fill(COLOR_CYAN,x+93+(k&1)*7,156+(k>>1)*4,5,3);
    }
}
static int photo_tone_matches(const struct photo_tone_recipe *r) {
    struct photo_tone_state actual;int slot=photo_tone_style_slot(r->style);
    return photo_tone_platform_read(NULL,&actual) && actual.active==r->style && actual.raw_iso==r->raw_iso &&
        actual.style[slot].contrast==r->contrast && actual.style[slot].sharpness==r->sharpness &&
        (r->style==0x86 || (actual.style[slot].saturation==r->saturation && actual.style[slot].color_tone==r->color_tone)) &&
        actual.wb[0]==9 && actual.wb[1]==9 && actual.wb[2]==r->kelvin && actual.wb[3]==r->kelvin && actual.wb[4]==r->gm && actual.wb[5]==r->ba;
}

static int photo_tone_draw(void) {
    photo_thai_prepare();
    bmp_fill(COLOR_BLACK,0,0,720,480);bmp_fill(COLOR_GRAY(5),0,0,720,48);
    photo_text(FONT(FONT_LARGE,COLOR_WHITE,COLOR_GRAY(5)),16,2,570,"FLIM TONE");
    for(int g=0;g<4;g++) {
        int bg=g==photo_tone_group?COLOR_BLUE:COLOR_BLACK;
        int x=8+g*158,width=g==3?230:150;
        bmp_fill(bg,x,54,width,40);
        photo_text(FONT(FONT_MED,g==photo_tone_group?COLOR_WHITE:COLOR_CYAN,bg),x+6,60,width-12,photo_tone_groups[g]);
    }
    int ids[PHOTO_TONE_COUNT],n=photo_tone_ids(photo_tone_group,ids),selected=photo_tone_selected[photo_tone_group];
    int first=selected/3*3;
    for(int i=0;i<3 && first+i<n;i++)photo_tone_canister(24+i*234,ids[first+i],first+i==selected);
    const struct photo_tone_recipe *r=&photo_tone_recipes[photo_tone_current()];
    bmp_printf(FONT(FONT_MED,COLOR_WHITE,COLOR_BLACK),16,350,"%d/%d ISO%d K%d",selected+1,n,r->effective_iso,r->kelvin);
    bmp_printf(FONT(FONT_MED,COLOR_WHITE,COLOR_BLACK),16,376,"GM%+d BA%+d",r->gm,r->ba);
    const char *message=photo_tone_working?"Setting tone - please wait":photo_tone_confirm==1?"Apply tone? SET confirms":photo_tone_confirm==2?"Restore session settings? SET":photo_tone_message;
    const struct photo_tone_recipe *badge=r;
    int active=0;
    if(!photo_tone_working && photo_tone_session.active>=0) {
        const struct photo_tone_recipe *current=&photo_tone_recipes[photo_tone_session.active];
        if(photo_tone_matches(current)){badge=current;active=1;}
        else if(streq(message,"Tone ready - take a JPEG"))message="Settings changed in Canon";
    }
    photo_text(FONT(FONT_MED_LARGE,COLOR_CYAN,COLOR_BLACK),16,403,392,message);
    int bg=COLOR_GRAY(7),border=active?COLOR_CYAN:COLOR_ORANGE;
    bmp_fill(bg,420,363,288,72);bmp_draw_rect(border,420,363,288,72);
    bmp_draw_rect(COLOR_GRAY(28),422,365,284,68);
    photo_text(FONT(FONT_MED,active?COLOR_CYAN:COLOR_WHITE,bg),430,366,268,active?"Active JPEG tone":"FLIM TONE");
    int f=bmp_string_width(FONT(FONT_LARGE,COLOR_WHITE,bg),badge->name)<=268?FONT_LARGE:FONT_MED_LARGE;
    int name_width=bmp_string_width(FONT(f,COLOR_WHITE,bg),badge->name);
    photo_text(FONT(f,COLOR_WHITE,bg),430+(268-name_width)/2,394,name_width,badge->name);
    if(!photo_tone_working && !photo_tone_confirm && streq(photo_tone_message,"Settings not ready - retry")) {
        char first[33];snprintf(first,sizeof(first),"%.32s",photo_tone_read_detail);
        bmp_fill(COLOR_BLACK,16,347,392,54);
        photo_text(FONT(FONT_MED,COLOR_WHITE,COLOR_BLACK),16,350,392,first);
        photo_text(FONT(FONT_MED,COLOR_WHITE,COLOR_BLACK),16,376,392,strlen(photo_tone_read_detail)>32?photo_tone_read_detail+32:"");
    }
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
        int action=photo_tone_confirm;photo_tone_confirm=0;photo_tone_working=1;photo_tone_step=0;photo_tone_steps=9;return action;
    }
    return 0;
}
