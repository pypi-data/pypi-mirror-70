import re
import logging


正則組 = {
    '^> *(?P<原文>(?P<函數>\S*)(?P<參數表>(.*)))$': {
        '類型': '函數調用',
        '子樹': {
            '參數表': {
                '(?P<a>(((?<=").*?(?="))|(((?<= )|(?<=^))([^" ]+?)(?=( |$)))))': None
            }
        }
    },
    '^```(?P<代碼類型>.*?)\\n((?P<代碼內容>(.|\\n)*?)\\n)?```$': {
        '類型': '插入代碼'
    },
    '^@ *(?P<人物名>.+?) *(?P<操作符>[\\+\\|]) *(?P<目標>.+?)$': {
        '類型': '人物操作'
    },
    '^={3,} *(?P<插入圖>.*) *$': {
        '類型': '插入圖',
    },
    '^(?=[^#])(?P<名>.+?)(\|(?P<代>.+?))? +(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\))? *[「“"](?P<語>(.|\\n)*?)["”」] *$': {
        '類型': '人物對話',
    },
    '^(?P<名>.+?)(\|(?P<代>.+?))? +(\[(?P<特效>.+?)\])? *(\((?P<顏>.+?)\)) *$': {
        '類型': '人物表情',
    },
    '^(?P<鏡頭符號>[\\+\\-]) *(?P<內容>.*)$': {
        '類型': '鏡頭',
    },
    '^\? +(?P<選項名>.+?) *-> *(?P<文件>.+?)(, *(?P<位置>.*?))?$': {
        '類型': '選項'
    },
    '^#(?P<註釋>.*)$': {
        '類型': '註釋',
    },
    '^\\* *(?P<躍點>.*)$': {
        '類型': '躍點'
    },
}
續行組 = {
    r'^(?P<有效字>(.|\n)*)\\$',
    '^(?=[^#])(.+?)(\|(.+?))? +(\[(?P<特效>.+?)\])? *(\((.+?)\))?「([^」]*)$',
    r'^```(.|\n)*(?<!\n```)$',
}
錯誤組 = {
    '^.*?「[^」]*「.*$':
        '引號不匹配',
}


class parse_error(Exception):
    pass


def 遞歸re(s, start=正則組):
    d = []
    for i in start:
        單位 = re.finditer(i, s)
        for j in 單位:
            gd = j.groupdict()
            d.append(gd)
            if isinstance(start[i], dict):
                gd['類型'] = start[i]['類型']
            if start[i] is not None and '子樹' in start[i]:
                for k in start[i]['子樹']:
                    gd[k] = 遞歸re(gd[k], start[i]['子樹'][k])
    return d


def 加載(x):
    import _io
    if type(x) is _io.TextIOWrapper:
        全文 = x.read()
    else:
        全文 = x
    行組 = 全文.split('\n')
    while 行組 and 行組[-1] == '':
        行組 = 行組[:-1]
    return 行組解析(行組)


def 行組解析(行組):
    全 = []
    多行緩衝 = ''
    for 當前行 in iter(行組):
        if not re.search('\\S', 當前行):
            if 全:
                全[-1]['之後的空白'] = 全[-1].get('之後的空白', 0) + 1
            continue

        當前行 = 當前行.rstrip('\r').rstrip('\n')
        
        if 多行緩衝:
            當前行 = 多行緩衝 + '\n' + 當前行
            多行緩衝 = ''
        for 規則 in 續行組:
            t = re.match(規則, 當前行)
            if t:
                if '有效字' in t.groupdict():
                    多行緩衝 = t.groupdict()['有效字']
                else:
                    多行緩衝 = 當前行
                logging.debug(多行緩衝)
                break
        if t:
            continue

        自 = {}
        自['縮進數'] = len(當前行) - len(當前行.lstrip(' '))

        當前行 = 當前行.lstrip(' ').rstrip(' ')
        for 表達式, 信息 in 錯誤組.items():
            if re.match(表達式, 當前行):
                raise parse_error(f'『{當前行}』有語法錯誤——{信息}。')
        d = 遞歸re(當前行)
        if not d:
            d.append({'類型': '旁白', '旁白': 當前行})
        if len(d) > 1:
            raise parse_error(f'『{當前行}』匹配過多，有可能是【{"，".join([i["類型"] for i in d])}】')
        自.update(d[0])
        全.append(自)
    return 全


load = 加載
