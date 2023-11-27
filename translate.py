
from tenApi import *
from tenOrc import *

class Translate:
    Source = 0
    Target = 0
    tenApi = TenApi()
    #如果有其他翻译在这里添加
    def Totranslate(self, text,Source, Target):
        newtext = " "
        # 腾讯翻译
        newtext = self.tenApi.translation(text,Source,Target)
        # 将字符串转换为JSON对象
        json_data = json.loads(newtext)
        return json_data["TargetText"]
