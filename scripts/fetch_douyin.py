#!/usr/bin/env python3
"""下载抖音分享链接的无水印视频（不需要登录）。

python3 fetch_douyin.py "<分享文本或 https://v.douyin.com/xxx/>" --out 参考/原片.mp4
同时在 --out 旁写 <名>.json：标题、作者、时长、点赞/转发/收藏/评论。
原理：iPhone UA + cookie 打开短链 → iesdouyin 分享页 → _ROUTER_DATA.videoInfoRes → play_addr（playwm 换 play）。
"""
import argparse, json, re, subprocess, sys, tempfile, os
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
ap = argparse.ArgumentParser(); ap.add_argument('link'); ap.add_argument('--out', required=True); a = ap.parse_args()
m = re.search(r'https?://v\.douyin\.com/[\w-]+/?', a.link) or re.search(r'video/(\d+)', a.link)
if not m: sys.exit('没找到抖音链接')
cj = tempfile.mktemp()
def curl(*args): return subprocess.run(['curl', '-sL', '-c', cj, '-b', cj, '-A', UA, *args], capture_output=True, text=True).stdout
if 'v.douyin.com' in m.group(0):
    loc = subprocess.run(['curl', '-sI', '-c', cj, '-A', UA, m.group(0)], capture_output=True, text=True).stdout
    vid = re.search(r'video/(\d+)', loc).group(1)
else:
    vid = m.group(1)
html = ''
for _ in range(3):
    html = curl(f'https://www.iesdouyin.com/share/video/{vid}/')
    if 'videoInfoRes' in html: break
i = html.find('_ROUTER_DATA = ') + 15; j = html.find('</script>', i)
d = json.loads(html[i:j].strip().rstrip(';'))
page = next(v for k, v in d['loaderData'].items() if isinstance(v, dict) and 'videoInfoRes' in v)
it = page['videoInfoRes']['item_list'][0]
url = it['video']['play_addr']['url_list'][0].replace('playwm', 'play')
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
subprocess.run(['curl', '-sL', '-A', UA, '-o', a.out, url], check=True)
meta = {'id': vid, 'desc': it.get('desc'), 'author': it.get('author', {}).get('nickname'), 'duration_ms': it['video'].get('duration'), 'stats': it.get('statistics')}
json.dump(meta, open(os.path.splitext(a.out)[0] + '.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(meta, ensure_ascii=False)); print('saved', a.out, os.path.getsize(a.out))
