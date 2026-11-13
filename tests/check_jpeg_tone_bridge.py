"""Compile the actual Canon adapter functions against a property-delivery fixture."""
from pathlib import Path
import os,re,subprocess,tempfile
root=Path(__file__).resolve().parents[1]
style=(root/'firmware/src/picstyle.c').read_text()
a=style.index('int photo_jpeg_style_read(');b=style.index('\n#endif',a)
style_functions=style[a:b]
ui=(root/'firmware/src/photo-tone-600d.h').read_text()
adapter=re.search(r'#ifndef PHOTO_TONE_TEST_ADAPTER\n(.*?)\n#endif',ui,re.S)[1]
prelude=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "photo-tone-engine.h"
#define NUM_PICSTYLES 10
struct picstyle_settings_prop_struct {int32_t contrast;uint32_t sharpness;int32_t saturation,color_tone;uint32_t a,b;};
static struct picstyle_settings_prop_struct picstyle_settings[NUM_PICSTYLES];
static unsigned picstyle_settings_prop_sizes[NUM_PICSTYLES];
static int get_prop_picstyle_index(int id){return id==0x81?1:id==0x83?3:id==0x86?6:0;}
static unsigned get_picstyle_prop_ID(int i){return 100+i;}
static int requests,accept_writes=1,recording,movie,job_ready=1,shooting_mode,control_bv;
#define FEATURE_EXPO_OVERRIDE 1
#define CONTROL_BV control_bv
static char photo_tone_read_detail[96];
static int pic_quality=3<<24;
struct {int raw_picstyle,raw_iso;} lens_info;
#define RECORDING recording
static int is_movie_mode(void){return movie;}
static int job_state_ready_to_take_pic(void){return job_ready;}
enum {PROP_ISO=19,PROP_PICTURE_STYLE=20,PROP_WB_MODE_PH=1,PROP_WB_MODE_LV,PROP_WB_KELVIN_PH,PROP_WB_KELVIN_LV,PROP_WBS_GM,PROP_WBS_BA};
#define PROP_HANDLER(name) static void handler_##name(void *buf,unsigned len)
static int prop_request_change_wait(unsigned prop,const void *data,size_t len,int timeout);
'''
postlude=r'''
static int prop_request_change_wait(unsigned prop,const void *data,size_t len,int timeout){
 assert(timeout==350);requests++;
 if(!accept_writes)return 0;
 if(prop>=100 && prop<110){assert(len==24);memcpy(&picstyle_settings[prop-100],data,len);return 1;}
 assert(len==4);int value=*(const int*)data;
 if(prop==PROP_WB_KELVIN_PH || prop==PROP_WB_KELVIN_LV)assert(value>=1500 && value<=15000);
 switch(prop){
 case PROP_ISO:assert(value==0 || (value>=72 && value<=128));lens_info.raw_iso=value;handler_PROP_ISO(&value,4);break;
 case PROP_PICTURE_STYLE:lens_info.raw_picstyle=value;break;
 case PROP_WB_MODE_PH:handler_PROP_WB_MODE_PH(&value,4);break;
 case PROP_WB_MODE_LV:handler_PROP_WB_MODE_LV(&value,4);break;
 case PROP_WB_KELVIN_PH:handler_PROP_WB_KELVIN_PH(&value,4);break;
 case PROP_WB_KELVIN_LV:handler_PROP_WB_KELVIN_LV(&value,4);break;
 case PROP_WBS_GM:handler_PROP_WBS_GM(&value,4);break;
 case PROP_WBS_BA:handler_PROP_WBS_BA(&value,4);break;
 default:assert(!"Property outside the native tone whitelist");
 }return 1;
}
int main(void){
 (void)photo_tone_groups;
 for(int i=0;i<NUM_PICSTYLES;i++){picstyle_settings[i]=(struct picstyle_settings_prop_struct){0,3,0,0,0x12345678,0x87654321};picstyle_settings_prop_sizes[i]=24;}
 struct photo_jpeg_style wanted={-2,2,2,1},out;
 assert(photo_jpeg_style_write(0x81,&wanted));assert(photo_jpeg_style_read(0x81,&out));assert(!memcmp(&out,&wanted,sizeof(out)));
 assert(picstyle_settings[1].a==0x12345678 && picstyle_settings[1].b==0x87654321);
 int calls=requests;picstyle_settings_prop_sizes[1]=0;assert(!photo_jpeg_style_write(0x81,&wanted));assert(requests==calls);picstyle_settings_prop_sizes[1]=24;
 wanted.contrast=5;assert(!photo_jpeg_style_write(0x81,&wanted));assert(requests==calls);wanted.contrast=1;
 accept_writes=0;assert(!photo_jpeg_style_write(0x81,&wanted));assert(picstyle_settings[1].contrast==-2);accept_writes=1;
 assert(!photo_jpeg_style_read(0x21,&out));
 lens_info.raw_picstyle=0x82;
 int zero=0,k=5500,negative_byte=255;handler_PROP_ISO(&zero,4);
 handler_PROP_WB_MODE_PH(&zero,4);handler_PROP_WB_MODE_LV(&zero,4);
 handler_PROP_WB_KELVIN_PH(&k,4);handler_PROP_WB_KELVIN_LV(&k,4);
 handler_PROP_WBS_GM(&negative_byte,4);handler_PROP_WBS_BA(&zero,4);
 assert(photo_tone_wb[4]==-1);
 struct photo_tone_io io={NULL,photo_tone_platform_ready,photo_tone_platform_read,photo_tone_platform_write,NULL};
 struct photo_tone_state original;assert(io.read(NULL,&original));
 for(int i=0;i<PHOTO_TONE_COUNT;i++){
  struct photo_tone_session s={.active=-1};assert(photo_tone_apply(&s,&io,i)==1);assert(photo_tone_restore(&s,&io)==1);
  struct photo_tone_state restored;assert(io.read(NULL,&restored));assert(photo_tone_state_equal(&original,&restored));
  assert(picstyle_settings[1].a==0x12345678 && picstyle_settings[3].b==0x87654321);
 }
 /* Reproduce 600D startup under AWB: no inactive Kelvin payloads and only
  * the target Standard style observed; unrelated style metadata is absent. */
 photo_tone_wb_seen=0;handler_PROP_WB_MODE_PH(&zero,4);handler_PROP_WB_MODE_LV(&zero,4);
 handler_PROP_WBS_GM(&zero,4);handler_PROP_WBS_BA(&zero,4);
 photo_tone_wb[2]=photo_tone_wb[3]=0;
 picstyle_settings_prop_sizes[3]=picstyle_settings_prop_sizes[6]=0;
 struct photo_tone_session awb_session={.active=-1};
 assert(io.read(NULL,&original));assert(original.wb[2]==0 && original.style[1].sharpness==-10);
 assert(photo_tone_apply(&awb_session,&io,0)==1);
 assert(photo_tone_restore(&awb_session,&io)==1); /* No write of the unknown 0 K slot. */
 assert(photo_tone_wb[0]==0 && photo_tone_wb[1]==0);
 /* A genuinely unknown target still refuses to write. */
 calls=requests;struct photo_tone_session unknown={.active=-1};assert(!photo_tone_apply(&unknown,&io,5));assert(requests==calls);
 /* Monochrome filter/toning are opaque values, not RGB saturation sliders. */
 picstyle_settings_prop_sizes[6]=24;picstyle_settings[6].saturation=0x12340000;picstyle_settings[6].color_tone=0x56780000;
 struct photo_tone_session mono={.active=-1};assert(photo_tone_apply(&mono,&io,6)==1);assert(photo_tone_restore(&mono,&io)==1);
 assert(picstyle_settings[6].saturation==0x12340000 && picstyle_settings[6].color_tone==0x56780000);
 picstyle_settings_prop_sizes[3]=24;
 calls=requests;struct photo_tone_session s={.active=-1};
 pic_quality=4<<24;assert(!photo_tone_apply(&s,&io,0));pic_quality=3<<24;
 recording=1;assert(!photo_tone_apply(&s,&io,0));recording=0;
 movie=1;assert(!photo_tone_apply(&s,&io,0));movie=0;
 job_ready=0;assert(!photo_tone_apply(&s,&io,0));job_ready=1;
 shooting_mode=9;assert(!photo_tone_apply(&s,&io,0));shooting_mode=0;
 assert(requests==calls);
 control_bv=1;assert(!photo_tone_apply(&s,&io,0));control_bv=0;assert(requests==calls);
 photo_tone_iso_seen=0;assert(!photo_tone_apply(&s,&io,0));assert(requests==calls);handler_PROP_ISO(&zero,4);
 photo_tone_wb_seen=0;assert(!photo_tone_apply(&s,&io,0));assert(requests==calls);
 puts("PASS production Canon adapter: 72 original recipes/ISO/restore, exact property lengths, untouched reserved bytes, signed WB shift, ignored writes, no writes in RAW-only/recording/movie/busy/Auto modes or before metadata arrives");
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='jpeg-tone-bridge-') as tmp:
 p=Path(tmp);(p/'test.c').write_text(prelude+style_functions+'\n'+adapter+'\n'+postlude)
 subprocess.run(['gcc','-std=c11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(root/'firmware/src'),str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True,env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0'))
