# -*- coding: utf-8 -*-
# 1. 网上的一些 Ajax 的网站经常有变化, 爬虫会失效
# 2. 大型网站太复杂, 对 ajax 这个知识点...
# 3. 只学习爬取 Ajax, 都后台的运行情况不清楚, 感觉心里没底...
# 4. 所以自己弄了个简单使用 Ajax 的网站来爬取, 而且用了两层 Ajax...
# 5. 自己的网站, 运行在自己电脑上, 保证各种 Restful API 接口不会变
# 6. 更重要的是, 可以直接看 Restful API 的源码!!!
import scrapy
from ..items import UserItem

class AjaxSpider(scrapy.Spider):
    name = "ajax"
    allowed_domains = ["localhost:3000"]  # cdjblog && staexp && docmongo, 开启 Express 博客和数据库, 要先在界面上添加几个用户
    start_urls = ['http://localhost:3000/users']  # 点击用户名, 会在左侧 Ajax 显示用户名
    # 界面分为 User Infr, User List, Add User 几个区域, 初始化爬取的都为空的, User List 也是使用 Ajax 从 Mongo 读取的
    # 当用 Ajax 加载出来 User List 中下信息以后, 用鼠标点击 UserName, 会在左侧 User Info 中显示详细信息, 这个过成也是 Ajax
    # 两侧 Ajax, 最终目标是 User Info 中的内容

    def parse(self, response):  # 这个函数会自动调用, 下面的需要 callback 指定
        item = UserItem()
        import pdb; pdb.set_trace()  # p response.body && open('tmp.html', 'w').write(str(response.body))
        # 可以发现只是 layout.pug 和 user-manager.pug 中的内容, 从 Mongo 中读取的信息都无法显示
        # 在 Network 中可以看到 user-manager.js, Request URL:http://loo:3000/javascripts/user-manager.js, 这就是 Ajax 的 js 文件
        # 在 userlist 中可以发现一个 URL http://loo:3000/users/userlist
        return [Request("http://loo:3000/users/userlist", callback = self.post_login)]
        pass
        # 这个 ajax 先放一放, 看完 scrapy 文档, 知道各种函数的自动调用关系后在来写
