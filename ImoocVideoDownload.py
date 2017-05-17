from bs4 import BeautifulSoup

from urllib.request import urlopen

import urllib.request

from urllib.error import URLError, HTTPError

import json

import re

import os

from builtins import type


import pdfkit
# 获取url的内容


def get_url_content(url):

    html = urllib.request.urlopen(url)
      
    content = html.read()
    
#     print(html.getcode())

    html.close()

    return content
    

##获取课程列表

i=1

print ('增强版慕课网教程爬虫，支持下载非视频类的教程，保存称PDF文件')

print('输入课程编号，如http://www.imooc.com/learn/177，输入177即可')

while True:   
           
        ##获取课程的内容
        
        chapter_address = input('输入课程地址(输入exit退出)：')

        if(chapter_address == 'exit'):

            break
        
        course_url = "http://www.imooc.com/learn/" + chapter_address.strip()
                 
        try:               
            
            soup = BeautifulSoup(get_url_content(course_url).decode('utf-8'),"html.parser")
            
            video_count = 0
        
            item_count = 0        
         
            course_name = soup.find('div',class_="hd clearfix")
            
            print(course_name.get_text())
            
            video_path = os.path.abspath('.') + '/' + course_name.get_text().strip() + '/'
                    
            if not os.path.isdir(video_path):
                        
                os.mkdir(video_path)
            
            file_name = course_name.get_text().strip()      ##保存文件的文件名，文件名不能有\/?<>""，所有先将这些字符替换掉，否则保存成文件的时候会出错
            
            if '/' in file_name:
                
                file_name = course_name.get_text().strip().replace('/','&')
                
            if '\"' in file_name:
                
                file_name = course_name.get_text().strip().replace('\"','“')
    
            if not os.path.isdir('Imooc/'):                      ##如果当前目录不存在，创建文件夹
                
                os.mkdir('Imooc/')
                
            output_file = open('Imooc/'+file_name+'.txt', 'w')         ##将课程的名称及学习地址保存程一个文件
            
            chapter_names = soup.find_all('div',class_="chapter")
            
            for chapter_name in chapter_names:
                
# print(chapter_name.find('strong').get_text().split()[0]+' ' +chapter_name.find('strong').get_text().split()[1])
                
                output_file.write(chapter_name.find('strong').get_text().split()[0]+' ' +chapter_name.find('strong').get_text().split()[1]+'\r\n')
                
                class_links = chapter_name.find_all('a',href=re.compile(r"\d"),class_="J-media-item")
                
                for class_link in class_links:
                    
# print(' '.join(class_link.get_text().strip().split()[0:len(class_link.get_text().strip().split())-1]),
# 'http://www.imooc.com'+class_link['href'])      ##使用split()函数分割字符串，默认使用空格、换行符、制表符分割，并返回一个列表（列表最后一个元素不需要）
                    
                    output_file.write(' '.join(class_link.get_text().strip().split()[0:len(class_link.get_text().strip().split())-1])+'>'+'http://www.imooc.com'+class_link['href']+'\r\n')     ##join()函数将列表转换成String
                    
                    if "video" in class_link['href']:       ##用于统计课程有几个视频
                        
                        video_count = video_count + 1
                        
                    item_count = item_count + 1             ##用于统计课程有几个学习内容（有的课程不是视频教程）
                    
            print('共' + str(video_count) + '个视频')
            
            print('共' + str(item_count) + '个学习内容','\r\n\r\n')
            
            output_file.close()
            
            video_info_file = open('Imooc/'+file_name+'.txt', 'r')
    
            info_data = video_info_file.readlines()
            
            for temp in info_data:

                if 'code' in temp:  ##保存不是视频的教程到pdf

                    # print(temp)

                    file_name = temp.split('>')[0].replace(':','：')

                    code_link = temp.split('>')[1]

                    code_content = BeautifulSoup(urllib.request.urlopen(code_link).read().decode('utf-8'),"html.parser")

                    code_content.find('div',class_="code-panel")

                    print(code_content.find('div',class_="code-panel"))

                    options = {
                        # 定义编码类型，防止中文出现乱码
                        'encoding': "UTF-8"
                    }
                    # config = pdfkit.configuration(
                        # wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe')

                    pdfkit.from_string(
                        str(code_content.find('div',class_="code-panel")), file_name +'.pdf', options=options)

                    type(urllib.request.urlopen(code_link).read())

                elif 'video' in temp:     ##处理文件名，文件名的合法性检查
                    
                    video_name = temp.split('>')[0].replace(':','：')
            
                    video_link = temp.split('>')[1]
            
                    video_id = video_link.split('/')[len(video_link.split('/'))-1]
            
                    print(video_name,video_link)
            
            ##        url="http://www.imooc.com/course/ajaxmediainfo/?mid=0000&mode=flash"    ##用0000替换视频地址的编号
                    
                    url="http://www.imooc.com/course/ajaxmediainfo/?mid=" + video_id.strip() +  "&mode=flash"    ##用0000替换视频地址的编号
            
    #                 response=urllib.request.urlopen(url)    #返回文件对象
    #           
    #                 page=response.read()
    #           
    #                 response.close()
                    
                    #直接将Json数据保存为本地文件：
            
                    output_file = open("Imooc视频Json数据.txt", 'w')
            
                    output_file.write(bytes.decode(get_url_content(url)))
            
                    output_file.close()
            
                    input_file = open("Imooc视频Json数据.txt", 'r')
            
                    video_info = input_file.read()

                    # print(type(video_info))                 ##返回值为Str

                    ##使用正则表达式获取视频地址

                    video_down_link = re.compile(r'http.+auth_key=\S{47}')

                    print(video_down_link.findall(video_info))  ##注意findall与search的区别，findall返回所有符合条件的值，返回类型为List，search返回第一个符合条件的值，返回类型为Match

                    ##
            
                    video_link = json.loads(video_info)     ##返回值为dict
            
            ##        print(type(video_link))
            
                    '''Json数据格式
                    {
                        "result": 0,
                        "data": {
                            "result": {
                                "mid": 3510,
                                "mpath": [
                                    "http://v2.mukewang.com/d51dbce1-b075-4558-b1b3-bfb4fcc5ee0a/L.mp4?auth_key=1480781145-0-0-32089e0973914437dc19596d2cc552c8",
                                    "http://v2.mukewang.com/d51dbce1-b075-4558-b1b3-bfb4fcc5ee0a/M.mp4?auth_key=1480781145-0-0-4d0a14128facb64e0f94bba9419ce7a4",
                                    "http://v2.mukewang.com/d51dbce1-b075-4558-b1b3-bfb4fcc5ee0a/H.mp4?auth_key=1480781145-0-0-68c1c5dbdd7540020065c030842843d8"
                                ],
                                "cpid": "918",
                                "name": "WAMPServer集成环境下载和安装",
                                "time": 0,
                                "practise": []
                            }
                        },
                        "msg": "成功"
                    }
                    '''
                    ##video_link，video_link['data']，video_link['data']['result']对应的均为dict，video_link['data']['result']['mpath']对应的是list
            
#                     print(type(video_link['data']['result']['mpath']))
                    
                    print(video_link['data']['result']['mpath'][len(video_link['data']['result']['mpath'])-1])
                            
                    urllib.request.urlretrieve(video_link['data']['result']['mpath'][len(video_link['data']['result']['mpath'])-1],video_path + video_name.split()[0] + ' ' +  video_link['data']['result']['name'] + '.mp4')     ##默认下载高清视频
            
                    ##print(type(video_link['data']['result']['mpath'][len(video_link['data']['result']['mpath'])-1]))
            
                    input_file.close()
                else:
                    # print(urllib.request.urlopen(temp).read())
                    pass
            
        except HTTPError as e:
            
            print('没有这个课程，请输入正确的编号···')            
             
        

    
        



