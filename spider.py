import requests,re,time,sys
from threading import Thread
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class C(Chrome):#C继承了Chrome类
    l_s_re=[]#存储结果的列表
    dy_name=""

    def begin(self):
        self.get("https://www.dy2018.com")
        element = self.find_element(By.CLASS_NAME, 'formhue')
        return element

    def search(self,element):#进入网页，搜索自己想看的电影，然后抓取搜索结果的网址
        element.send_keys(f"{self.dy_name}\n")
        page=self.page_source#抓取搜索结果的页面源代码
        return page

    def get_web(self,url):#对网站发起请求，返回网页的源代码
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/30"
        }
        resp=requests.get(url,headers=headers)
        try:
            text=resp.content.decode("gbk")
        except:
            try:
                text = resp.content.decode("utf-8")
            except:
                try:
                    text = resp.content.decode("gb2312")
                except:
                    text = resp.content.decode("iso-8859-1")
        resp.close()
        return text

    def anoly(self,url_text):#从搜索结果的网页源代码中提取每一个结果的url，并返回一个结果列表
        url1="https://www.dy2018.com/"
        s1=re.compile(r'.*?<b>.*?<a href="/(?P<s_url>.*?)" target="_blank" class="ulink" title="(?P<c_name>.*?)">'
                      r'.*?<tr>.*?<td colspan="2" style="padding-left:3px">(?P<intros>.*?)</td>.*?</tr>',re.S)
        self.l_s_re=s1.findall(url_text)# 将影片信息存进该列表中
        print("\n搜索成功！！！\n")
        for i in range(len(self.l_s_re)):
            self.l_s_re[i]=list(self.l_s_re[i])
            self.l_s_re[i][0]=url1+self.l_s_re[i][0]
            print(f"{i+1}"+"."+self.l_s_re[i][1])#打印出搜索结果
            l1=self.l_s_re[i][2].split("◎")
            for meg in l1:
                meg=meg.strip()#去除前后空白
                print("◎"+meg)
            print("\n")
        return self.l_s_re

    def select(self,l):#把结果列表输入
        i=int(input("\n请输入你要看的影片的序号："))
        url=l[i-1][0]
        #换个通用的方法来提取影片资源的下载链接
        print("请稍等......")
        self.get(url)
        l=self.find_elements(By.TAG_NAME,"td")
        print("结果已保存，若要观看，请复制链接，到迅雷打开，即可观看！！！")
        with open(f'./movies/{self.l_s_re[i-1][1]}.txt','w',encoding="utf-8")as f:
            for x in range(len(l)-2):
                print(l[x].text)
                f.write(l[x].text+"\n")

    def dtime(self):
        # 搜索倒计时
        def ftime_t():
            t = Thread(target=ftime)
            t.start()
        def ftime():
            sec = 30
            while True:
                if self.l_s_re == []:
                    sys.stdout.write("\r正在搜索中："+str(sec))
                    sys.stdout.flush()  # 刷新
                    sec -= 1
                    time.sleep(0.98)
                else:
                    break
        return ftime_t()
