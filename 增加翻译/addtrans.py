#!/usr/bin/env python3
# encoding: utf-8
import os
import collections
import ipdb
import codecs
import opencc
import translater


def main():
    base = os.getcwd()
    locale_CN = None
    locale_TW = None
    locale_EN = None
    for file in os.listdir(base):
        if file.endswith('zh_CN.properties'):
            locale_CN = file
            continue
        if file.endswith('zh_TW.properties'):
            locale_TW = file
            continue
        if file.endswith('en_US.properties'):
            locale_EN = file
            continue
    if not locale_CN or not locale_TW or not locale_EN:
        print('没有找到对应的国际化文件，请检查！')
        return

    map_CN = get_kvmap_in_locale_file(locale_CN)


    process_TW(map_CN, locale_TW)
    process_EN(map_CN, locale_EN)


def process_EN(map_CN, locale_EN):
    # 处理英文翻译
    map_EN = get_kvmap_in_locale_file(locale_EN)
    error_keys = []
    result_EN = ''
    for k, v in map_EN.items():
        if not v and map_CN[k]:
            try:
                v_CN = codecs.decode(map_CN[k], 'unicode_escape')
                v = translater.zh2en(v_CN)
                print(k, v_CN, v)
            except Exception as e:
                print(str(e))
                error_keys.append(k)
        result_EN += k + '=' + v + '\n'
    with open(locale_EN, 'w') as f:
        f.write(result_EN)
    print('请手动处理以下英文key: ')
    for k in error_keys:
        print(k)


def process_TW(map_CN, locale_TW):
    # 处理台湾翻译
    map_TW = get_kvmap_in_locale_file(locale_TW)
    error_keys = []
    result_TW = ''
    for k, v in map_TW.items():
        if not v and map_CN[k]:
            try:
                v_CN = codecs.decode(map_CN[k], 'unicode_escape')
                v_TW = opencc.convert(v_CN, config='s2twp.json')
                v_TW = codecs.encode(v_TW, 'unicode_escape').decode()
                v = v_TW.upper().replace('\\U', '\\u')
            except Exception as e:
                print(str(e))
                error_keys.append(k)
        result_TW += k + '=' + v + '\n'
    with open(locale_TW, 'w') as f:
        f.write(result_TW)
    print('请手动处理以下key: ')
    for k in error_keys:
        print(k)


def get_kvmap_in_locale_file(file):
    kvmap = collections.OrderedDict()
    with open(file) as f:
        content = f.read()
    contentList = content.splitlines()
    for line in contentList:
        # ipdb.set_trace()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            print('!!!\n', line)
        k, v = line.split('=', 1)
        k = k.strip()
        kvmap[k] = v
    return kvmap


if __name__ == "__main__":
    main()
