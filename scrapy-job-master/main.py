from scrapy import cmdline



website = 'zhipin'
choice = input("\n>>")
if choice == 0:
    website = 'zhipin'
elif choice == "1":
    website = '51job'
elif choice == "2":
    website = 'lagou'
cmdline.execute("scrapy crawl {}".format(website).split())
