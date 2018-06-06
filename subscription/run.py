from scrapy.cmdline import execute
from subscription import MailTool

# execute(['scrapy', 'crawl', 'weibo'])
# execute(['scrapy', 'crawl', 'wechat'])
MailTool.send_wechat()