"""
This script fetches the IDs and popular songs of a predefined list of 
artists on NetCloud Music.

Reference:
A pre-developed API for NetCloud Music by `CeuiLiSA` on Zhihu, 2017.
    Available via https://zhuanlan.zhihu.com/p/30246788
"""

import urllib.request
import urllib.parse
import json


api_base = 'https://api.imjad.cn/cloudmusic/'


def format_get_request(base, data):
    return api_base + '?' + '&'.join('{}={}'.format(k, data[k]) for k in data)


def fetch_artist_info(artist_id):
    data = {'type': 'artist', 'id': artist_id}
    url = format_get_request(api_base, data)
    response_raw = urllib.request.urlopen(url)
    response_txt = response_raw.read().decode('utf-8')
    response_json = json.loads(response_txt)
    return response_json


def search_artist_info(artist_name):
    data = {
        'type': 'search', 
        'search_type': 100, 
        's': urllib.parse.quote(artist_name)
    }
    url = format_get_request(api_base, data)
    response_raw = urllib.request.urlopen(url)
    response_txt = response_raw.read().decode('utf-8')
    response_json = json.loads(response_txt)
    nfound = len(response_json['result']['artists'])
    if nfound == 0:
        return None
    res0_name = response_json['result']['artists'][0]['name']
    res0_id = response_json['result']['artists'][0]['id']
    return res0_name, res0_id


if __name__ == '__main__':
    artists = ['崔健', '李志', '老狼', '万能青年旅店', '朴树', '许巍', 
               '花儿乐队', '马頔', '万晓利', '陈鸿宇', '郑钧', '撒娇', 
               '张玮玮和郭龙',  'Jam', '晓月老板', '新裤子', '满江', 
               '尧十三', '宋冬野', '窦唯', '罗大佑', '海龟先生', 
               '后海大鲨鱼', '陈粒', '赵雷', '丢火车', '陈奕迅', 
               '水木年华', '田馥甄', '谭维维', '李宗盛', '赵照', 
               '衣湿乐队', '苏阳', '谢春花', '南征北战', 'Gala', 
               '痛仰乐队', '莫染', '花粥', '貳佰', '房东的猫', '夏小虎', 
               '好妹妹乐队']
    artist_data = {}

    print('Searching the IDs of the listed artists =====')
    for artist_name in artists:
        res = search_artist_info(artist_name)
        if res is None:
            res_name, res_id = None, -1
        res_name, res_id = res
        if res_name != artist_name:
            print('[Warning] replacing `{}` for `{}`'.format(res_name, artist_name))
        else:
            print('[Info] id for `{}` found to be {}'.format(res_name, res_id))
        artist_data[artist_name] = {'id': res_id}

    print('Fetching more data for the artists =====')
    for artist_name in artists:
        artist_id = artist_data[artist_name]['id']
        if artist_id == -1:
            continue
        info = fetch_artist_info(artist_id)
        nsongs = len(info['hotSongs'])
        print('[Info] found {} songs for `{}`'.format(nsongs, artist_name))
        artist_data[artist_name]['info'] = info

    print('Serializing data =====')
    with open('data/artist_index.json', 'w') as fh:
        fh.write(json.dumps(artist_data, ensure_ascii=False))
    print('[Info] done.')
