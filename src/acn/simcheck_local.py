import re,sys,glob,html,subprocess,collections
def clean(t): 
    t=html.unescape(re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>',' ',t)); t=re.sub(r'<[^>]+>',' ',t); return t
def words(t): return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", t.lower())
def src_text(p):
    if p.endswith('.pdf'): return subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
    return clean(open(p,errors='ignore').read())
ms=subprocess.run(['pdftotext','/home/claude/ACN-PROJECT-V2/springer_cicps_submission/main.pdf','-'],capture_output=True,text=True).stdout
i=ms.rfind('References'); ms=ms[:i] if i>0 else ms
mw=words(ms); print('manuscript words (excl. references):',len(mw))
N=int(sys.argv[1]) if len(sys.argv)>1 else 8
def grams(w,n): return [tuple(w[i:i+n]) for i in range(len(w)-n+1)]
mg=grams(mw,N); cover=[False]*len(mw)
res=[]
for p in sorted(glob.glob('/tmp/src_texts/*')):
    sw=words(src_text(p)); sg=set(grams(sw,N)); hit=[i for i,g in enumerate(mg) if g in sg]
    for i in hit:
        for j in range(i,i+N): cover[j]=True
    res.append((p.split('/')[-1],len(sw),len(hit)))
    if hit:
        # print matched spans
        spans=[];s=hit[0];e=hit[0]
        for i in hit[1:]:
            if i<=e+1: e=i
            else: spans.append((s,e)); s=e=i
        spans.append((s,e))
        for s,e in spans[:6]: print('  [%s] %s'%(p.split('/')[-1],' '.join(mw[s:e+N])))
print(); [print(f'{n:24s} src_words={a:6d}  matching {N}-grams={h}') for n,a,h in res]
print(f'\nTOTAL manuscript words covered by any {N}-gram match: {sum(cover)} / {len(mw)} = {100*sum(cover)/len(mw):.2f}%')
