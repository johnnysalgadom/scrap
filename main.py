import requests
import json
import os
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import ProductModel, CategoryModel, PostModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv('database_uri')
CREATED_BY = 'scrapy'
PAGES = 5
INITIAL_PAGE = 1
PRODUCT_PAGE = 'https://app.kajabi.com/admin/sites/46190/products?page='
WEBSITE_URL = 'https://app.kajabi.com'
API_URL_BASE = 'https://app.kajabi.com/api/admin/products/'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
s = Session()

#change the cookies and headers based of the evaluation day. Get it from kajabi website
page_cookies = {
    '_gcl_au': '1.1.96861702.1653058689',
    '_vwo_uuid_v2': 'DBE4263CD03763B77C98443DD0244C8A2|44b685ea5444cee5efbe5adbeb8c02ad',
    '_vwo_uuid': 'DBE4263CD03763B77C98443DD0244C8A2',
    'OptanonAlertBoxClosed': '2022-05-20T15:14:19.933Z',
    '_rdt_uuid': '1653059660174.488f2495-4859-4a38-aed3-f6f53bc10a04',
    '_fbp': 'fb.1.1653059660194.982904317',
    'hubspotutk': 'a20b697c912dabace88f78b6887d89ca',
    '_pin_unauth': 'dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA',
    'rbuid': 'rbos-7565073a-6ce9-472b-89b5-9f214626655d',
    '_hjSessionUser_2946942': 'eyJpZCI6ImM0M2IzNzc5LWVmZjAtNTEzOC1iOGFiLWI3YzFhZGYxNDEzMiIsImNyZWF0ZWQiOjE2NTMwNTg2ODk0OTUsImV4aXN0aW5nIjp0cnVlfQ==',
    'kjb_signin_id': 'd5e12466-98c7-4984-a789-a1e7df43f124',
    'kjb_app_fmarketing': 'vip%40fasterwaytofatloss.com%7CPro+Monthly+%2B+Access%7Chome_trial_growth',
    '_pin_unauth': 'dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA',
    'ajs_user_id': '258278909666892368587741315999637852220',
    'ajs_anonymous_id': '24bcca18-dfa0-44cf-b33d-bad2135cd171',
    '_gid': 'GA1.2.861677027.1654614261',
    '_vis_opt_s': '2%7C',
    '_vis_opt_test_cookie': '1',
    '__hssrc': '1',
    '__cfruid': 'be4707f34b6ffd42bacec94fa34dcff6d8dcb453-1654614263',
    '_kjb_ua_components': '33e07560e858fe73042eb0b50b056baf',
    '_hjSessionUser_1925747': 'eyJpZCI6IjMxYTBkMDEzLTViMDYtNWZlYy1hOTEyLWViMTEyMDZkODE2NSIsImNyZWF0ZWQiOjE2NTQ2MTU4MDg1NDUsImV4aXN0aW5nIjp0cnVlfQ==',
    'tatari-session-cookie': 'f642e9bc-6e85-65f3-708c-5cea22b2ad01',
    '_vwo_ds': '3%3At_0%2Ca_0%3A0%241653058686%3A47.10241406%3A%3A41_0%2C38_0%2C10_0%2C7_0%2C6_0%3A363_0%2C255_0%2C129_0%2C124_0%3A0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Jun+07+2022+19%3A52%3A44+GMT-0500+(hora+est%C3%A1ndar+de+Per%C3%BA)&version=6.35.0&isIABGlobal=false&hosts=&consentId=63d46b73-9f3b-4951-997c-89acc478393a&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&geolocation=PE%3BLMA&AwaitingReconsent=false',
    '_derived_epik': 'dj0yJnU9aURFRWh2cXFEcFc3cHdIZXNGbzc0N1dlZzNobThKY0wmbj1DSjRUbjlaRHBIQmZMMFhNMnpxYmxRJm09MSZ0PUFBQUFBR0tmOHRzJnJtPTEmcnQ9QUFBQUFHS2Y4dHM',
    '_kjb_session': 'f516c919167d561e19c178440bb4018d',
    'ab.storage.sessionId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%22f7919484-e113-525e-47a5-fea2d0d218ec%22%2C%22e%22%3A1654727962587%2C%22c%22%3A1654726162590%2C%22l%22%3A1654726162590%7D',
    'ab.storage.deviceId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%2243104d41-1cc3-64dc-6ced-b0667655160c%22%2C%22c%22%3A1653058688943%2C%22l%22%3A1654726162591%7D',
    'ab.storage.userId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%22258278909666892368587741315999637852220%22%2C%22c%22%3A1654177606358%2C%22l%22%3A1654726162592%7D',
    '__zlcmid': '10fjVdCvDZh26zO',
    '_clck': 'hvcyev|1|f28|0',
    '__cf_bm': '6a2WTgq2lRcNn80yBu_nca2v63Lp6b59Fydwd56Ox80-1654906315-0-AcEnkA+86oNFvFl11FR2Q8NMgipc1OXlQjkcpyXmts41DQ6A1/OQV/VfnxbJxry/n0OxZgzgCpTNkk6JIjC6j18=',
    '_sp_ses.5a96': '*',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_2946942': 'eyJpZCI6IjhkZmQ2YzAyLTdmMzctNDM3Mi1iY2M3LWI3NjdmZGM0MmFiNCIsImNyZWF0ZWQiOjE2NTQ5MDYzMTcyMTUsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '__hstc': '223412292.a20b697c912dabace88f78b6887d89ca.1653058690021.1654887792030.1654906319225.20',
    'amp_d4cd2a': '2VXRywwNWz5zLHKVBgOP4N.Njg0NTk=..1g581kpre.1g581uqsm.0.3l.3l',
    '__atuvc': '21%7C22%2C96%7C23',
    '__atuvs': '62a3ddcce44c0e97004',
    '_sp_id.5a96': '2c2e2b45-4946-43e3-98ab-ec556fcfbbdb.1653059660.20.1654906646.1654887791.e0a164d9-a82e-4f82-97c2-e2ad3708fb19',
    '_uetsid': '1c7e69d0e67311eca36723fbfea95933',
    '_uetvid': '71afa620e27a11ec9f06398f70b0d565',
    'tatari-cookie-test': '25504413',
    '_derived_epik': 'dj0yJnU9OTBBbnZxMlVLQTZVdk1jeDFpeUZRb1hmZldoWjBocUombj11VjFGZU1iV0ZybHgzdVBlVUxXUHFnJm09MSZ0PUFBQUFBR0tqM3hVJnJtPTEmcnQ9QUFBQUFHS2ozeFU',
    '_clsk': '8rrz84|1654906646356|6|1|www.clarity.ms/eus2-e/collect',
    '__hssc': '223412292.5.1654906319225',
    '_ga': 'GA1.2.277638690.1653059660',
    '_ga_5R3LGJJD0H': 'GS1.1.1654906316.17.1.1654906646.0',
    '_dd_s': 'rum=1&id=7486a017-61e0-4f5e-80a5-1cc1146c4668&created=1654906312750&expire=1654907845336',
}

page_headers = {
    'authority': 'app.kajabi.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_gcl_au=1.1.96861702.1653058689; _vwo_uuid_v2=DBE4263CD03763B77C98443DD0244C8A2|44b685ea5444cee5efbe5adbeb8c02ad; _vwo_uuid=DBE4263CD03763B77C98443DD0244C8A2; OptanonAlertBoxClosed=2022-05-20T15:14:19.933Z; _rdt_uuid=1653059660174.488f2495-4859-4a38-aed3-f6f53bc10a04; _fbp=fb.1.1653059660194.982904317; hubspotutk=a20b697c912dabace88f78b6887d89ca; _pin_unauth=dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA; rbuid=rbos-7565073a-6ce9-472b-89b5-9f214626655d; _hjSessionUser_2946942=eyJpZCI6ImM0M2IzNzc5LWVmZjAtNTEzOC1iOGFiLWI3YzFhZGYxNDEzMiIsImNyZWF0ZWQiOjE2NTMwNTg2ODk0OTUsImV4aXN0aW5nIjp0cnVlfQ==; kjb_signin_id=d5e12466-98c7-4984-a789-a1e7df43f124; kjb_app_fmarketing=vip%40fasterwaytofatloss.com%7CPro+Monthly+%2B+Access%7Chome_trial_growth; _pin_unauth=dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA; ajs_user_id=258278909666892368587741315999637852220; ajs_anonymous_id=24bcca18-dfa0-44cf-b33d-bad2135cd171; _gid=GA1.2.861677027.1654614261; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; __hssrc=1; __cfruid=be4707f34b6ffd42bacec94fa34dcff6d8dcb453-1654614263; _kjb_ua_components=33e07560e858fe73042eb0b50b056baf; _hjSessionUser_1925747=eyJpZCI6IjMxYTBkMDEzLTViMDYtNWZlYy1hOTEyLWViMTEyMDZkODE2NSIsImNyZWF0ZWQiOjE2NTQ2MTU4MDg1NDUsImV4aXN0aW5nIjp0cnVlfQ==; tatari-session-cookie=f642e9bc-6e85-65f3-708c-5cea22b2ad01; _vwo_ds=3%3At_0%2Ca_0%3A0%241653058686%3A47.10241406%3A%3A41_0%2C38_0%2C10_0%2C7_0%2C6_0%3A363_0%2C255_0%2C129_0%2C124_0%3A0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+07+2022+19%3A52%3A44+GMT-0500+(hora+est%C3%A1ndar+de+Per%C3%BA)&version=6.35.0&isIABGlobal=false&hosts=&consentId=63d46b73-9f3b-4951-997c-89acc478393a&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&geolocation=PE%3BLMA&AwaitingReconsent=false; _derived_epik=dj0yJnU9aURFRWh2cXFEcFc3cHdIZXNGbzc0N1dlZzNobThKY0wmbj1DSjRUbjlaRHBIQmZMMFhNMnpxYmxRJm09MSZ0PUFBQUFBR0tmOHRzJnJtPTEmcnQ9QUFBQUFHS2Y4dHM; _kjb_session=f516c919167d561e19c178440bb4018d; ab.storage.sessionId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%22f7919484-e113-525e-47a5-fea2d0d218ec%22%2C%22e%22%3A1654727962587%2C%22c%22%3A1654726162590%2C%22l%22%3A1654726162590%7D; ab.storage.deviceId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%2243104d41-1cc3-64dc-6ced-b0667655160c%22%2C%22c%22%3A1653058688943%2C%22l%22%3A1654726162591%7D; ab.storage.userId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%22258278909666892368587741315999637852220%22%2C%22c%22%3A1654177606358%2C%22l%22%3A1654726162592%7D; __zlcmid=10fjVdCvDZh26zO; _clck=hvcyev|1|f28|0; __cf_bm=6a2WTgq2lRcNn80yBu_nca2v63Lp6b59Fydwd56Ox80-1654906315-0-AcEnkA+86oNFvFl11FR2Q8NMgipc1OXlQjkcpyXmts41DQ6A1/OQV/VfnxbJxry/n0OxZgzgCpTNkk6JIjC6j18=; _sp_ses.5a96=*; _hjIncludedInSessionSample=0; _hjSession_2946942=eyJpZCI6IjhkZmQ2YzAyLTdmMzctNDM3Mi1iY2M3LWI3NjdmZGM0MmFiNCIsImNyZWF0ZWQiOjE2NTQ5MDYzMTcyMTUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; __hstc=223412292.a20b697c912dabace88f78b6887d89ca.1653058690021.1654887792030.1654906319225.20; amp_d4cd2a=2VXRywwNWz5zLHKVBgOP4N.Njg0NTk=..1g581kpre.1g581uqsm.0.3l.3l; __atuvc=21%7C22%2C96%7C23; __atuvs=62a3ddcce44c0e97004; _sp_id.5a96=2c2e2b45-4946-43e3-98ab-ec556fcfbbdb.1653059660.20.1654906646.1654887791.e0a164d9-a82e-4f82-97c2-e2ad3708fb19; _uetsid=1c7e69d0e67311eca36723fbfea95933; _uetvid=71afa620e27a11ec9f06398f70b0d565; tatari-cookie-test=25504413; _derived_epik=dj0yJnU9OTBBbnZxMlVLQTZVdk1jeDFpeUZRb1hmZldoWjBocUombj11VjFGZU1iV0ZybHgzdVBlVUxXUHFnJm09MSZ0PUFBQUFBR0tqM3hVJnJtPTEmcnQ9QUFBQUFHS2ozeFU; _clsk=8rrz84|1654906646356|6|1|www.clarity.ms/eus2-e/collect; __hssc=223412292.5.1654906319225; _ga=GA1.2.277638690.1653059660; _ga_5R3LGJJD0H=GS1.1.1654906316.17.1.1654906646.0; _dd_s=rum=1&id=7486a017-61e0-4f5e-80a5-1cc1146c4668&created=1654906312750&expire=1654907845336',
    'referer': 'https://app.kajabi.com/admin/sites/46190/products?page=4',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}

api_cookies = {
    '_gcl_au': '1.1.96861702.1653058689',
    '_vwo_uuid_v2': 'DBE4263CD03763B77C98443DD0244C8A2|44b685ea5444cee5efbe5adbeb8c02ad',
    '_vwo_uuid': 'DBE4263CD03763B77C98443DD0244C8A2',
    'OptanonAlertBoxClosed': '2022-05-20T15:14:19.933Z',
    '_rdt_uuid': '1653059660174.488f2495-4859-4a38-aed3-f6f53bc10a04',
    '_fbp': 'fb.1.1653059660194.982904317',
    'hubspotutk': 'a20b697c912dabace88f78b6887d89ca',
    '_pin_unauth': 'dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA',
    'rbuid': 'rbos-7565073a-6ce9-472b-89b5-9f214626655d',
    '_hjSessionUser_2946942': 'eyJpZCI6ImM0M2IzNzc5LWVmZjAtNTEzOC1iOGFiLWI3YzFhZGYxNDEzMiIsImNyZWF0ZWQiOjE2NTMwNTg2ODk0OTUsImV4aXN0aW5nIjp0cnVlfQ==',
    'kjb_signin_id': 'd5e12466-98c7-4984-a789-a1e7df43f124',
    'kjb_app_fmarketing': 'vip%40fasterwaytofatloss.com%7CPro+Monthly+%2B+Access%7Chome_trial_growth',
    '_pin_unauth': 'dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA',
    'ajs_user_id': '258278909666892368587741315999637852220',
    'ajs_anonymous_id': '24bcca18-dfa0-44cf-b33d-bad2135cd171',
    '_gid': 'GA1.2.861677027.1654614261',
    '_vis_opt_s': '2%7C',
    '_vis_opt_test_cookie': '1',
    '__hssrc': '1',
    '__cfruid': 'be4707f34b6ffd42bacec94fa34dcff6d8dcb453-1654614263',
    '_kjb_ua_components': '33e07560e858fe73042eb0b50b056baf',
    '_hjSessionUser_1925747': 'eyJpZCI6IjMxYTBkMDEzLTViMDYtNWZlYy1hOTEyLWViMTEyMDZkODE2NSIsImNyZWF0ZWQiOjE2NTQ2MTU4MDg1NDUsImV4aXN0aW5nIjp0cnVlfQ==',
    'tatari-session-cookie': 'f642e9bc-6e85-65f3-708c-5cea22b2ad01',
    '_vwo_ds': '3%3At_0%2Ca_0%3A0%241653058686%3A47.10241406%3A%3A41_0%2C38_0%2C10_0%2C7_0%2C6_0%3A363_0%2C255_0%2C129_0%2C124_0%3A0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Jun+07+2022+19%3A52%3A44+GMT-0500+(hora+est%C3%A1ndar+de+Per%C3%BA)&version=6.35.0&isIABGlobal=false&hosts=&consentId=63d46b73-9f3b-4951-997c-89acc478393a&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&geolocation=PE%3BLMA&AwaitingReconsent=false',
    '_derived_epik': 'dj0yJnU9aURFRWh2cXFEcFc3cHdIZXNGbzc0N1dlZzNobThKY0wmbj1DSjRUbjlaRHBIQmZMMFhNMnpxYmxRJm09MSZ0PUFBQUFBR0tmOHRzJnJtPTEmcnQ9QUFBQUFHS2Y4dHM',
    '_kjb_session': 'f516c919167d561e19c178440bb4018d',
    'ab.storage.sessionId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%22f7919484-e113-525e-47a5-fea2d0d218ec%22%2C%22e%22%3A1654727962587%2C%22c%22%3A1654726162590%2C%22l%22%3A1654726162590%7D',
    'ab.storage.deviceId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%2243104d41-1cc3-64dc-6ced-b0667655160c%22%2C%22c%22%3A1653058688943%2C%22l%22%3A1654726162591%7D',
    'ab.storage.userId.943f47b8-3716-428e-a125-ac9a054f1501': '%7B%22g%22%3A%22258278909666892368587741315999637852220%22%2C%22c%22%3A1654177606358%2C%22l%22%3A1654726162592%7D',
    '__zlcmid': '10fjVdCvDZh26zO',
    '_clck': 'hvcyev|1|f28|0',
    '_sp_ses.5a96': '*',
    '_hjSession_2946942': 'eyJpZCI6IjhkZmQ2YzAyLTdmMzctNDM3Mi1iY2M3LWI3NjdmZGM0MmFiNCIsImNyZWF0ZWQiOjE2NTQ5MDYzMTcyMTUsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjIncludedInSessionSample': '0',
    '_hjAbsoluteSessionInProgress': '0',
    '__hstc': '223412292.a20b697c912dabace88f78b6887d89ca.1653058690021.1654887792030.1654906319225.20',
    't-ip': '1',
    '_uetsid': '1c7e69d0e67311eca36723fbfea95933',
    '_uetvid': '71afa620e27a11ec9f06398f70b0d565',
    'outbrain_cid_fetch': 'true',
    '__hssc': '223412292.6.1654906319225',
    '_clsk': '8rrz84|1654906956585|7|1|www.clarity.ms/eus2-e/collect',
    '_gat_UA-149652847-1': '1',
    '__cf_bm': 's3Boreaglovedkrk4jM7b.wFM3_XSR4kAVL.LaieAB0-1654907249-0-AWln8PppzP1VgJddofNiySyoAEJG3HZuYbG1g2FPc1tLzt6wcczSzIo7qxv3bINcXVAmvorWVQTOJAdzOqoF3eM=',
    '_dd_s': 'rum=1&id=7486a017-61e0-4f5e-80a5-1cc1146c4668&created=1654906312750&expire=1654908150591',
    '_gat': '1',
    'amp_d4cd2a': '2VXRywwNWz5zLHKVBgOP4N.Njg0NTk=..1g581kpre.1g582hadk.0.3n.3n',
    '_sp_id.5a96': '2c2e2b45-4946-43e3-98ab-ec556fcfbbdb.1653059660.20.1654907251.1654887791.e0a164d9-a82e-4f82-97c2-e2ad3708fb19',
    '_ga_5R3LGJJD0H': 'GS1.1.1654906316.17.1.1654907251.0',
    '_ga': 'GA1.1.277638690.1653059660',
    'tatari-cookie-test': '22559799',
    '_derived_epik': 'dj0yJnU9WGhxdm9POVFCbk1ZXzg1Z3NnWmhqck1ISDRYUVlrejkmbj05ZnRCNFV4WHNiVWpqYWxKeFhSN1pnJm09MSZ0PUFBQUFBR0tqNFhJJnJtPTEmcnQ9QUFBQUFHS2o0WEk',
    '__atuvc': '21%7C22%2C98%7C23',
    '__atuvs': '62a3ddcce44c0e97006',
}

api_headers = {
    'authority': 'app.kajabi.com',
    'accept': 'application/json',
    'accept-language': 'es-PE,es-419;q=0.9,es;q=0.8,en;q=0.7',
    'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJlbWFpbCI6InZpcEBmYXN0ZXJ3YXl0b2ZhdGxvc3MuY29tIiwiaWQiOjY4NDU5LCJleHAiOjE2NTQ5OTM2NDl9.d_jvshF31u9UC-CKO5P9UqqX5CZN0dp5SkhsHUbhnnXBw2aR-8XH-pHGwsXPm095bn2qZr15FKVPLPwbGRbslQ',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_gcl_au=1.1.96861702.1653058689; _vwo_uuid_v2=DBE4263CD03763B77C98443DD0244C8A2|44b685ea5444cee5efbe5adbeb8c02ad; _vwo_uuid=DBE4263CD03763B77C98443DD0244C8A2; OptanonAlertBoxClosed=2022-05-20T15:14:19.933Z; _rdt_uuid=1653059660174.488f2495-4859-4a38-aed3-f6f53bc10a04; _fbp=fb.1.1653059660194.982904317; hubspotutk=a20b697c912dabace88f78b6887d89ca; _pin_unauth=dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA; rbuid=rbos-7565073a-6ce9-472b-89b5-9f214626655d; _hjSessionUser_2946942=eyJpZCI6ImM0M2IzNzc5LWVmZjAtNTEzOC1iOGFiLWI3YzFhZGYxNDEzMiIsImNyZWF0ZWQiOjE2NTMwNTg2ODk0OTUsImV4aXN0aW5nIjp0cnVlfQ==; kjb_signin_id=d5e12466-98c7-4984-a789-a1e7df43f124; kjb_app_fmarketing=vip%40fasterwaytofatloss.com%7CPro+Monthly+%2B+Access%7Chome_trial_growth; _pin_unauth=dWlkPVpUa3pZVGs1WTJVdE56TmpOeTAwTXprekxXSXpOR1l0TWpRM1lUVXlOMk0yWTJNNA; ajs_user_id=258278909666892368587741315999637852220; ajs_anonymous_id=24bcca18-dfa0-44cf-b33d-bad2135cd171; _gid=GA1.2.861677027.1654614261; _vis_opt_s=2%7C; _vis_opt_test_cookie=1; __hssrc=1; __cfruid=be4707f34b6ffd42bacec94fa34dcff6d8dcb453-1654614263; _kjb_ua_components=33e07560e858fe73042eb0b50b056baf; _hjSessionUser_1925747=eyJpZCI6IjMxYTBkMDEzLTViMDYtNWZlYy1hOTEyLWViMTEyMDZkODE2NSIsImNyZWF0ZWQiOjE2NTQ2MTU4MDg1NDUsImV4aXN0aW5nIjp0cnVlfQ==; tatari-session-cookie=f642e9bc-6e85-65f3-708c-5cea22b2ad01; _vwo_ds=3%3At_0%2Ca_0%3A0%241653058686%3A47.10241406%3A%3A41_0%2C38_0%2C10_0%2C7_0%2C6_0%3A363_0%2C255_0%2C129_0%2C124_0%3A0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+07+2022+19%3A52%3A44+GMT-0500+(hora+est%C3%A1ndar+de+Per%C3%BA)&version=6.35.0&isIABGlobal=false&hosts=&consentId=63d46b73-9f3b-4951-997c-89acc478393a&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1&geolocation=PE%3BLMA&AwaitingReconsent=false; _derived_epik=dj0yJnU9aURFRWh2cXFEcFc3cHdIZXNGbzc0N1dlZzNobThKY0wmbj1DSjRUbjlaRHBIQmZMMFhNMnpxYmxRJm09MSZ0PUFBQUFBR0tmOHRzJnJtPTEmcnQ9QUFBQUFHS2Y4dHM; _kjb_session=f516c919167d561e19c178440bb4018d; ab.storage.sessionId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%22f7919484-e113-525e-47a5-fea2d0d218ec%22%2C%22e%22%3A1654727962587%2C%22c%22%3A1654726162590%2C%22l%22%3A1654726162590%7D; ab.storage.deviceId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%2243104d41-1cc3-64dc-6ced-b0667655160c%22%2C%22c%22%3A1653058688943%2C%22l%22%3A1654726162591%7D; ab.storage.userId.943f47b8-3716-428e-a125-ac9a054f1501=%7B%22g%22%3A%22258278909666892368587741315999637852220%22%2C%22c%22%3A1654177606358%2C%22l%22%3A1654726162592%7D; __zlcmid=10fjVdCvDZh26zO; _clck=hvcyev|1|f28|0; _sp_ses.5a96=*; _hjSession_2946942=eyJpZCI6IjhkZmQ2YzAyLTdmMzctNDM3Mi1iY2M3LWI3NjdmZGM0MmFiNCIsImNyZWF0ZWQiOjE2NTQ5MDYzMTcyMTUsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInSessionSample=0; _hjAbsoluteSessionInProgress=0; __hstc=223412292.a20b697c912dabace88f78b6887d89ca.1653058690021.1654887792030.1654906319225.20; t-ip=1; _uetsid=1c7e69d0e67311eca36723fbfea95933; _uetvid=71afa620e27a11ec9f06398f70b0d565; outbrain_cid_fetch=true; __hssc=223412292.6.1654906319225; _clsk=8rrz84|1654906956585|7|1|www.clarity.ms/eus2-e/collect; _gat_UA-149652847-1=1; __cf_bm=s3Boreaglovedkrk4jM7b.wFM3_XSR4kAVL.LaieAB0-1654907249-0-AWln8PppzP1VgJddofNiySyoAEJG3HZuYbG1g2FPc1tLzt6wcczSzIo7qxv3bINcXVAmvorWVQTOJAdzOqoF3eM=; _dd_s=rum=1&id=7486a017-61e0-4f5e-80a5-1cc1146c4668&created=1654906312750&expire=1654908150591; _gat=1; amp_d4cd2a=2VXRywwNWz5zLHKVBgOP4N.Njg0NTk=..1g581kpre.1g582hadk.0.3n.3n; _sp_id.5a96=2c2e2b45-4946-43e3-98ab-ec556fcfbbdb.1653059660.20.1654907251.1654887791.e0a164d9-a82e-4f82-97c2-e2ad3708fb19; _ga_5R3LGJJD0H=GS1.1.1654906316.17.1.1654907251.0; _ga=GA1.1.277638690.1653059660; tatari-cookie-test=22559799; _derived_epik=dj0yJnU9WGhxdm9POVFCbk1ZXzg1Z3NnWmhqck1ISDRYUVlrejkmbj05ZnRCNFV4WHNiVWpqYWxKeFhSN1pnJm09MSZ0PUFBQUFBR0tqNFhJJnJtPTEmcnQ9QUFBQUFHS2o0WEk; __atuvc=21%7C22%2C98%7C23; __atuvs=62a3ddcce44c0e97006',
    'referer': 'https://app.kajabi.com/admin/products/209914',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
    'x-csrf-token': 'TR3jhwCQBPvMT/+UYvnOhvKxOyt/BIXDf67a4GPJTpMYL7/PkqNH4fjscV4/l53HBb6Kq+0oNPUV8NHTxX/TrA==',
}

for x in range(INITIAL_PAGE, PAGES + 1):
    product_response = requests.get(PRODUCT_PAGE + str(x), cookies= page_cookies, headers= page_headers)

    #get the product page
    product_soup = BeautifulSoup(product_response.content, 'html.parser')
    #print(product_soup)

    #get the list of products
    product_detail_anchors = product_soup.find_all("a", class_="sage-link") 
    #iterate each product
    for product_detail_anchor in product_detail_anchors:
        product_id = ''
        product_title = ''
        description = ''
        product_thumbnail = ''
        product_detail_link = product_detail_anchor.get('href')
        product_detail_link = WEBSITE_URL + product_detail_link
        #print('link: ' + product_detail_link)
        product_detail_response = requests.get(product_detail_link, cookies= page_cookies, headers= page_headers)
        product_detail_soup = BeautifulSoup(product_detail_response.content, 'html.parser')
        product_detail_text_in_json = product_detail_soup.find(id="kjb-redux-store-data")
        #print(product_detail_text_in_json)
        if product_detail_text_in_json != None:
            product_detail_json = json.loads(product_detail_text_in_json.get_text())
            if product_detail_json != None:
                #print(product_detail_json)
                if product_detail_json['data']['id'] != None:
                    product_id = product_detail_json['data']['id']
                if product_detail_json['data']['attributes']['title'] != None:
                    product_title = product_detail_json['data']['attributes']['title']
                if product_detail_json['data']['attributes']['description'] != None:
                    product_description = product_detail_json['data']['attributes']['description']
                if product_detail_json['data']['attributes']['thumbnailUrl'] != None:
                    product_thumbnail = product_detail_json['data']['attributes']['thumbnailUrl']
                    print('product_id: ' + product_id)
                    #print('product_title: ' + product_title)
                    #print('product_description: ' + product_description)
                    #print('product_thumbnail: ' + product_thumbnail)
                    # save product entity
                if s.query(ProductModel).filter_by(id=product_id).first() is None:
                    product_model = ProductModel (
                        id = product_id,
                        title = product_title,
                        description = product_description,
                        thumbnail = product_thumbnail,
                        json_data = product_detail_json,
                        created_by = CREATED_BY,
                    )
                    s.add(product_model)
                    s.commit()

                if product_id != '':

                    #get categories
                    categories_url = API_URL_BASE + product_id + '/categories'
                    category_response = requests.get(categories_url, cookies= api_cookies, headers= api_headers)
                    category_json = category_response.json()
                    if category_json['data'] != None:
                        #print(type(category_json))
                        #print(category_json)
                        #iterate each category
                        for category in category_json['data']:
                            category_id = ''
                            category_title = ''
                            category_description = ''
                            category_poster_image_url = ''
                            if category['id'] != None:
                                category_id = category['id']
                            if category['attributes']['title'] != None:
                                category_title = category['attributes']['title']
                            if category['attributes']['description'] != None:
                                category_description = category['attributes']['description']
                            if category['attributes']['posterImageUrl'] != None:
                                category_poster_image_url = category['attributes']['posterImageUrl']
                            print('category_id: ' + category_id) 
                            #print('category_title: ' + category_title) 
                            #print('category_description: ' + category_description) 
                            #print('category_poster_image_url: ' + category_poster_image_url)
                            # save category entity
                            if s.query(CategoryModel).filter_by(id=category_id).first() is None:
                                category_model = CategoryModel (
                                    id = category_id,
                                    product_id = product_id,
                                    title = category_title,
                                    description = category_description,
                                    poster_image = category_poster_image_url,
                                    json_data = category,
                                    created_by = CREATED_BY,
                                )
                                s.add(category_model)
                                s.commit()

                    #get posts
                    posts_url = API_URL_BASE + product_id + '/posts'
                    post_response = requests.get(posts_url, cookies= api_cookies, headers= api_headers)
                    post_json = post_response.json()
                    if post_json != None:
                        #print(type(post_json))
                        for post in post_json['data']:
                            post_id = ''
                            post_title = ''
                            post_edit_url = ''
                            post_publishing_status = ''
                            post_category_id = ''
                            post_body = ''
                            post_poster_image_url = ''
                            if post['id'] != None:
                                post_id = post['id']
                            if post['attributes']['title'] != None:
                                post_title = post['attributes']['title']
                            if post['attributes']['urls']['editUrl'] != None:
                                post_edit_url = WEBSITE_URL + post['attributes']['urls']['editUrl']
                            if post['attributes']['publishing']['status'] != None:
                                post_publishing_status = post['attributes']['publishing']['status']
                            if post['relationships']['category']['data']['id'] != None:
                                post_category_id = post['relationships']['category']['data']['id']
                            #get post page 
                            post_response = requests.get(post_edit_url, cookies= page_cookies, headers= page_headers)
                            post_soup = BeautifulSoup(post_response.content, 'html.parser')
                            post_detail_text_in_json = post_soup.find(id="kjb-redux-store-data")
                            if post_detail_text_in_json != None:
                                post_detail_json = json.loads(post_detail_text_in_json.get_text())
                                if post_detail_json['data']['attributes']['body'] != None:
                                    post_body = post_detail_json['data']['attributes']['body']
                                if post_detail_json['data']['attributes']['posterImageUrl'] != None:
                                    post_poster_image_url = post_detail_json['data']['attributes']['posterImageUrl']
                            print('post_id: ' + post_id) 
                            #print('post_title: ' + post_title) 
                            #print('post_edit_url: ' + post_edit_url) 
                            #print('post_publishing_status: ' + post_publishing_status) 
                            #print('post_category_id: ' + post_category_id)
                            #print('post_body: ' + post_body)
                            #print('post_poster_image: ' + post_poster_image_url)
                            # save post entity
                            if s.query(PostModel).filter_by(id=post_id).first() is None:
                                post_model = PostModel (
                                    id = post_id,
                                    category_id = post_category_id,
                                    title = post_title,
                                    publishing_status = post_publishing_status,
                                    body = post_body,
                                    poster_image = post_poster_image_url,
                                    json_data = post,
                                    created_by = CREATED_BY,
                                )
                                s.add(post_model)
                                s.commit()
s.close()

