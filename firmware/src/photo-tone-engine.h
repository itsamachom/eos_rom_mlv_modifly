/* Native JPEG tone transaction engine, GPL-2.0-or-later.
 * Portable: hardware I/O is supplied by an adapter; no image conversion or file I/O. */
#ifndef PHOTO_TONE_ENGINE_H
#define PHOTO_TONE_ENGINE_H
#include <string.h>
#include "photo-tone-recipes-600d.h"
#include "photo-tone-types.h"
struct photo_tone_state { int active; struct photo_jpeg_style style[3]; int wb[6]; };
/* WB order: photo mode, LV mode, photo Kelvin, LV Kelvin, GM, BA.
 * Write operations: 0 active style, 1..3 native style data, 4..9 WB fields, 10..12 select native style for restore. */
struct photo_tone_io {
    void *ctx;
    int (*ready)(void *);
    int (*read)(void *,struct photo_tone_state *);
    int (*write)(void *,int,const struct photo_tone_state *);
    void (*progress)(void *,int,int);
};
struct photo_tone_session { struct photo_tone_state original; int saved, active, faulted; };
static int photo_tone_style_slot(int id) { return id==0x81?0:id==0x83?1:id==0x86?2:-1; }
static int photo_tone_state_equal(const struct photo_tone_state *a,const struct photo_tone_state *b) {
    return a->active==b->active && !memcmp(a->style,b->style,sizeof(a->style)) && !memcmp(a->wb,b->wb,sizeof(a->wb));
}
static int photo_tone_write_sequence(const struct photo_tone_io *io,const struct photo_tone_state *s,const int *ops,int n) {
    for(int i=0;i<n;i++) {
        if(io->progress)io->progress(io->ctx,i,n);
        if(!io->ready(io->ctx) || !io->write(io->ctx,ops[i],s))return 0;
    }
    if(io->progress)io->progress(io->ctx,n,n);
    struct photo_tone_state actual;
    return io->read(io->ctx,&actual) && photo_tone_state_equal(&actual,s);
}
static int photo_tone_restore_state(const struct photo_tone_io *io,const struct photo_tone_state *state) {
    static const int ops[]={10,1,11,2,12,3,6,7,8,9,4,5,0};
    return photo_tone_write_sequence(io,state,ops,13);
}
/* 1 success, 0 not ready/no writes, -1 rolled back, -2 recovery required. */
static int photo_tone_apply(struct photo_tone_session *session,const struct photo_tone_io *io,int index) {
    struct photo_tone_state before,wanted;
    if(index<0 || index>=PHOTO_TONE_COUNT || session->faulted || !io->ready(io->ctx) || !io->read(io->ctx,&before))return 0;
    if(!session->saved){session->original=before;session->saved=1;session->active=-1;}
    wanted=before;
    const struct photo_tone_recipe *r=&photo_tone_recipes[index];int slot=photo_tone_style_slot(r->style);
    if(slot<0)return 0;
    wanted.active=r->style;
    wanted.style[slot].contrast=r->contrast;wanted.style[slot].sharpness=r->sharpness;
    /* Monochrome's other two fields are filter/toning: keep the owner's values. */
    if(r->style!=0x86){wanted.style[slot].saturation=r->saturation;wanted.style[slot].color_tone=r->color_tone;}
    wanted.wb[0]=wanted.wb[1]=9;wanted.wb[2]=wanted.wb[3]=r->kelvin;wanted.wb[4]=r->gm;wanted.wb[5]=r->ba;
    int ops[]={0,slot+1,6,7,8,9,4,5};
    if(photo_tone_write_sequence(io,&wanted,ops,8)){session->active=index;return 1;}
    if(photo_tone_restore_state(io,&before))return -1;
    session->faulted=1;session->active=-1;return -2;
}
static int photo_tone_restore(struct photo_tone_session *session,const struct photo_tone_io *io) {
    if(!session->saved || !io->ready(io->ctx))return 0;
    if(!photo_tone_restore_state(io,&session->original)){session->faulted=1;session->active=-1;return -2;}
    session->saved=0;session->faulted=0;session->active=-1;return 1;
}
#endif
