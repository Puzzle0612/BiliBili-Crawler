"获取所有完结番链接模块"

#引用模块
import requests
import threading
import operator

# 定义全局变量headers
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"
}

#获取完结番剧总页数
def get_total_pages(url,headers=headers):
    response = requests.get(url,headers=headers,timeout=5)
    json_data = response.json()
    page_info = json_data.get("data").get("page")
    total_rows = int(page_info.get("count"))
    page_size = int(page_info.get("size"))

    if(total_rows%page_size==0):
        return total_rows//page_size
    else:
        return total_rows//page_size+1

#获取完结番剧信息的列表总和
def get_video_info_list(start,total_pages,url,headers=headers):
    video_info_list = []
    for i in range(start,total_pages):
        appended_url = url+"&pn="+str(i)
        response = requests.get(appended_url,headers=headers,timeout=5)
        json_data = response.json()
        page_video_info_list = json_data.get("data").get("archives")
        # 获取标签
        for i in page_video_info_list:
            i["tags"] = get_video_tags(i["aid"])
        video_info_list.extend(page_video_info_list)
    return video_info_list

#定义线程
class MyThread(threading.Thread):
    def __init__(self,s,e,url):
        threading.Thread.__init__(self)
        self.s = s
        self.e = e
        self.url = url

    def run(self):
        self.re = get_video_info_list(self.s, self.e, self.url)

    def get_result(self):
            return self.re

#把rank写入记事本
def write_rank_data(video_info_list):
    with open("rank.txt", "a",encoding="utf-8") as file:
        for each in video_info_list[0:49]:
            each_info = []
            each_info.append(each.get("aid"))
            each_info.append(each.get("videos"))
            each_info.append(each.get("title"))
            each_info.append(each.get("play"))
            each_info.append(each.get("create"))
            each_info.append(each.get("author"))
            each_info.append(each.get("favorites"))
            each_info.append(each.get("stat").get("coin"))
            each_info.append(each.get("stat").get("reply"))
            each_info.append(each.get("video_review"))
            each_info.append(each.get("tags"))
            file.write(str(each_info)+"\n")
        file.close()

def write_all_data(video_info_list):
    with open("all.txt", "a", encoding="utf-8") as file:
         for each in video_info_list:
            each_info = []
            each_info.append(each.get("aid"))
            each_info.append(each.get("videos"))
            each_info.append(each.get("title"))
            each_info.append(each.get("play"))
            each_info.append(each.get("create"))
            each_info.append(each.get("author"))
            each_info.append(each.get("favorites"))
            each_info.append(each.get("stat").get("coin"))
            each_info.append(each.get("stat").get("reply"))
            each_info.append(each.get("video_review"))
            each_info.append(each.get("tags"))
            file.write(str(each_info) + "\n")


#写入项目属性名
def write_column_name(file_name):
    with open(file_name, "w",encoding="utf-8") as file:
        column_name_list = ["番号", "集数", "名字", "播放量", "投稿时间", "作者", "收藏数", "硬币数", "评论数","弹幕数","标签"]
        file.write(str(column_name_list)+'\n')

#获取标签
def get_video_tags(aid):
    get_tags_url =  "https://api.bilibili.com/x/tag/archive/tags?aid="+str(aid)
    response = requests.get(get_tags_url,headers=headers,timeout=5)
    json_data = response.json()
    tag_list = json_data.get("data")
    if(tag_list):
        tags = []
        for i in tag_list:
            tags.append(i.get("tag_name"))
        return tags
    return []



#主函数
if __name__=="__main__":
    get_pages_url = "https://api.bilibili.com/archive_rank/getarchiverankbypartion?tid=32"
    total_pages = get_total_pages(get_pages_url)
    get_video_list_url = "https://api.bilibili.com/archive_rank/getarchiverankbypartion?tid=32"
    #建立线程
    t1 = MyThread(1, 200, get_video_list_url)
    t2 = MyThread(201, 400, get_video_list_url)
    t3 = MyThread(601, total_pages, get_video_list_url)
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    video_info_list = []
    video_info_list.extend(t1.get_result())
    video_info_list.extend(t2.get_result())
    video_info_list.extend(t3.get_result())
    print(len(video_info_list))
    right_video_info_list = []
    for j in video_info_list:
        if type(j["play"]) == int:
           right_video_info_list.append(j)

    #按播放量排序
    try:
        right_video_info_list.sort(key= operator.itemgetter("play"), reverse=True)
    except TypeError as e:
        print(e)
    write_column_name("rank.txt")
    write_rank_data(right_video_info_list)

    write_column_name("all.txt")
    write_all_data(video_info_list)







