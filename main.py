# Press the green button in the gutter to run the script.
from spider import C
from selenium.webdriver.chrome.options import Options#无头浏览器，打开使用浏览器的过程在后台进行，不显示窗口


class Dytt(object):
    def spider(self):
        print("程序正在启动中，请稍后。。。。。。")
        opt = Options()
        opt.add_argument("--headless")  # 无头设置
        c = C(options=opt)
        c.implicitly_wait(8)
        element = c.begin()  # 先启动浏览器，进入网页，并找到输入搜索框,返回搜索框元素
        print("注意：输入的关键字只能在2-30个字符之间！！！")
        c.dy_name = input("请输入要搜索的影片名称：")
        c.dtime()  # 倒计时
        url_text = c.search(element=element)  # 进入主页搜索电影,返回搜索结果的页面源代码
        l_re = c.anoly(url_text=url_text)  # 解析页面源代码，提取出结果，存在一个列表里
        c.select(l=l_re)  # 把结果列表传入，从中拿到自己想看的电影的主页链接，并对该主页发起requests请求，解析获取我们最终所需的视频链接
        c.quit()  # 退出窗口


if __name__ == '__main__':
    d=Dytt()
    d.spider()


