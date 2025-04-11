from pathlib import Path
from time import sleep
from datetime import datetime
import os, re, zipfile, sys, shutil, conf


intro ="USAGE tracebook.py [FLAGS]\n\
Use trackbook.py -h or trackbook.py --help for more info."
def timer(count=5):
  '''The time it should count'''
  for i in range(int(count)+1):
    print(f"\rStart: {count - i}", end="")
    sleep(1)
    
    
args = sys.argv
try:
  if args[1].lower() in ['-h', '--help']:
    print("\nTrack Books V1 \n\
    Searches for all specified file types and compresses them in current directory as a zip file.\n\n You can change the file types from conf.py under trackBooks setion in SEARCH_BOOK varaible. \n\nFlags available\n\n\t -v or --verbose  To be verbose\n\t -vv or --very-verbose To be very Verbose(Print pdf directory names as well).\n\t --no-count  Don't do contdown.\n\t")
    sys.exit()
  else:
    print(intro)
except Exception:
  print(intro)

if not '--no-count' in args:
  timer()
pdfregex = re.compile(r'^.+\.' + conf.SEARCH_BOOK + '$')
walk_where =Path('/storage/emulated/0/')
# Change mode to append or check if the file exists, then decide what to do.
dnow = datetime.now()
zb= f'{conf.NZIP_NAME}%s:%s:%s-%s-%s-%s.zip'%(dnow.hour, dnow.minute, dnow.second, dnow.day, dnow.month, dnow.year)
zf = zipfile.ZipFile(f'{zb}', 'w')

for F, SF, File in os.walk(walk_where):
  try:
    if args[1].lower() in ['-vv', '--very-verbose']:
      print(f"In directory {F}\n")
  except Exception:
    args.insert(1, 'none')
    continue
  
  for f in File:
    if re.match(pdfregex, f):
      shutil.copy(Path(F)/f, '.')
      zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
      print(f"Found your book named '{f}'\nCopied and compressed it into {zf.filename}\n\n")
      os.remove(Path('.')/f)
 
print('Done ✓')   
zf.close()
print(f"zip file size is {round(os.path.getsize(zb)/1024, 2)}MB")
