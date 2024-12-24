from .wbi import encWbi, getWbiKeys
import requests

def getSingleVideoInfo(avid: int = 0, bv: str = '') -> dict:
    '获取单个视频的信息'
    if avid == 0 and bv == '':
        return {'status': 'error', 'message': 'avid 和 bv 至少需要一个'}
    if avid != 0:
        params = {
            'aid': avid
        }
    else:
        params = {
            'bvid': bv
        }
    img_key, sub_key = getWbiKeys()
    signed_params = encWbi(params, img_key, sub_key)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
    }
    
    response = requests.get(
        "https://api.bilibili.com/x/web-interface/wbi/view/detail",
        params=signed_params,
        headers=headers,
    )

    video_info = response.json()
    
    video_data = {
        "aid": video_info["data"]["View"]["aid"],
        "bvid": video_info["data"]["View"]["bvid"],
        "pubdate": video_info["data"]["View"]["pubdate"],
        "title": video_info["data"]["View"]["title"],
        "description": video_info["data"]["View"]["desc"],
        "tag": ";".join([tag["tag_name"] for tag in video_info["data"]["Tags"]]),
        "pic": video_info["data"]["View"]["pic"].replace("http://", "//"),
        "type_id": video_info["data"]["View"]["tid"],
        "user_id": video_info["data"]["View"]["owner"]["mid"],
    }
    
    return video_data
