import urllib
import os
import logging
import re
import datetime
import random
import time
from time import localtime, strftime
from grab.spider import Spider, Task
import codecs

sitePath = 'cian/'
visitedDic = dict()

class SitePars(Spider):
    initial_urls = ['https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=4959&room1=1']
    

    def prepare(self):
        if not os.path.exists(self.env.dataDir + sitePath):
            os.mkdir(self.env.dataDir + sitePath)
        if not os.path.exists(self.env.dataDir + u'cian_output.csv'):
            with codecs.open(self.env.dataDir + u'cian_output.csv', u'w', encoding=u'utf-8') as csv_file:
                csv_file.write(u'ID;Type;Material;Region;Street;Floor;MaxFloor;Rooms;Square;LivingSquare;KitchenSquare;Price;Delivery;rBuilt;Date;Link;\n')

    def task_initial(self, grab, task):
        num_of_pages = 2+200
        for n in range(1, num_of_pages):
            yield Task(u'nav', url = u'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=%s&region=4959&room1=1' % n)

    def task_nav(self, grab, task):

        obj, url, request, xpath_string = '', '', '', ''
        for elem in grab.doc.tree.xpath('//a[@target="_blank"]/@href'):
            if elem[0:33] == 'https://rostov.cian.ru/sale/flat/':
                url = grab.make_url_absolute(elem)               
                yield Task('cianobject', url=grab.make_url_absolute(elem))

    def task_cianobject(self, grab, task):
        global visitedDic

        stripPrice = re.compile(u'[\s0-9]+', re.U)
        stripNum = re.compile(u'\d+',re.U)
        mainDescr, listDescr = '', []
        dateYest = datetime.timedelta(days=1)
        
        objID = stripNum.findall(task.url)[0]
        if objID in visitedDic:
            return
        visitedDic[objID]=1
        rCost = stripPrice.findall(grab.doc.select(u'//div[@class="object_descr_price"]').text())[0]
        rCost = re.sub("[^0-9]","", rCost, re.U) + ';'
        
        rType = grab.doc.select(u'//tr[th[contains(.,\'Тип дома:\')]]/td').text()
        rMaterial = '-;'
        if rType.find(',')!=-1:
            rMaterial = rType.split(',')[1] + ';'
        rType = rType.split(',')[0].replace(u'вторичка','0').replace(u'новостройка','1') + ';'
        
        rRegion = grab.doc.select(u'//a[@class=\'breadcrumbs__item\'][4]').text().replace(u'район','').strip() + ';'#grab.doc.select(u'//h1[@class="object_descr_addr"]').text() + ';'
        rStreet = grab.doc.select(u'//h1[@class=\'object_descr_addr\']/a[4]').text() + ';'
        rFloor = grab.doc.select(u'//tr[th[contains(.,\'Этаж\')]]/td').text()
        rMaxFloor = rFloor.split('/')[1].strip() + ';'
        rFloor = rFloor.split('/')[0].strip() + ';'
        rRoomCount = grab.doc.select(u'//div[@class="object_descr_title"]').text().replace(u'студия','0')
        rRoomCount = stripNum.findall(rRoomCount)[0] + ';'
        rSquare = grab.doc.select(u'//tr[th[contains(.,\'Общая площадь:\')]]/td').text()
        rSquare = rSquare.split(' ')[0] + ';'
        rLiveSquare = grab.doc.select(u'//tr[th[contains(.,\'Жилая площадь:\')]]/td').text()
        rLiveSquare = rLiveSquare.split(' ')[0] + ';'
        rDinnerSquare = grab.doc.select(u'//tr[th[contains(.,\'Площадь кухни:\')]]/td').text()
        rDinnerSquare = rDinnerSquare.split(' ')[0] + ';'
        try:
            rDelivery = grab.doc.select(u'//tr[th[contains(.,\'Сдача ГК\')]]/td').text() + ';'
        except:
            rDelivery = '-;'
        try:
            rBuilt = grab.doc.select(u'//tr[th[contains(.,\'Год постройки\')]]/td').text() + ';'
        except:
            rBuilt = '-;'
        
        #rRights = grab.doc.select(u'//tr[th[contains(.,\'Тип
        #продажи:\')]]/td').text() + ';'
        
        for elem in grab.xpath_list(u'//span[@class="object_descr_dt_added"]'):
            if elem.text_content().find(u'вчера') != -1:
                rDate = str(datetime.date.today() - dateYest) + ';'
            elif elem.text_content().find(u'сегодня') != -1:
                rDate = str(datetime.date.today()) + ';'
            else:
                rDate = elem.text_content() + ';'

        #агентство
        for elem in grab.xpath_list(u'//span[@class="object_descr_rieltor_name"]'):
            rAgency = elem.text_content() + ';'
        
        stringO = objID + ';' + rType + rMaterial + rRegion + rStreet + rFloor + rMaxFloor + rRoomCount + rSquare + rLiveSquare + rDinnerSquare + rCost + rDelivery+rBuilt + rDate + task.url + ';'

        #пишем в файл
        stringO = stringO.strip('\r\n\t').replace('\r\n', ' ')
        with codecs.open(self.env.dataDir + u'cian_output.csv', u'a', encoding=u'utf-8') as csv_file:
            csv_file.write(stringO + "\n")


def GoGrab(env, threads=1, debug=False):
    print('')
    print('Grabing cian.ru ')
    print(' at ' + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print('\r\n')
    logging.basicConfig(level=logging.DEBUG)
    bot = SitePars(thread_number = threads)
    bot.env = env
    bot.run()

