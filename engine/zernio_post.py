"""Post to the FOOTBALL channel (TikTok @dexedits62 + YouTube @dexedits-y3y) through its own Zernio account.
The API key is read from ~/.config/dex-football/zernio.key (never commit it). The F1 channel keeps using the Zernio
connector.
Usage:
  python3 zernio_post.py accounts
  python3 zernio_post.py post <tiktok|youtube> <media_url> <caption_file> [--title "YT title"] [--at 2026-11-28T08:00:00+01:00]
Without --at it publishes now. The connection here drops often, so every call retries on network errors."""
import json, os, sys, time, urllib.request, urllib.error

BASE = 'https://zernio.com/api/v1'
ACCOUNTS = {'tiktok': '6b09da6d630ef5302d6940f0', 'youtube': '6b09daa8630ef5302d694105'}
KEY = open(os.path.expanduser('~/.config/dex-football/zernio.key')).read().strip()


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    for i in range(6):
        req = urllib.request.Request(BASE + path, data=data, method=method, headers={
            'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json', 'User-Agent': 'dex-client/1.0'})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=120).read() or b'{}')
        except urllib.error.HTTPError as e:
            return {'_http': e.code, '_body': e.read().decode()[:800]}
        except Exception as e:
            print('network retry', i + 1, type(e).__name__, file=sys.stderr); time.sleep(8)
    return {'_error': 'network failed 6 times'}


if __name__ == '__main__':
    if sys.argv[1] == 'accounts':
        d = call('GET', '/accounts')
        print([(a.get('platform'), a.get('username'), a.get('_id')) for a in d.get('accounts', [])] or d)
    elif sys.argv[1] == 'post':
        plat, url, capf = sys.argv[2], sys.argv[3], sys.argv[4]
        args = sys.argv[5:]
        title = args[args.index('--title') + 1] if '--title' in args else None
        at = args[args.index('--at') + 1] if '--at' in args else None
        p = {'platform': plat, 'accountId': ACCOUNTS[plat]}
        if plat == 'youtube':
            p['platformSpecificData'] = {'title': title or open(capf).read()[:95], 'visibility': 'public'}
        body = {'content': open(capf).read().strip(), 'platforms': [p], 'mediaItems': [{'type': 'video', 'url': url}]}
        if at: body.update(scheduledFor=at, timezone='Africa/Lagos')
        else: body['publishNow'] = True
        print(json.dumps(call('POST', '/posts', body))[:1500])
