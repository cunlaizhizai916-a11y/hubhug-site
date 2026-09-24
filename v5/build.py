import base64,pathlib
d=pathlib.Path(__file__).parent
s=(d/'src.html').read_text()
for k in ['hero','svc1','svc2','svc3','portrait']:
    s=s.replace('{{%s}}'%k,'data:image/jpeg;base64,'+base64.b64encode((d/'_img'/f'{k}.jpg').read_bytes()).decode())
(d/'index.html').write_text(s)
print((d/'index.html').stat().st_size/1024,'KB')
