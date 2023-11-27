import json
import configparser
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models



class TenApi:
    params = 0;
    def __init__(self):
        #读取配置文件
        config=configparser.ConfigParser()
        config.read("./key.ini")
        self.TenApi_ID = config.get("Tencent_cloud","ipSecretId")
        self.TenApi_Key = config.get("Tencent_cloud","SecretKey")
        self.params = {
                "SourceText": "",
                "Source": "en",
                "Target": "zh",
                "ProjectId": 0,
                "UntranslatedText": ""
        }

    def translation(self,text ,Source = "en",Target = "zh"):
        self.params["SourceText"] = text
        self.params["Source"] = Source
        self.params["Target"] = Target
        newtext =''
        try:
            cred = credential.Credential(self.TenApi_ID, self.TenApi_Key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tmt_client.TmtClient(cred, "ap-chengdu", clientProfile)

            req = models.TextTranslateRequest()

            req.from_json_string(json.dumps(self.params))

        # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
            resp = client.TextTranslate(req)
            # 输出json格式的字符串回包
            newtext = resp.to_json_string()
            return newtext

        except TencentCloudSDKException as err:
            newtext = err.get_message()
            print(newtext)
