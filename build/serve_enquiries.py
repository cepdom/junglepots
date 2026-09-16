"""Local review server. Run with Python; open http://127.0.0.1:8766/junglepots-contact.html.
Enquiries are stored outside the served folder. This is not a production service.
"""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from email.parser import BytesParser
from email.policy import default
from pathlib import Path
import json,uuid,re
ROOT=Path(__file__).resolve().parent
INBOX=ROOT.parent/'JunglePots-local-enquiries'
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
 def reply(self,code,data):
  body=json.dumps(data).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_POST(self):
  if self.path!='/api/enquiries':return self.reply(404,{'error':'Not found'})
  if self.headers.get('Origin') not in (None,'http://127.0.0.1:8766','http://localhost:8766'):return self.reply(403,{'error':'Origin not allowed'})
  try:
   length=int(self.headers.get('Content-Length','0'))
   if not 0<length<21*1024*1024:raise ValueError('Request exceeds 20 MB attachment limit.')
   content=self.headers.get('Content-Type','')
   if not content.startswith('multipart/form-data;'):raise ValueError('Expected form data.')
   message=BytesParser(policy=default).parsebytes(('Content-Type: '+content+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+self.rfile.read(length))
   fields={};files=[]
   for part in message.iter_parts():
    name=part.get_param('name',header='content-disposition');filename=part.get_filename();body=part.get_payload(decode=True) or b''
    if filename:
     ext=Path(filename).suffix.lower()
     valid=(ext=='.pdf' and body.startswith(b'%PDF-')) or (ext in ('.jpg','.jpeg') and body.startswith(b'\xff\xd8\xff')) or (ext=='.png' and body.startswith(b'\x89PNG\r\n\x1a\n')) or (ext=='.webp' and body[:4]==b'RIFF' and body[8:12]==b'WEBP')
     if name!='attachments' or not valid or len(body)>10*1024*1024:raise ValueError('Invalid attachment type or size.')
     files.append((filename,ext,body))
    elif name:
     value=body.decode('utf-8');
     if len(value)>5000:raise ValueError('A field is too long.')
     fields[name]=value.strip()
   if len(files)>5 or sum(len(f[2]) for f in files)>20*1024*1024:raise ValueError('Too many attachments or total size exceeded.')
   if any(not fields.get(k) for k in ('name','email','location','brief')):raise ValueError('Complete all required fields.')
   if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',fields['email']):raise ValueError('Enter a valid email.')
   if fields.get('quantity') and (not fields['quantity'].isdigit() or int(fields['quantity'])<1):raise ValueError('Quantity must be a positive whole number.')
   reference=uuid.uuid4().hex;folder=INBOX/reference;folder.mkdir(parents=True)
   manifest=[]
   for i,(name,ext,body) in enumerate(files):
    stored=str(i+1)+ext;(folder/stored).write_bytes(body);manifest.append({'original_name':name,'stored_name':stored,'bytes':len(body)})
   (folder/'enquiry.json').write_text(json.dumps({'reference':reference,'fields':fields,'attachments':manifest},ensure_ascii=False,indent=2),encoding='utf-8')
   self.reply(201,{'reference':reference})
  except (ValueError,UnicodeError) as e:self.reply(400,{'error':str(e)})
  except Exception:self.reply(500,{'error':'Local storage failed. Please try again.'})
if __name__=='__main__':
 print('Local review: http://127.0.0.1:8766/junglepots-contact.html',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8766),Handler).serve_forever()
