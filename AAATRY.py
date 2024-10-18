# -*- coding: utf-8 -*-
import datetime
import json
import time

import requests


def get_data(keyword, index):
    import requests

    url = 'https://www.douyin.com/aweme/v1/web/search/item/'

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.douyin.com/search/%E4%BD%A0%E5%A5%BD?type=video",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    cookies = {
        "ttwid": "1%7CVuEAHhzc_rpr9Qqn8roflevYIm-glnSkTe45a8idDIQ%7C1728896747%7C8d05444b5b5dbf24c5c6405f8157c4abe24ba67dd38d6fdd5fc3894c11ce812b",
        "UIFID_TEMP": "dca68353d0985e2a8bd3e6652fe656c462342d173f24572ea68edd0cbeddca382b29bec0f6137803b446669465487ecdb004a3bbdc6358d0b0667404279aeaf1a68987eaf6ab82f56fa6cecd175f063d",
        "s_v_web_id": "verify_m28shh9v_Si10LXbG_ZvnQ_4sIN_8KMT_OhTurQ8MHESR",
        "fpk1": "U2FsdGVkX1/IradFsBglKUrSiiaD8odiTf6fuNVw5yzVVLu1fQKgZniNG6wT49KjCrdTjUTBcA7XezKTlcPC3w",
        "fpk2": "e2dd8fac9c214f2e57aa0dea655ff030",
        "passport_csrf_token": "9477186fded3cda6a18d2548471b4c7d",
        "passport_csrf_token_default": "9477186fded3cda6a18d2548471b4c7d",
        "bd_ticket_guard_client_web_domain": "2",
        "FORCE_LOGIN": "%7B%22videoConsumedRemainSeconds%22%3A180%7D",
        "UIFID": "dca68353d0985e2a8bd3e6652fe656c462342d173f24572ea68edd0cbeddca388e44d62707c86ce7e9466d8bc9b210fca100fa0ddfa49156d35ba26c0ed63a873b0869328c75efd9227ec1bc7840f3a8bce54a190d0c5d9f8e2a39f5ab907d3413fb858fc48068e6809efd13c525248d02e7aab864c6e92ddc42047ff6dcf5af042b997640d4d64c508e30392b0869e5f80ae79ec6d08a10780846966f01dffc",
        "xgplayer_user_id": "101340608806",
        "pwa2": "%220%7C0%7C3%7C0%22",
        "dy_swidth": "2560",
        "dy_sheight": "1440",
        "__live_version__": "%221.1.2.4155%22",
        "live_use_vvc": "%22false%22",
        "download_guide": "%223%2F20241015%2F1%22",
        "vdg_s": "1",
        "passport_mfa_token": "CjeXCpxldeLWL9hxYU8Ov3EFhkGM%2F08hGkMMfP%2FKmLwaUZzqRP4MFjyFMIBFcqfrS33DaXN85v6CGkoKPKZLm6oIzIfCd8QiDDdWSeyhm0blTiTUHerkC2Mk6h9Wiy0nVCWihJEOkv1LMF33O08xCpSwaPCCuGvH2RDq8N4NGPax0WwgAiIBA5XPDdc%3D",
        "d_ticket": "01bc6179a270eb67485c937cb674dd09e7aa8",
        "n_mh": "9-mIeuD4wZnlYrrOvfzG3MuT6aQmCUtmr8FxV8Kl8xY",
        "is_staff_user": "false",
        "publish_badge_show_info": "%220%2C0%2C0%2C1729059077572%22",
        "SelfTabRedDotControl": "%5B%5D",
        "_bd_ticket_crypt_doamin": "2",
        "__security_server_data_status": "1",
        "passport_assist_user": "ClCOzaw3rA3YbM2eHtM8ixkz06L4qUylA7uK-WElx4pNuWPqNjsYGPh7HQK3XnUeIsnIaBQyL5-5lMpGuXs6twobHJMIvvsF7DqgQQBXYZz_zhpKCjwb036P3qPLdiZydzl4nxBM3uXpAprnLGC4bfLNbbiVh2AzMnD9rsooqE5wpcSZ05lYmP_5aiXQEJg-0ZEQjfLeDRiJr9ZUIAEiAQNMMU1X",
        "sso_uid_tt": "97ec4f7603ee3bc56556f727c3c35c8e",
        "sso_uid_tt_ss": "97ec4f7603ee3bc56556f727c3c35c8e",
        "toutiao_sso_user": "3e04b8cb4bb63f5dd3558ff9454913db",
        "toutiao_sso_user_ss": "3e04b8cb4bb63f5dd3558ff9454913db",
        "sid_ucp_sso_v1": "1.0.0-KDRjNmRjM2EwMzU2N2MzYWI2MWFiZDQxZTA2YjU4YTkxNGQ4N2Q3ZDIKIQiknbCVv829BhDp8724BhjvMSAMMK_W_LUGOAZA9AdIBhoCbGYiIDNlMDRiOGNiNGJiNjNmNWRkMzU1OGZmOTQ1NDkxM2Ri",
        "ssid_ucp_sso_v1": "1.0.0-KDRjNmRjM2EwMzU2N2MzYWI2MWFiZDQxZTA2YjU4YTkxNGQ4N2Q3ZDIKIQiknbCVv829BhDp8724BhjvMSAMMK_W_LUGOAZA9AdIBhoCbGYiIDNlMDRiOGNiNGJiNjNmNWRkMzU1OGZmOTQ1NDkxM2Ri",
        "passport_auth_status": "3b191a8b7905c16895a16775c2268f29%2C1312920a3a4c70a89bae330b1d7b7d3a",
        "passport_auth_status_ss": "3b191a8b7905c16895a16775c2268f29%2C1312920a3a4c70a89bae330b1d7b7d3a",
        "uid_tt": "91f3cff9985a70c7fd9abbd8499574e8",
        "uid_tt_ss": "91f3cff9985a70c7fd9abbd8499574e8",
        "sid_tt": "31deb9686c8505a7f3d14dc1295380aa",
        "sessionid": "31deb9686c8505a7f3d14dc1295380aa",
        "sessionid_ss": "31deb9686c8505a7f3d14dc1295380aa",
        "live_can_add_dy_2_desktop": "%221%22",
        "_bd_ticket_crypt_cookie": "818d8ee0cfccbebc170932ddb4188948",
        "sid_guard": "31deb9686c8505a7f3d14dc1295380aa%7C1729067502%7C5183998%7CSun%2C+15-Dec-2024+08%3A31%3A40+GMT",
        "sid_ucp_v1": "1.0.0-KGNiNGQzZmFlMmEyZDI3NTQ3YTMzN2MzOWYzZWNiMGM4MWM3NmY1NjEKGwiknbCVv829BhDu8724BhjvMSAMOAZA9AdIBBoCbHEiIDMxZGViOTY4NmM4NTA1YTdmM2QxNGRjMTI5NTM4MGFh",
        "ssid_ucp_v1": "1.0.0-KGNiNGQzZmFlMmEyZDI3NTQ3YTMzN2MzOWYzZWNiMGM4MWM3NmY1NjEKGwiknbCVv829BhDu8724BhjvMSAMOAZA9AdIBBoCbHEiIDMxZGViOTY4NmM4NTA1YTdmM2QxNGRjMTI5NTM4MGFh",
        "volume_info": "%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D",
        "strategyABtestKey": "%221729126851.698%22",
        "store-region": "cn-fj",
        "store-region-src": "uid",
        "SearchResultListTypeChangedManually": "%221%22",
        "SEARCH_RESULT_LIST_TYPE": "%22multi%22",
        "__ac_signature": "_02B4Z6wo00f01eui.ywAAIDB3IY7cod5pWnrgvuAAB364f",
        "hevc_supported": "true",
        "xg_device_score": "7.802204888412783",
        "device_web_cpu_core": "12",
        "device_web_memory_size": "8",
        "architecture": "amd64",
        "stream_recommend_feed_params": "%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22",
        "csrf_session_id": "69800725dada9fe8640a7acaa8e48e2d",
        "WallpaperGuide": "%7B%22showTime%22%3A1728973866307%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A41%2C%22cursor2%22%3A12%2C%22hoverTime%22%3A1729065479094%7D",
        "FOLLOW_LIVE_POINT_INFO": "%22MS4wLjABAAAAAXX9j8RaPw7ZoQEp6M9IQ9HONxZwFeHvdbtbhbcxFVwb9CEcYS2Yo0bu1KJvPt2y%2F1729180800000%2F0%2F0%2F1729136848189%22",
        "FOLLOW_NUMBER_YELLOW_POINT_INFO": "%22MS4wLjABAAAAAXX9j8RaPw7ZoQEp6M9IQ9HONxZwFeHvdbtbhbcxFVwb9CEcYS2Yo0bu1KJvPt2y%2F1729180800000%2F0%2F1729136248189%2F0%22",
        "stream_player_status_params": "%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22",
        "bd_ticket_guard_client_data": "eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSEVqbTRucjQxZVR0TUJSK2wvRHFWOXZXS2ZXRjhSYXY1ZnNiYS93YVQ4TVR4RjVaWkZxMDFkSHNrbVVYcmM2L3lUL0poTURld2tyNTdKZVREOHRrLzA9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D",
        "odin_tt": "68bf26b1337ab897e237a45e54dd1c0d7c3023bf7ee8a37c015f98ca37421ff2147c8f1087757416a28687acfd55d1a7",
        "passport_fe_beating_status": "false",
        "__ac_nonce": "067108aa000b773ab801b",
        "home_can_add_dy_2_desktop": "%220%22",
        "IsDouyinActive": "true"
    }
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": "aweme_video_web",
        "enable_history": "1",
        "keyword": f"{keyword}",
        "search_source": "normal_search",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "offset": f"{index}",
        "count": "30",
        "need_filter_settings": "1",
        "list_type": "single",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "pc_libra_divert": "Windows",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1707",
        "screen_height": "1067",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Edge",
        "browser_version": "129.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "129.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "10",
        "effective_type": "4g",
        "round_trip_time": "100",
        "webid": "7346781703702382121",
        "msToken": "ndZ3ngOvND6qfniBskis-9kP8-XtZZEYtrvTFiVz-rsmdfRvqRRja_GewR4pTKHuFlBlduq9KP4K5DsHVemvJd50fQaTRJPYw0NH4JCpdcCnv_cqq0abzbIH1Qwtwr8gcajSesIWjb6x2wr0YTjk2RVqAeiz42Af5L2QD1vvhCgp5uzcy3-oLn4=",
        "a_bogus": "OX45httyYNWRFVMtucrFyenl8/9MNBWy3PTORbCl9xE5bqePVmPxdPCpbxuw48uUbupskHVH0flMbdVcBzt0ZCrpqmkDSYvj5z29nusog1H4GGJh7HgDCjbxuk-a8KTO8QAjiMJ56ssE2xI5nHCwAdlCL/-xBRRDOp34VluSN2ym0Sujho25aVtpihJqJf=="
    }

    # 发送GET请求
    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    return response


def save_data(response, name,index):
    if response.status_code == 200:
        try:
            # 将响应的 JSON 数据转换为 Python 字典
            data = response.json()

            # 将数据写入 JSON 文件
            with open(f'{name}_{index}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)  # 使用 indent 参数格式化输出

            print(f"数据已成功写入 '{name}.json' 文件")
        except json.JSONDecodeError:
            print("无法解析响应的 JSON 数据")
    else:
        print(f"请求失败，状态码：{response.status_code}")


def read_data(name, results,index):
    with open(f'{name}_{index}.json', 'r', encoding='utf-8') as f:
        rs = f.read()  # 读取文件内容

    # 将字符串加载为 JSON 对象（字典）
    data = json.loads(rs)
    datas = data['data']

    for d in datas:
        # print(json.dumps(d, ensure_ascii=False, indent=4))
        aweme_info = d['aweme_info']
        statistics = aweme_info["statistics"]
        digg_count = statistics['digg_count']
        comment_count = statistics['comment_count']
        share_count = statistics['share_count']
        create_time = get_time(aweme_info['create_time'])
        desc = aweme_info['desc']
        aweme_id = aweme_info['aweme_id']
        author = aweme_info["author"]["nickname"]
        video = aweme_info["video"]["play_addr"]["url_list"][0]
        # 检查 '描述' 或 '作者' 是否包含指定的 name 关键词
        if name in desc or name in author:
            info_dict = {
                '创建时间': create_time,  # 创建时间
                '描述': desc,  # 描述
                '唯一ID': aweme_id,  # 唯一 ID
                '统计信息': statistics,  # 统计信息
                '作者': author,  # 作者
                '视频播放地址': video,  # 视频播放地址
                '点赞数': digg_count,  # 点赞数
                '评论数': comment_count,  # 评论数
                '分享数': share_count  # 分享数
            }

            # 将字典添加到结果列表中
            results.append(info_dict)
    return results


def get_time(create_time):
    from datetime import datetime

    # 定义时间戳
    timestamp = create_time

    # 转换为 UTC 时间
    dt_object_utc = datetime.utcfromtimestamp(timestamp)
    formatted_time_utc = dt_object_utc.strftime('%Y-%m-%d %H:%M:%S')

    # 转换为本地时间
    dt_object_local = datetime.fromtimestamp(timestamp)
    formatted_time_local = dt_object_local.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time_local


import csv


# def save_results_to_csv(results, file_name):
#     # 打开文件以写入
#     with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
#         # 创建 csv.writer 对象
#         writer = csv.writer(csvfile)
#
#         # 写入表头
#         writer.writerow(["Create Time", "Description", "Author"])
#
#         # 写入每一行数据
#         for item in results:
#             writer.writerow([item['create_time'], item['desc'], item['aweme_id']])

def save_results_to_html(results, file_name):
    # 创建HTML文件的基本结构
    html_content = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>结果表格</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>结果表格</h1>
        <table>
            <tr>
                <th>创建时间</th>
                <th>描述</th>
                <th>唯一ID</th>
                <th>作者</th>
                <th>视频播放地址</th>
                <th>点赞数</th>
                <th>评论数</th>
                <th>分享数</th>
            </tr>
    """

    # 添加数据行
    for item in results:
        html_content += f"""
            <tr>
                <td>{item['创建时间']}</td>
                <td>{item['描述']}</td>
                <td>{item['唯一ID']}</td>
                <td>{item['作者']}</td>
                <td>{item['视频播放地址']}</td>
                <td>{item['点赞数']}</td>
                <td>{item['评论数']}</td>
                <td>{item['分享数']}</td>
            </tr>
        """

    # 完成HTML结构
    html_content += """
            </table>
        </body>
    </html>
    """

    # 将HTML内容写入文件
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(html_content)


if __name__ == '__main__':
    name = 'S14'
    results = []
    index = 0
    for page in range(2):
        index = page * 30  # 每次迭代 index 乘以 30，表示每页的偏移量
        response = get_data(name, index)
        save_data(response, name,index)
        results = read_data(name, results,index)
        time.sleep(10)


    # save_results_to_csv(results, f'{name}_results.csv')
    # print(results)
    save_results_to_html(results, f'{name}.html')
