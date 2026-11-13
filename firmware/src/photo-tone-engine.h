/* Native JPEG tone transaction engine, GPL-2.0-or-later.
 * Portable: hardware I/O is supplied by an adapter; no image conversion or file I/O. */
#ifndef PHOTO_TONE_ENGINE_H
#define PHOTO_TONE_ENGINE_H
#include <string.h>
#include "photo-tone-recipes-600d.h"
#include "photo-tone-types.h"
struct photo_tone_state { int active, raw_iso; struct photo_jpeg_style style[3]; int wb[6]; };
/* WB order: photo mode, LV mode, photo Kelvin, LV Kelvin, GM, BA.
 * Write operations: 0 active style, 1..3 native style data, 4..9 WB fields, 10..12 select native style for restore, 13 ISO (original upstream conversion). */
struct photo_tone_io {
    void *ctx;
    int (*ready)(void *);
    int (*read)(void *,struct photo_tone_state *);
    int (*write)(void *,int,const struct photo_tone_state *);
    void (*progress)(void *,int,int);
};
struct photo_tone_session { struct photo_tone_state original; int saved, active, faulted; };
static int photo_tone_style_slot(int id) { return id==0x81?0:id==0x83?1:id==0x86?2:-1; }
static int photo_tone_style_known(const struct photo_jpeg_style *s) { return s->sharpness>=0 && s->sharpness<=7; }
static int photo_tone_kelvin_known(int k) { return k>=1500 && k<=15000; }
static int photo_tone_state_equal(const struct photo_tone_state *a,const struct photo_tone_state *b) {
    if(a->active!=b->active || a->raw_iso!=b->raw_iso)return 0;
    for(int i=0;i<3;i++)if(photo_tone_style_known(&b->style[i]) && memcmp(&a->style[i],&b->style[i],sizeof(a->style[i])))return 0;
    for(int i=0;i<6;i++) {
        /* A dormant Kelvin slot may be absent/zero under AWB. Never invent its value. */
        if((i==2 || i==3) && !photo_tone_kelvin_known(b->wb[i]) && b->wb[i-2]!=9)continue;
        if(a->wb[i]!=b->wb[i])return 0;
    }
    return 1;
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
    int ops[14],n=0;
    for(int i=0;i<3;i++)if(photo_tone_style_known(&state->style[i])){ops[n++]=10+i;ops[n++]=1+i;}
    if(photo_tone_kelvin_known(state->wb[2]))ops[n++]=6;
    if(photo_tone_kelvin_known(state->wb[3]))ops[n++]=7;
    ops[n++]=8;ops[n++]=9;ops[n++]=4;ops[n++]=5;ops[n++]=13;ops[n++]=0;
    return photo_tone_write_sequence(io,state,ops,n);
}
/* 1 success, 0 not ready/no writes, -1 rolled back, -2 recovery required. */
static int photo_tone_apply(struct photo_tone_session *session,const struct photo_tone_io *io,int index) {
    struct photo_tone_state before,wanted;
    if(index<0 || index>=PHOTO_TONE_COUNT || session->faulted || !io->ready(io->ctx) || !io->read(io->ctx,&before))return 0;
    const struct photo_tone_recipe *r=&photo_tone_recipes[index];int slot=photo_tone_style_slot(r->style);
    if(slot<0 || !photo_tone_style_known(&before.style[slot]))return 0;
    if(!session->saved){session->original=before;session->saved=1;session->active=-1;}
    /* Back up a newly observed target before its first mutation in this session. */
    if(!photo_tone_style_known(&session->original.style[slot]))session->original.style[slot]=before.style[slot];
    wanted=before;
    wanted.active=r->style;wanted.raw_iso=r->raw_iso;
    wanted.style[slot].contrast=r->contrast;wanted.style[slot].sharpness=r->sharpness;
    /* Monochrome's other two fields are filter/toning: keep the owner's values. */
    if(r->style!=0x86){wanted.style[slot].saturation=r->saturation;wanted.style[slot].color_tone=r->color_tone;}
    wanted.wb[0]=wanted.wb[1]=9;wanted.wb[2]=wanted.wb[3]=r->kelvin;wanted.wb[4]=r->gm;wanted.wb[5]=r->ba;
    int ops[]={0,slot+1,4,5,6,7,8,9,13};
    if(photo_tone_write_sequence(io,&wanted,ops,9)){session->active=index;return 1;}
    if(photo_tone_restore_state(io,&before))return -1;
    session->faulted=1;session->active=-1;return -2;
}
static int photo_tone_restore(struct photo_tone_session *session,const struct photo_tone_io *io) {
    if(!session->saved || !io->ready(io->ctx))return 0;
    if(!photo_tone_restore_state(io,&session->original)){session->faulted=1;session->active=-1;return -2;}
    session->saved=0;session->faulted=0;session->active=-1;return 1;
}
#endif
