### Description
要控制好的就是 douban.py 中的 URL 和 Xpath...
### Run
``` zsh
# 进入 shell 模式测试, 一般配置好 settings.py 以后先用这个测试一下
scrapy shell https://movie.douban.com/chart  # 这个命令和 settings.py 中 DEFAULT_REQUEST_HEADERS, USER_AGENT 有很大的联系
view(response)  # 可以看爬取的结果, 相当于运行到 spiders/xx.py parse() 那里停下了

scrapy genspider -t basic douban douban.com  # 新建一个爬虫, 生成 spiders/douban.py; -t basic 是默认的
# 修改 items.py 和 douban.py; (items 中默认只有 JspiderItem, 删掉重写)
# pipelines.py 中修改 MongoDB 的相关东西
scrapy crawl douban  # 运行项目
# 过程是: 运行 douban.py -> 抓取整个网页赋值给 reponse -> parse() 处理 reponse, 将 JspiderItem 的实例 item 的各个成员变量赋值 ->
# parse() 将 item 传递给 pipelines.py 中的 JspiderPipeline 的方法 process_item()
# process_item() 这里可以对数据进行处理(也可以不处理), 将数据 return -> 默认是打印出来
# 其中每个 item 传递后都有 yield item 来进行异步
```
### Tips
``` zsh
# 本别用 Copy Xpath 和 Copy selector 得到下面结果, 将表示范围的去掉
//*[@id="subject_list"]/ul/li[1]/div[2]
subject_list > ul > li:nth-child(1) > div.info  # for sel in response.css('#subject_list > ul > li > div.info'):
```
