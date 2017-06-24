# -*- coding: utf-8 -*-
# 这个以后用到了再整理
import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["xuzhougeng.top"]

    def start_requests(self):
        return [Request('http://xuzhougeng.top/auth/login', callback=self.post_login)]

    def post_login(self, response):
        sign_in = response.xpath('//*[@id="navbar-collapse-01"]/ul[2]/li/a/text()').extract()[0]
        print(sign_in)
        csrf = response.css('div > input::attr(value)').extract_first()
        return FormRequest.from_response(response,formdata=
        {'csrf_token':csrf,
         'email':'admin@admin.com',
         'password':'password',
         'remember_me':'y',
         'submit:':'Log In'
         },callback=self.after_login)

    def after_login(self, response):
        sign_out = response.css('#signin_icon > a::text').extract()
        print(sign_out)
