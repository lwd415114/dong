# -*- coding: utf-8 -*-
import scrapy
from qiche.items import QicheItem
from urllib import request
import time,os,random
import ssl
class YxSpider(scrapy.Spider):
    name = 'YX'
    allowed_domains = ['www.xin.com']
    start_urls = ['https://www.xin.com/xian/i1/']
    def parse(self, response):
        res=response.css("div.carlist-show>div>ul li")
        item=QicheItem()
        for x in res:
            item['name']=x.css('div.pad h2 a::text').extract_first()
            item['years']=x.css("div.pad span::text").extract_first()
            item['far']=x.css("div.pad span").xpath('string(.)').extract_first()
            
            item['price']=x.css("div.pad p em").xpath("string(.)").extract_first()
            if item['price']:
                item['price']=item['price'].replace('\n','').replace(' ','')
                
            item['price1']=x.css("div.pad span.pay-price").xpath("string(.)").extract_first()
            if item['price1']:
                item['price1']=item['price1'].replace('\n','').replace(' ','')
                
            item['mai']=x.css("span.change-ycgicon::text").extract_first()
            #获取车辆的url并进入到车辆的网页
            item['p']=x.css("div.across a::attr(href)").extract_first()
            p_url='https:'+item['p']
            time.sleep(random.random()*3)
            yield scrapy.Request(p_url,callback=self.p_parse)

            yield item
        for page in range(1,51):
            url="https://www.xin.com/xian/i"+str(page)
            yield scrapy.Request(url,callback=self.parse)

    def p_parse(self,response):
        nm=response.css("span.cd_m_h_tit::text").extract_first().replace("\n",'').strip()
        try:
            #建立文件夹在img文件夹下以车的名字命名
            os.mkdir('img/'+nm)
        except:
            pass
        
        re=response.css('dl.cd_m_i_imglist dd')
        print(re)
        for i in re:
            try:
                img=i.css("img::attr('data-src')").extract_first()
                print(img)
                img_url='https:'+img
                print(img_url)
                ssl._create_default_https_context = ssl._create_unverified_context
                time.sleep(5)
                request.urlretrieve(img_url,'img/'+nm+'/'+img.split('/')[-1])
            except:
                raise
            
            
        

            
        
      
