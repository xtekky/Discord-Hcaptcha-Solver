from tls_client         import Session
from requests           import post
from datetime           import datetime
from json               import dumps
from subprocess         import check_output
from threading          import Thread, current_thread
from time               import sleep

import random

openai_key = 'sk-xxx'

class Hcaptcha:
    def __init__(this, sitekey: str, host: str, proxy: str = None):

        this.client         = Session(client_identifier = 'chrome110')
        this.client.headers = {
            "host"               : "hcaptcha.com",
            "connection"         : "keep-alive",
            "sec-ch-ua"          : "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
            "accept"             : "application/json",
            "sec-ch-ua-mobile"   : "?0",
            "user-agent"         : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "sec-ch-ua-platform" : "\"Windows\"",
            "origin"             : "https://newassets.hcaptcha.com",
            "sec-fetch-site"     : "same-site",
            "sec-fetch-mode"     : "cors",
            "sec-fetch-dest"     : "empty",
            "referer"            : "https://newassets.hcaptcha.com/",
            "accept-encoding"    : "gzip, deflate, br",
            "accept-language"    : "en-US,en;q=0.9"
        }

        # api_js              = this.client.get('https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad').text
        this.config         = {
            'v'       : '7d69057', #findall(r'v1\/([A-Za-z0-9]+)\/static', api_js)[1],
            'sitekey' : sitekey,
            'host'    : host
        }
        
        this.client.proxies = {
            'http' : f'http://{proxy}',
            'https': f'http://{proxy}' } if proxy else None
    
    def get_captchas(this) -> dict:
        checksiteconfig = this.client.post(f"https://hcaptcha.com/checksiteconfig", params = (this.config | {
            'sc'      : '1',
            'swa'     : '1' })).json()

        getcaptcha = this.client.post(f"https://hcaptcha.com/getcaptcha/{this.config['sitekey']}", data = (this.config | {
            'hl'         : 'en',
            'motionData' : this.motion_data(),
            'n'          : this.hsw(checksiteconfig['c']['req']),
            'c'          : dumps(checksiteconfig['c']) })).json()
        
        return this.client.post(f"https://hcaptcha.com/getcaptcha/{this.config['sitekey']}", data = (this.config | {
            'hl'        : 'en',
            'a11y_tfe'  : 'true',
            'action'    : 'challenge-refresh',
            'old_ekey'  : getcaptcha['key'],
            'extraData' : getcaptcha,
            'motionData': this.motion_data(), 
            'n'         : this.hsw(getcaptcha['c']['req']),        
            'c'         : dumps(getcaptcha['c'])})).json()
        
    def motion_data(this) -> str:
            return "{\"st\":1662999253604,\"dct\":1662999253604,\"mm\":[[249,206,1662999326866],[234,163,1662999326894],[221,142,1662999326920],[214,139,1662999326946],[209,141,1662999326974],[202,149,1662999327000],[194,157,1662999327026],[189,160,1662999327053],[187,160,1662999327080],[185,159,1662999327106],[181,151,1662999327134],[177,140,1662999327160],[175,131,1662999327186],[174,127,1662999327214],[173,124,1662999327265],[172,125,1662999327634],[170,127,1662999327653],[168,129,1662999327680],[166,130,1662999327707],[164,130,1662999327746],[164,131,1662999327854],[163,133,1662999327880],[162,135,1662999327907],[162,138,1662999327934],[162,141,1662999327960],[163,144,1662999327987],[165,147,1662999328014],[170,151,1662999328040],[179,157,1662999328067],[190,161,1662999328094],[198,165,1662999328120],[205,167,1662999328147],[209,167,1662999328174],[212,167,1662999328200],[214,167,1662999328228],[215,166,1662999328253],[218,166,1662999328280],[220,165,1662999328307],[222,165,1662999328334],[225,165,1662999328360],[229,166,1662999328388],[236,170,1662999328414],[244,175,1662999328440],[249,178,1662999328467],[251,178,1662999328494],[251,177,1662999328736],[249,174,1662999328761],[246,170,1662999328787],[242,166,1662999328813],[238,161,1662999328841],[234,156,1662999328867],[231,154,1662999328893],[229,151,1662999328920],[226,147,1662999328947],[221,141,1662999328974],[214,134,1662999329001],[208,128,1662999329027],[204,124,1662999329054],[201,122,1662999329081],[202,122,1662999329343],[207,125,1662999329361],[219,131,1662999329387],[234,139,1662999329414],[248,147,1662999329440],[258,153,1662999329468],[260,155,1662999329494],[261,156,1662999329520],[261,159,1662999329548],[262,161,1662999329574],[262,162,1662999329601],[262,163,1662999329702],[262,164,1662999329721],[262,166,1662999329748],[263,169,1662999329788],[263,171,1662999329851],[264,172,1662999329881],[265,174,1662999329921],[266,175,1662999329948],[267,176,1662999329975],[269,178,1662999330001],[270,179,1662999330025],[269,179,1662999330255],[266,178,1662999330281],[262,177,1662999330307],[259,175,1662999330334],[255,173,1662999330361],[249,168,1662999330388],[243,162,1662999330414],[238,156,1662999330441],[235,152,1662999330467],[234,151,1662999330495],[235,151,1662999330593],[238,151,1662999330614],[247,154,1662999330641],[254,158,1662999330668],[261,162,1662999330694],[265,165,1662999330721],[266,168,1662999330748],[268,171,1662999330775],[269,174,1662999330802],[272,176,1662999330828],[273,178,1662999330854],[275,178,1662999330931]],\"mm-mp\":22.28095238095237,\"md\":[[173,124,1662999327280],[251,178,1662999328537],[270,179,1662999330025],[275,178,1662999330990]],\"md-mp\":1236.6666666666667,\"mu\":[[173,124,1662999327413],[251,178,1662999328655],[270,179,1662999330166],[275,178,1662999331088]],\"mu-mp\":1225,\"kd\":[[83,1662999327818],[65,1662999327841],[68,1662999327963],[68,1662999329203],[65,1662999329359],[68,1662999329572],[68,1662999330532],[65,1662999330621],[83,1662999330643]],\"kd-mp\":313.8888888888889,\"ku\":[[83,1662999328019],[68,1662999328243],[68,1662999329449],[65,1662999329584],[83,1662999329605],[68,1662999329772],[68,1662999330823],[65,1662999330867]],\"ku-mp\":317.6666666666667,\"topLevel\":{\"st\":1662999246905,\"sc\":{\"availWidth\":1920,\"availHeight\":1050,\"width\":1920,\"height\":1080,\"colorDepth\":24,\"pixelDepth\":24,\"top\":0,\"left\":0,\"availTop\":0,\"availLeft\":0,\"mozOrientation\":\"landscape-primary\",\"onmozorientationchange\":null},\"nv\":{\"permissions\":{},\"pdfViewerEnabled\":true,\"doNotTrack\":\"1\",\"maxTouchPoints\":0,\"mediaCapabilities\":{},\"oscpu\":\"Windows NT 10.0; Win64; x64\",\"vendor\":\"\",\"vendorSub\":\"\",\"productSub\":\"20100101\",\"cookieEnabled\":true,\"buildID\":\"20181001000000\",\"mediaDevices\":{},\"serviceWorker\":{},\"credentials\":{},\"clipboard\":{},\"mediaSession\":{},\"webdriver\":false,\"hardwareConcurrency\":12,\"geolocation\":{},\"appCodeName\":\"Mozilla\",\"appName\":\"Netscape\",\"appVersion\":\"5.0 (Windows)\",\"platform\":\"Win32\",\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0\",\"product\":\"Gecko\",\"language\":\"en-US\",\"languages\":[\"en-US\",\"en\"],\"locks\":{},\"onLine\":true,\"storage\":{},\"plugins\":[\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\",\"internal-pdf-viewer\"]},\"dr\":\"\",\"inv\":false,\"exec\":false,\"wn\":[],\"wn-mp\":450.51612903225805,\"xy\":[],\"xy-mp\":0,\"mm\":[[568,779,1662999326734],[517,755,1662999326760],[468,720,1662999326787],[428,674,1662999326813],[400,627,1662999326840],[385,577,1662999326864]],\"mm-mp\":82.32692307692308},\"v\":1}".replace('1662739', str(round(datetime.now().timestamp()))[:7])

    def hsw(self, req: str) -> str:
        return check_output(["node", './hsw.js', req]).decode('utf-8').strip()

    def solve_text(self, task):
        question = task["datapoint_text"]["en"]
        
        response = post('https://api.openai.com/v1/chat/completions', headers = {'Authorization': f'Bearer {openai_key}'}, 
            json = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'user',
                        'content': f'srictly respond yes | no: {question}',
                    }
                ],
                'temperature': 0
            }
        )
        
        if 'yes' in response.json()["choices"][0]['message']["content"].lower():
            print(f'yes: {question}')
            current_thread().return_value =  (task['task_key'], {'text': 'yes'})
            
        else:
            print(f'no: {question}')
            current_thread().return_value =  (task['task_key'], {'text': 'no'})

def solve(key, host, proxy):
    try:
        hcap = Hcaptcha(key, host, proxy)
        data = hcap.get_captchas()
        
        threads = [Thread(target=hcap.solve_text, args=[task]) for task in data['tasklist']]

        for thread in threads: thread.start()
        for thread in threads: thread.join()
        
        answers = {
                    a:b for a,b in [
                        th.return_value for th in threads
                    ]
                }
        
        print(answers)
        
        sleep(0.8); checkcaptcha = hcap.client.post(f"https://hcaptcha.com:443/checkcaptcha/{hcap.config['sitekey']}/{data['key']}", json = {
                'answers'       : answers,
                'c'             : dumps(data['c']),
                'job_mode'      : 'text_free_entry',
                'motionData'    : hcap.motion_data(), #dumps(MotionData.generate(solution)),
                'n'             : hcap.hsw(data['c']['req']),
                'serverdomain'  : hcap.config['host'],
                'sitekey'       : hcap.config['sitekey'],
                'v'             : hcap.config['v'],
        })
        
        if 'UUID' in checkcaptcha.text:
            print('solved', checkcaptcha.json()['generated_pass_UUID'][-100:])
            return checkcaptcha.json()['generated_pass_UUID']
        else:
            print('failed')
            return False
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    token = solve('4c672d35-0701-42b2-88c3-78380b0db560', 'discord.com', 'https proxy')
    print(token)
