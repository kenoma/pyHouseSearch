import urllib
import os
import logging
import re
import datetime
import random
import time
from time import localtime, strftime
from grab.spider import Spider, Task

imgDict, typeDict, roomsDict = {}, {}, {}
sitePath = 'cian/'

class SitePars(Spider):
    initial_urls = ['http://www.cian.ru/cat.php?deal_type=2&obl_id=1&city[0]=1&room0=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&p=1']

    def prepare(self):
        if not os.path.exists(self.env.dataDir + sitePath):
            os.mkdir(self.env.dataDir + sitePath)
        if not os.path.exists(self.env.dataDir + u'cian_output.csv'):
            self.csv_file = open(self.env.dataDir + u'cian_output.csv', u'w', encoding=u'utf-8')
            self.csv_file.write(u'ID объекта;Тип недвижимости;Адрес;Станция метро;Этаж/Этажность;Количество комнат;Площадь общая;Площадь жилая;Площадь кухни;Вид передаваемого права;Цена продажи;Дата предложения;Описание;Агентство;Телефон;Ссылка\n')
        else:
            self.csv_file = open(self.env.dataDir + u'cian_output.csv', u'a', encoding=u'utf-8')

    def task_initial(self, grab, task):
        num_of_pages = 2
        for n in range(1, num_of_pages):
            yield Task(u'nav', url = u'https://rostov.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=%s&region=4959&room1=1&room2=1&room3=1&room7=1&room9=1' % n)

    def task_nav(self, grab, task):
        global typeDict

        obj, url, request, xpath_string = '', '', '', ''
        for elem in grab.doc.tree.xpath('//a[@target="_blank"]/@href'):
            if elem[0:33]=='https://rostov.cian.ru/sale/flat/':
                url = grab.make_url_absolute(elem)               
                yield Task('cianobject', url=grab.make_url_absolute(elem))

    def task_cianobject(self, grab, task):
        global imgDict, typeDict, roomsDict

        nonNum = re.compile(u'[^0-9]', re.U)
        stripNum = re.compile(u'\d+',re.U)
        mainDescr, listDescr = '', []
        dateYest = datetime.timedelta(days=1)

        objID = stripNum.findall(task.url)[0]

        rType, rAddress, rMetro, rFloor, rRoomCount, rSquare, rLiveSquare, rDinnerSquare, rRights, rCost, rDate, rDescr, rAgency, rPhone, rawDescr = \
            ';', ';', ';', ';', ';', ';', ';', ';', ';', ';', ';', ';', ';', ';', ''

#
        request = '//td[@id="dl2m_' + obj + '_dopsved"]'
        xpath_string = grab.xpath(request)
            
        if len(xpath_string.text_content().encode('utf-8').split(u'Новостройка')) > 1:
            typeDict[obj] = u'Новостройка;'
        elif len(xpath_string.text_content().encode('utf-8').split(u'Вторичка')) > 1:
            typeDict[obj] = u'Вторичка;'
        else:
            typeDict[obj] = 'not defined;'

        request = '//td[@id="dl2m_' + obj + '_room"]'
        xpath_string = grab.xpath(request)
        roomsDict[obj] = xpath_string.text_content().encode('utf-8').split('\n')[0] + ';'
#                

        #вид передаваемого права
        rRights = typeDict[objID]
        
        #количество комнат
        rRoomCount = roomsDict[objID]

        #тип недвижимости
        if rRoomCount == u'комната;':
            rType = u'Комната;'
        else:
            rType = u'Квартира;'

        #адрес
        for elem in grab.xpath_list('//h1[@class="object_descr_addr"]'):
            rAddress = elem.text_content().encode('utf-8').replace('\r\n', '').replace('\t', '').replace('\n', '').replace('\r', '').strip() + ';'

        #станция метро
        for elem in grab.xpath_list('//div[@class="object_descr_metro"]'):
            rMetro = elem.text_content().encode('utf-8').replace('\r\n', '').replace('\t', '').replace('\n', '').replace('\r', '').strip() + ';'

        #стоимость
        for elem in grab.xpath_list('//div[@class="object_descr_price"]'):
            if len(elem.text_content().encode('utf-8').split('~')) > 1:
                rCost = str(re.sub(nonNum, '', elem.text_content().encode('utf-8').split('~')[1])) + ';'
            else:
                rCost = str(re.sub(nonNum, '', elem.text_content())) + ';'

        #общий блок описания
        for elem in grab.xpath_list('//table[@class="object_descr_props"]'):
            mainDescr = elem.text_content().encode('utf-8')

        listDescr = mainDescr.split('\n')

        for count in range(len(listDescr)):
            if listDescr[count].strip() == u'Этаж:':
                rFloor = listDescr[count+1].strip() + ';'
            if listDescr[count].strip() == u'Общая площадь:':
                rSquare = listDescr[count+2].strip() + ';'
            if listDescr[count].strip() == u'Жилая площадь:':
                rLiveSquare = listDescr[count+1].strip() + ';'
            if listDescr[count].strip() == u'Площадь кухни:':
                rDinnerSquare = listDescr[count+1].strip() + ';'

        #дата
        for elem in grab.xpath_list('//span[@class="object_descr_dt_added"]'):
            if elem.text_content().encode('utf-8')[0:10] == u'вчера':
                rDate = str(datetime.date.today() - dateYest) + ';'
            elif elem.text_content().encode('utf-8')[0:14] == u'сегодня':
                rDate = str(datetime.date.today()) + ';'
            else:
                rDate = elem.text_content().encode('utf-8') + ';'

        #агентство
        for elem in grab.xpath_list('//span[@class="object_descr_rieltor_name"]'):
            rAgency = elem.text_content().encode('utf-8') + ';'

        #описание
        for elem in grab.xpath_list('//div[@class="object_descr_text"]'):
            rDescr = elem.text_content().encode('utf-8').replace('\r\n', '').replace('\t', '').replace('\n', '').replace('\r', '').replace(';', '|').strip() + ';'

        #телефоны
        for elem in grab.xpath_list('//div[@class="object_descr_phones"]/strong'):
            rPhone = elem.text_content().encode('utf-8') + ';'

        #составляем строку для заливки 
        stringO = objID + ';' + rType + rAddress + rMetro + rFloor \
            + rRoomCount + rSquare + rLiveSquare + rDinnerSquare \
            + rRights + rCost + rDate + rDescr + rAgency + rPhone + task.url + ';'

        #пишем в файл
        stringO = stringO.strip('\r\n\t').replace('\r\n', ' ')
        self.csv_file.write(stringO + "\n")

        #меняем каталог для работы с фс
        os.chdir(self.env.envOutput + sitePath)
        os.mkdir(objID)
        # save an url screenshot
        ##scrFolder = self.glb.envOutput + 'screenshots/'
        
        scrFolder = self.env.envOutput + sitePath + objID

        if self.env.usrFlag == 1:
            # write here your command! change sript_name to your
            currCmd = self.env.dataDir + 'script_name' + ' ' + task.url + ' -o ' + scrFolder + task.url.split('/')[-2] + '.png'
        elif self.env.usrFlag == -1:
            currCmd = 'python ' + '/root/Desktop/pyParser/webkit2png' + ' ' + task.url + ' -f jpg -o ' + scrFolder + '/' + objID + '.jpg'
            #currCmd = 'python ' + self.glb.envDir + 'Modules/webkit2png_lin.py' + ' ' + task.url + ' -o ' + scrFolder + task.url.split('=')[1] + '.png'
        
        os.system(currCmd)

        # saving all images. PLEASE, CREATE imgs folder in pyOutput 
        for nxtElem in grab.tree.xpath('//div[@class="object_descr_images_w"]/a/@href'):
            imgDict[grab.make_url_absolute(nxtElem)]=objID
            yield Task('imageSave', url=grab.make_url_absolute(nxtElem))

    #images saving...
    def task_imageSave(self, grab, task):
        global imgDict
        imgRes = imgDict[task.url] + '_' + str(random.randint(1,99))
        path = self.env.envOutput + sitePath + imgDict[task.url] + '/%s.jpg' % imgRes
        grab.response.save(path)

def GoGrab(env, threads = 1, debug = False):
    print('')
    print('Grabing cian.ru ')
    print(' at ' + strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print('\r\n')
    logging.basicConfig(level=logging.DEBUG)
    bot = SitePars(thread_number = threads)
    bot.env = env
    bot.run()

