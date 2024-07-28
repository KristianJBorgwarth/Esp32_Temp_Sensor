import os
import urequests
import json
import hashlib
import binascii
import machine
import time
import network
import gc

global internal_tree

ssid = "some ssid"
password = "some password"
user = 'some user'
repository = 'some repo'
token = ''
default_branch = 'main'
ignore_files = ['/lib/ugit.py', 'README.md', "pymakr.conf"]
ignore = ignore_files
giturl = 'https://github.com/{user}/{repository}'
call_trees_url = f'https://api.github.com/repos/{user}/{repository}/git/trees/{default_branch}?recursive=1'
raw = f'https://raw.githubusercontent.com/{user}/{repository}/master/'

def pull(f_path, raw_url):
    print(f'Attempting to pull {f_path} from GitHub...')
    gc.collect()
    print("Free memory before fetch:", gc.mem_free())
    headers = {'User-Agent': 'ugit-turfptax'}
    try:
        response = urequests.get(raw_url, headers=headers)
        if response.status_code == 200:
            content = response.content
            with open(f_path, 'wb') as file:
                file.write(content)
            print(f"{f_path} fetched successfully.")
        else:
            print(f"Failed to fetch {f_path}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Exception fetching {f_path}: {e}")
    finally:
        response.close()
        gc.collect()
        print("Free memory after fetch:", gc.mem_free())
        time.sleep(1)

def pull_all(tree=call_trees_url,raw = raw,ignore = ignore,isconnected=False):
  if not isconnected:
      wlan = wificonnect() 
  os.chdir('/')
  tree = pull_git_tree()
  internal_tree = build_internal_tree()
  internal_tree = remove_ignore(internal_tree)
  print(' ignore removed ----------------------')
  print(internal_tree)
  for i in tree['tree']:
    if i['type'] == 'tree':
      try:
        os.mkdir(i['path'])
      except:
        print(f'failed to {i["path"]} dir may already exist')
    elif i['path'] not in ignore:
      try:
        os.remove(i['path'])
        internal_tree = remove_item(i['path'],internal_tree)
        gc.collect()
      except:
        continue
      try:
        pull(i['path'],raw + i['path'])
        gc.collect()
      except:
         continue
  if len(internal_tree) > 0:
      print(internal_tree, ' leftover!')
      for i in internal_tree:
          os.remove(i)
  time.sleep(10)
  print('resetting machine in 10: machine.reset()')
  machine.reset()

def wificonnect(ssid=ssid,password=password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    wlan.connect(ssid,password)
    while not wlan.isconnected():
        pass
    print('Wifi Connected!!')
    print(wlan.ifconfig())
    return wlan
  
def build_internal_tree():
  global internal_tree
  internal_tree = []
  os.chdir('/')
  for i in os.listdir():
    add_to_tree(i)
  return(internal_tree)

def add_to_tree(dir_item):
  global internal_tree
  if is_directory(dir_item) and len(os.listdir(dir_item)) >= 1:
    os.chdir(dir_item)
    for i in os.listdir():
      add_to_tree(i)
    os.chdir('..')
  else:
    print(dir_item)
    if os.getcwd() != '/':
      subfile_path = os.getcwd() + '/' + dir_item
    else:
      subfile_path = os.getcwd() + dir_item
    try:
      print(f'sub_path: {subfile_path}')
      internal_tree.append([subfile_path,get_hash(subfile_path)])
    except OSError: # type: ignore # for removing the type error indicator :)
      print(f'{dir_item} could not be added to tree')

def get_hash(file_path):
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return binascii.hexlify(hasher.digest()).decode('utf-8')

def is_directory(file):
  directory = False
  try:
    return (os.stat(file)[8] == 0)
  except:
    return directory
    
def pull_git_tree(tree_url=call_trees_url,raw = raw):
  gc.collect()
  headers = {'User-Agent': 'ugit-turfptax'} 
  if len(token) > 0:
      headers['authorization'] = "bearer %s" % token 
  r = urequests.get(tree_url,headers=headers)
  gc.collect()
  data = json.loads(r.content.decode('utf-8'))
  gc.collect()
  if 'tree' not in data:
      print('\nDefault branch "main" not found. Set "default_branch" variable to your default branch.\n')
      raise Exception(f'Default branch {default_branch} not found.') 
  tree = json.loads(r.content.decode('utf-8'))
  return(tree)
  
def parse_git_tree():
  tree = pull_git_tree()
  dirs = []
  files = []
  for i in tree['tree']:
    if i['type'] == 'tree':
      dirs.append(i['path'])
    if i['type'] == 'blob':
      files.append([i['path'],i['sha'],i['mode']])
  print('dirs:',dirs)
  print('files:',files)
   
def check_ignore(tree=call_trees_url,raw = raw,ignore = ignore):
  os.chdir('/')
  tree = pull_git_tree()
  check = []
  for i in tree['tree']:
    if i['path'] not in ignore:
        print(i['path'] + ' not in ignore')
    if i['path'] in ignore:
        print(i['path']+ ' is in ignore')
        
def remove_ignore(internal_tree,ignore=ignore):
    clean_tree = []
    int_tree = []
    for i in internal_tree:
        int_tree.append(i[0])
    for i in int_tree:
        if i not in ignore:
            clean_tree.append(i)
    return(clean_tree)
        
def remove_item(item,tree):
    culled = []
    for i in tree:
        if item not in i:
            culled.append(i)
    return(culled)
