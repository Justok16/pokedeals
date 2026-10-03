import json,urllib.request,csv,time,html
w=csv.writer(open('wp.csv','w',newline='',encoding='utf-8'))
w.writerow(['slug','nom','installs','note','nb_notes','maj','tags','resume','support','resolu'])
for page in range(1,41):
    u=("https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request%5Bper_page%5D=250"
       f"&request%5Bpage%5D={page}&request%5Bbrowse%5D=popular"
       "&request%5Bfields%5D%5Bdescription%5D=0&request%5Bfields%5D%5Bsections%5D=0")
    for e in range(3):
        try: d=json.load(urllib.request.urlopen(u,timeout=60)); break
        except Exception: time.sleep(5)
    else: continue
    for p in d['plugins']:
        w.writerow([p['slug'],html.unescape(p['name']),p.get('active_installs',0),p.get('rating',0),p.get('num_ratings',0),(p.get('last_updated') or '')[:10],'|'.join((p.get('tags') or {}).keys()) if isinstance(p.get('tags'),dict) else '',html.unescape(p.get('short_description') or '')[:150],p.get('support_threads',0),p.get('support_threads_resolved',0)])
    time.sleep(0.5)
print('ok')
