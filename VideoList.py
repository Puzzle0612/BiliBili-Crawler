"获取所有完结番链接模块"
import requests
from bs4 import BeautifulSoup
import lxml
import csv
# 定义全局变量headers
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"
}

def get_total_pages(url,headers=headers):
	"""
	获取完结番总页数函数
	:param url:
	:param headers:
	:return: 总页数
	"""
	response = requests.get(url,headers=headers)
	# 拿到真正的json数据
	json_data = response.json()
	page_info = json_data.get("data").get("page")
	total_rows = int(page_info.get("count"))
	page_size = int(page_info.get("size"))

	if(total_rows%page_size==0):
		return total_rows//page_size
	else:
		return total_rows//page_size+1

def get_video_info_list(total_pages,url,headers=headers):
	"""
	获取全部完结番的url
	:param total_pages:
	:param url:
	:param headers:
	:return: 所有完结番的url的list
	"""
	# 从第一页开始一直到最后一页
	for i in range(1,total_pages):
		# 给url加上当前页数的参数
		appended_url = url+"&pn="+str(i)
		response = requests.get(appended_url,headers=headers)
		# 拿到返回的json数据
		json_data = response.json()
		video_info_list = json_data.get("data").get("archives")
		write_data(video_info_list)


def write_data(video_info_list):
	# 将番剧信息全部写入csv文件里面
	with open("video.csv", "a",encoding="utf-8") as file:
		writer = csv.writer(file)
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

			# 拿到对应的标签
			tags = get_video_tags(each.get("aid"))
			each_info.append(tags)

			writer.writerow(each_info)

def write_column_name():
	"""
	因为列名只写一次，所以定义为函数，只在最开始的时候执行一次
	:return:
	"""
	with open("video.csv", "a",encoding="utf-8") as file:
		writer = csv.writer(file)
		# 先写列名
		column_name_list = ["番号", "集数", "名字", "播放量", "投稿时间", "作者", "收藏数", "硬币数", "评论数","弹幕数","标签"]
		writer.writerow(column_name_list)

def get_video_tags(aid):
	"""
	根据番剧的番号aid得到标签
	:param aid:
	:return:标签名字的数组
	"""
	get_tags_url =  "https://api.bilibili.com/x/tag/archive/tags?aid="+str(aid)
	response = requests.get(get_tags_url,headers=headers)
	json_data = response.json()
	# 拿到所有标签的完整信息
	tag_list = json_data.get("data")
	# 经测试，拿到的标签信息数组可能是NULL
	# 所以当为null时，返回一个空数组
	if(tag_list):
		# 创建只有标签名字的list
		tags = []
		for i in tag_list:
			tags.append(i.get("tag_name"))
		return tags
	return []

if __name__=="__main__":
	# 获取完结番分页信息链接
	# 返回的数据是json
	# tid参数是表示完结番分类id
	get_pages_url = "https://api.bilibili.com/archive_rank/getarchiverankbypartion?tid=32"
	total_pages = get_total_pages(get_pages_url)
	# 拿到番剧列表的链接
	get_video_list_url = "https://api.bilibili.com/archive_rank/getarchiverankbypartion?tid=32"
	write_column_name()
	get_video_info_list(total_pages,get_video_list_url)



