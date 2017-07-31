import os
from selenium import webdriver
from pyquery import  PyQuery as pq

# 创建一个driver,使用phantomjs浏览器
driver = webdriver.PhantomJS()




class Model(object):
    """
    基类，显示类信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}'.format(name, '\n '.join(properties))
        return s

class Zhi_Good(Model):
    """
    商品类,信息有图片链接，购买链接，价格预览，商品简介
    """
    def __init__(self):
        self.cover_url = ''
        self.abstract = ''
        self.buy_url = ''
        self.price = ''

def cathed_url(url):
    """
    缓存网页
    """
    folder = 'cached_url'
    filename = url.split('/')[-2] + '.html'
    print('文件名', filename)
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        driver.get(url)
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content

def item_form_div(div):
    """
    从div里获取商品信息
    """
    e = pq(div)

    g = Zhi_Good()
    g.abstract = e('.title_box').text()
    g.cover_url = e('.post_box_img img').attr('src')
    g.buy_url = e(".post_box_buy a").attr('href')
    g.price = e('.post_box_show').text()
    return g
    pass

def item_from_url(url):
    """
    获得指定div,通过div获取所需商品信息
    """
    page = cathed_url(url)
    e = pq(page)
    items = e(".post_box_t")
    return [item_form_div(i) for i in items]
    pass

def main():
    for i in range(0, 10):
        items = item_from_url('http://zhizhizhi.com/tc/shipin/page/{}/'.format(i))
        print(items)
    driver.close()
    pass

if __name__ == '__main__':
    main()




