import base64,subprocess,sys,os
src=open('src.html',encoding='utf8').read()
chars=''.join(sorted(set(src)))+''.join(chr(c) for c in range(32,127))
open('chars.txt','w',encoding='utf8').write(chars)
F='fonts/'
def sub(path,out):
    subprocess.run(['pyftsubset',path,'--text-file=chars.txt','--flavor=woff2','--output-file='+out,'--layout-features=*'],check=True)
    return base64.b64encode(open(out,'rb').read()).decode()
r=sub(F+'kfonts-hakgyoansim-bareondotum-0.1.0/HakgyoansimBareondotumR.woff2','r.woff2')
b=sub(F+'kfonts-hakgyoansim-bareondotum-0.1.0/HakgyoansimBareondotumB.woff2','b.woff2')
m=sub(F+'kossuyeom/HakgyoansimKossuyeomR.ttf','m.woff2')
c=sub(F+'cute/OwnglyphEuiyeonChae.ttf','c.woff2')
css=f'''@font-face{{font-family:"HakgyoBareun";font-weight:400;font-display:swap;src:url(data:font/woff2;base64,{r}) format("woff2")}}
@font-face{{font-family:"HakgyoBareun";font-weight:700;font-display:swap;src:url(data:font/woff2;base64,{b}) format("woff2")}}
@font-face{{font-family:"HakgyoKossuyeom";font-weight:400;font-display:swap;src:url(data:font/woff2;base64,{m}) format("woff2")}}
@font-face{{font-family:"CuteHand";font-weight:400;font-display:swap;src:url(data:font/woff2;base64,{c}) format("woff2")}}'''
img='data:image/webp;base64,'+base64.b64encode(open('yeram.webp','rb').read()).decode()
out=src.replace('/*FONTS*/',css,1)
import re
def emb(m):
    f='img/'+m.group(1)+('.png' if m.group(1)=='logo_head' else '.webp')
    return ('data:image/png;base64,' if f.endswith('.png') else 'data:image/webp;base64,')+base64.b64encode(open(f,'rb').read()).decode()
out=re.sub(r'\{\{IMG:(\w+)\}\}',emb,out)
assert '{{IMG' not in out
open('index.html','w',encoding='utf8').write(out)
print(len(out))
