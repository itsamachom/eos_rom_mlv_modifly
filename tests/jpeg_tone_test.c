/* Production engine/UI with camera properties simulated; GPL-2.0-or-later. */
#define main existing_photo_menu_tests
#include "photo_menu_test.c"
#undef main
struct tone_fixture { struct photo_tone_state state; int ready,reads,writes,fail_at,permanent,ignore_at; };
static struct photo_tone_state initial_state(void) {
    struct photo_tone_state s={.active=0x82,.raw_iso=0,.style={{0,3,0,0},{2,4,1,1},{-1,4,2,3}},.wb={0,1,5600,5300,-1,2}};return s;
}
static int fixture_ready(void *ctx) { return ((struct tone_fixture*)ctx)->ready; }
static int fixture_read(void *ctx,struct photo_tone_state *s) {struct tone_fixture *f=ctx;f->reads++;*s=f->state;return 1;}
static int fixture_write(void *ctx,int op,const struct photo_tone_state *s) {
    struct tone_fixture *f=ctx;f->writes++;
    assert(op>=0 && op<=13);
    if(f->ignore_at==f->writes)return 1;
    /* Failure may happen AFTER the camera changed: rollback must cover that too. */
    if(op==13)f->state.raw_iso=s->raw_iso;
    else if(op==0)f->state.active=s->active;
    else if(op<=3)f->state.style[op-1]=s->style[op-1];
    else if(op<=9)f->state.wb[op-4]=s->wb[op-4];
    else {const int ids[]={0x81,0x83,0x86};f->state.active=ids[op-10];}
    return !(f->fail_at && (f->writes==f->fail_at || (f->permanent && f->writes>=f->fail_at)));
}
int main(void) {
    assert(existing_photo_menu_tests()==0);
    for(int i=0;i<PHOTO_TONE_COUNT;i++) {
        struct tone_fixture f={.state=initial_state(),.ready=1};
        struct photo_tone_io io={&f,fixture_ready,fixture_read,fixture_write,NULL};
        struct photo_tone_session session={.active=-1};
        assert(photo_tone_apply(&session,&io,i)==1 && session.active==i && f.writes==9);
        const struct photo_tone_recipe *r=&photo_tone_recipes[i];int slot=photo_tone_style_slot(r->style);
        assert(f.state.raw_iso==r->raw_iso);
        assert(f.state.active==r->style && f.state.style[slot].contrast==r->contrast && f.state.style[slot].sharpness==r->sharpness);
        assert(f.state.wb[0]==9 && f.state.wb[1]==9 && f.state.wb[2]==r->kelvin && f.state.wb[3]==r->kelvin && f.state.wb[4]==r->gm && f.state.wb[5]==r->ba);
        if(r->style==0x86)assert(f.state.style[slot].saturation==2 && f.state.style[slot].color_tone==3);
        assert(photo_tone_restore(&session,&io)==1 && !session.saved);
        struct photo_tone_state before=initial_state();assert(photo_tone_state_equal(&before,&f.state));
    }
    const int original_iso[]={0,72,80,88,104,120,128};
    for(unsigned j=0;j<sizeof(original_iso)/sizeof(original_iso[0]);j++) {
        struct tone_fixture iso={.state=initial_state(),.ready=1};iso.state.raw_iso=original_iso[j];
        struct photo_tone_state original=iso.state;
        struct photo_tone_io iso_io={&iso,fixture_ready,fixture_read,fixture_write,NULL};
        struct photo_tone_session iso_session={.active=-1};
        for(int i=0;i<PHOTO_TONE_COUNT;i++)assert(photo_tone_apply(&iso_session,&iso_io,i)==1);
        assert(photo_tone_restore(&iso_session,&iso_io)==1 && photo_tone_state_equal(&iso.state,&original));
    }
    puts("PASS all 72 original native recipes incl. ISO, both photo/LV WB, exact session restore and monochrome filter/toning preservation");
    for(int fail=1;fail<=9;fail++) {
        struct tone_fixture f={.state=initial_state(),.ready=1,.fail_at=fail};
        struct photo_tone_io io={&f,fixture_ready,fixture_read,fixture_write,NULL};struct photo_tone_session s={.active=-1};
        assert(photo_tone_apply(&s,&io,0)==-1);struct photo_tone_state before=initial_state();assert(photo_tone_state_equal(&before,&f.state));
    }
    struct tone_fixture f={.state=initial_state(),.ready=1,.fail_at=3,.permanent=1};
    struct photo_tone_io io={&f,fixture_ready,fixture_read,fixture_write,NULL};struct photo_tone_session s={.active=-1};
    assert(photo_tone_apply(&s,&io,0)==-2 && s.faulted);int writes=f.writes;
    assert(!photo_tone_apply(&s,&io,1) && f.writes==writes);
    f.fail_at=0;f.permanent=0;assert(photo_tone_restore(&s,&io)==1 && !s.faulted);
    f.ready=0;writes=f.writes;assert(!photo_tone_apply(&s,&io,0) && f.writes==writes);
    f.ready=1;f.writes=0;f.ignore_at=3;assert(photo_tone_apply(&s,&io,0)==-1);
    struct photo_tone_state before=initial_state();assert(photo_tone_state_equal(&before,&f.state));
    puts("PASS each partial-write failure rolls back; ignored acknowledgements are detected; failed recovery blocks new applies until restore");
    reset();tone_host_ready=1;tone_host_state=initial_state();tone_host_write_calls=0;
    photo_tone_session=(struct photo_tone_session){.active=-1};photo_tone_group=0;memset(photo_tone_selected,0,sizeof(photo_tone_selected));
    photo_page_index=0;photo_selection[0]=0;photo_pane=PHOTO_ITEMS;render();
    press(BGMT_PRESS_SET);assert(photo_tone_opened && !tone_host_write_calls);
    press(BGMT_PRESS_RIGHT);press(BGMT_PRESS_DOWN);press(BGMT_PRESS_LEFT);assert(!tone_host_write_calls);
    press(BGMT_PRESS_SET);assert(photo_tone_confirm==1 && !tone_host_write_calls);
    press(BGMT_MENU);assert(photo_tone_opened && !photo_tone_confirm && !tone_host_write_calls);
    press(BGMT_PRESS_SET);press(BGMT_PRESS_SET);assert(photo_tone_session.active>=0 && tone_host_write_calls==9 && !photo_tone_working);
    assert(strstr(output,"Active JPEG tone"));
    tone_host_state.wb[4]++;render();assert(strstr(output,"Settings changed in Canon"));
    press(BGMT_Q);assert(photo_tone_confirm==2);press(BGMT_PRESS_SET);assert(!photo_tone_session.saved);
    assert(photo_tone_state_equal(&before,&tone_host_state));
    photo_tone_working=1;assert(photo_menu_key(BGMT_PRESS_HALFSHUTTER)==1 && photo_tone_opened);
    photo_tone_working=0;assert(photo_menu_key(BGMT_PRESS_HALFSHUTTER)==0 && !photo_tone_opened);
    puts("PASS real picker navigation has no writes; SET requires confirmation; callbacks run outside menu lock; external changes detected; Q restores; half-shutter guarded only while applying");
    photo_thai_attempted=0;photo_tone_message="JPEG / RAW+JPEG in Canon";
    for(int lang=0;lang<=1;lang++) {
        reset();tone_host_ready=1;photo_thai_enabled=lang;photo_tone_opened=1;
        for(int group=0;group<4;group++) {
            photo_tone_group=group;int ids[PHOTO_TONE_COUNT],n=photo_tone_ids(group,ids);
            for(int option=0;option<n;option++) {
                photo_tone_selected[group]=option;photo_tone_confirm=0;photo_tone_working=0;render();assert(!lang || photo_thai_active());
                char name[128];snprintf(name,sizeof(name),"tones-%s-%02d",lang?"th":"en",ids[option]+1);save_proof(name);
            }
        }
    }
    photo_thai_enabled=1;photo_tone_group=0;photo_tone_selected[0]=0;
    for(int step=0;step<9;step++){photo_tone_working=1;photo_tone_step=step;render();char name[40];snprintf(name,sizeof(name),"tone-setting-%d",step);save_proof(name);}
    photo_tone_working=0;puts("PASS all tone/category screens and setting-indicator frames stay inside the real framebuffer in Thai/English");
    return 0;
}
