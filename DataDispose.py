import time

import pandas
import pyspark
from pyspark import SparkConf
from pyspark.sql import SparkSession


def revert(city):
    citys_ = city.replace("市", " ").replace("县", " ")
    city_list = list(citys_.split(" "))
    for i in city_list:
        if i == "" or '':
            city_list.remove(i)
    citys_set = set(city_list)
    return citys_set


citys = "郑州市 洛阳市 焦作市 商丘市 信阳市 周口市 鹤壁市 安阳市 濮阳市 驻马店市 \
南阳市 开封市 漯河市 许昌市 新乡市 济源市 灵宝市 偃师市 邓州市 登封市 三门峡市 \
新郑市 禹州市 巩义市 永城市 长葛市 义马市 林州市 项城市 汝州市 荥阳市 \
平顶山市 卫辉市 辉县市 舞钢市 新密市 孟州市 沁阳市 郏县 \
合肥市 亳州市 芜湖市 马鞍山市 池州市 黄山市 滁州市 安庆市\
淮南市 淮北市 蚌埠市 宿州市 宣城市 六安市 阜阳市\
铜陵市 明光市 天长市 宁国市 界首市 桐城市 潜山市\
福州市 厦门市 泉州市 漳州市 南平市 三明市 龙岩市 莆田市 宁德市\
龙海市 建瓯市 武夷山市 长乐市 福清市 晋江市 南安市 福安市 邵武市 石狮市 福鼎市 建阳市 漳平市 永安市\
兰州市 白银市 武威市 金昌市 平凉市 张掖市 嘉峪关市 酒泉市\
庆阳市 定西市 陇南市 天水市 玉门市 临夏市 合作市 敦煌市 甘南州 \
贵阳市 安顺市 遵义市 六盘水市 兴义市 都匀市 凯里市 毕节市 清镇市\
铜仁市 赤水市 仁怀市 福泉市\
海口市 三亚市 万宁市 文昌市 儋州市 琼海市 东方市 五指山市\
石家庄市 保定市 唐山市 邯郸市 邢台市 沧州市 衡水市 廊坊市 承德市 迁安市\
鹿泉市 秦皇岛市 南宫市 任丘市 叶城市 辛集市 涿州市 定州市 晋州市 霸州市\
黄骅市 遵化市 张家口市 沙河市 三河市 冀州市 武安市 河间市深州市 新乐市\
泊头市 安国市 双滦区 高碑店市\
哈尔滨市 伊春市 牡丹江市 大庆市 鸡西市 鹤岗市 绥化市 齐齐哈尔市\
黑河市 富锦市 虎林市 密山市 佳木斯市 双鸭山市 海林市 铁力市 北安市\
五大连池市 阿城市 尚志市 五常市 安达市 七台河市 绥芬河市 双城市\
海伦市 宁安市 讷河市 穆棱市 同江市 肇东市\
武汉市 荆门市 咸宁市 襄阳市 荆州市 黄石市 宜昌市 随州市\
鄂州市 孝感市 黄冈市 十堰市 枣阳市 老河口市 恩施市 仙桃市\
天门市 钟祥市 潜江市 麻城市 洪湖市 汉川市 赤壁市 松滋市\
丹江口市 武穴市 广水市 石首市大冶市 枝江市 应城市 宜城市\
当阳市 安陆市 宜都市 利川市\
长沙市 郴州市 益阳市 娄底市 株洲市 衡阳市 湘潭市\
岳阳市 常德市 邵阳市 永州市 张家界市 怀化市 浏阳市\
醴陵市 湘乡市 耒阳市 沅江市 涟源市 常宁市 吉首市\
冷水江市 临湘市 汨罗市 武冈市 韶山市 湘西州 \
长春市 吉林市 通化市 白城市 四平市 辽源市 松原市 白山市\
集安市 梅河口市 双辽市 延吉市 九台市 桦甸市 榆树市 蛟河市\
磐石市 大安市 德惠市 洮南市 龙井市 珲春市 公主岭市 图们市\
舒兰市 和龙市 临江市 敦化市\
南京市 无锡市 常州市 扬州市 徐州市 苏州市 连云港市 盐城市\
淮安市 宿迁市 镇江市 南通市 泰州市 兴化市 东台市 常熟市\
江阴市 张家港市 通州市 宜兴市 邳州市 海门市 溧阳市 泰兴市\
如皋市 昆山市 启东市 江都市 丹阳市 吴江市 靖江市 扬中市\
新沂市 仪征市 太仓市 姜堰市 高邮市 金坛市 句容市 灌南县 海安市\
南昌市 赣州市 上饶市 宜春市 景德镇市 新余市 九江市 萍乡市\
抚州市 鹰潭市 吉安市 丰城市 樟树市 德兴市 瑞金市 井冈山市\
高安市 乐平市 南康市 贵溪市 瑞昌市 东乡县 广丰县 信州区 三清山\
沈阳市 葫芦岛市 大连市 盘锦市 鞍山市 铁岭市 本溪市 丹东市\
抚顺市 锦州市 辽阳市 阜新市 调兵山市 朝阳市 海城市 北票市\
盖州市 凤城市 庄河市 凌源市 开原市 兴城市 新民市 大石桥市\
东港市 北宁市 瓦房店市 普兰店市 凌海市 灯塔市 营口市\
西宁市 玉树市 格尔木市 德令哈市\
济南市 青岛市 威海市 潍坊市 菏泽市 济宁市 东营市烟台市\
淄博市 枣庄市 泰安市 临沂市 日照市 德州市 聊城市 滨州市\
乐陵市 兖州市 诸城市 邹城市 滕州市 肥城市 新泰市 胶州市\
胶南市 龙口市 平度市 莱西市\
太原市 大同市 阳泉市 长治市 临汾市 晋中市 运城市 忻州市\
朔州市 吕梁市 古交市 高平市 永济市 孝义市 侯马市 霍州市\
介休市 河津市 汾阳市 原平市 晋城市 潞城市\
西安市 咸阳市 榆林市 宝鸡市 铜川市 渭南市 汉中市 安康市\
商洛市 延安市 韩城市 兴平市 华阴市\
成都市 广安市 德阳市 乐山市 巴中市 内江市 宜宾市 南充市\
都江堰市 自贡市 泸州市 广元市达州市 资阳市 绵阳市 眉山市\
遂宁市 雅安市 阆中市 攀枝花市 广汉市 绵竹市 万源市 华蓥市\
江油市 西昌市 彭州市 简阳市 崇州市 什邡市 峨眉山市 邛崃市 双流县\
昆明市 玉溪市 大理市 曲靖市 昭通市 保山市 丽江市 临沧市 楚雄市\
开远市 个旧市 景洪市 安宁市 宣威市 文山市 普洱市\
杭州市 宁波市 绍兴市 温州市 台州市 湖州市 嘉兴市 金华市 舟山市\
衢州市 丽水市 余姚市 乐清市 临海市 温岭市 永康市 瑞安市 慈溪市\
义乌市 上虞市 诸暨市 海宁市 桐乡市 兰溪市 龙泉市 建德市 富德市\
富阳市 平湖市 东阳市 嵊州市 奉化市 临安市 江山市\
台北市 台南市 台中市 高雄市 桃源市\
广州市 深圳市 珠海市 汕头市 佛山市 韶关市 湛江市 肇庆市 江门市 茂名市 惠州市 梅州市 汕尾市 河源市 阳江市 清远市 东莞市 中山市 潮州市 揭阳市 云浮市\
南宁市 贺州市 玉林市 桂林市 柳州市 梧州市 北海市 钦州市 百色市\
防城港市 贵港市 河池市 崇左市 来宾市 东兴市 桂平市 北流市\
岑溪市 合山市 凭祥市 宜州市\
呼和浩特市 呼伦贝尔市 赤峰市 扎兰屯市 鄂尔多斯市 乌兰察布市\
巴彦淖尔市 二连浩特市 霍林郭勒市 包头市 乌海市 阿尔山市\
乌兰浩特市 锡林浩特市 根河市 满洲里市 额尔古纳市 牙克石市\
临河市 丰镇市 通辽市\
银川市 固原市 石嘴山市 青铜峡市 中卫市 吴忠市 灵武市\
拉萨市 那曲市 山南市 林芝市 昌都市 阿里地区日喀则市\
乌鲁木齐市 石河子市 喀什市 阿勒泰市 阜康市 库尔勒市 阿克苏市\
阿拉尔市 哈密市 克拉玛依市 昌吉市 奎屯市 米泉市 和田市 塔城市\
香港 澳门 上海 北京 天津 重庆 沈阳"
citys_henan = "郑州市 洛阳市 焦作市 商丘市 信阳市 周口市 鹤壁市 安阳市 濮阳市 驻马店市 \
南阳市 开封市 漯河市 许昌市 新乡市 济源市 灵宝市 偃师市 邓州市 登封市 三门峡市 \
新郑市 禹州市 巩义市 永城市 长葛市 义马市 林州市 项城市 汝州市 荥阳市 \
平顶山市 卫辉市 辉县市 河南 舞钢市 新密市 孟州市 沁阳市 郏县 "
set_henan = revert(citys_henan)
citys_anhui = "合肥市 亳州市 芜湖市 马鞍山市 池州市 黄山市 滁州市 安庆市\
淮南市 淮北市 蚌埠市 宿州市 宣城市 六安市 阜阳市\
铜陵市 明光市 天长市 安徽 宁国市 界首市 桐城市 潜山市"
set_anhui = revert(citys_anhui)
citys_fujian = "福建 福州市 厦门市 泉州市 漳州市 南平市 三明市 龙岩市 莆田市 宁德市\
龙海市 建瓯市 武夷山市 长乐市 福清市 晋江市 南安市 福安市 邵武市 石狮市 福鼎市 建阳市 漳平市 永安市"
set_fujian = revert(citys_fujian)
citys_hebei = "河北 石家庄市 保定市 唐山市 邯郸市 邢台市 沧州市 衡水市 廊坊市 承德市 迁安市\
鹿泉市 秦皇岛市 南宫市 任丘市 叶城市 辛集市 涿州市 定州市 晋州市 霸州市\
黄骅市 遵化市 张家口市 沙河市 三河市 冀州市 武安市 河间市深州市 新乐市\
泊头市 安国市 双滦区 高碑店市"
set_hebei = revert(citys_hebei)
citys_heilongjiang = "黑龙江 哈尔滨市 伊春市 牡丹江市 大庆市 鸡西市 鹤岗市 绥化市 齐齐哈尔市\
黑河市 富锦市 虎林市 密山市 佳木斯市 双鸭山市 海林市 铁力市 北安市\
五大连池市 阿城市 尚志市 五常市 安达市 七台河市 绥芬河市 双城市\
海伦市 宁安市 讷河市 穆棱市 同江市 肇东市"
set_heilongjiang = revert(citys_heilongjiang)
citys_hubei = "武汉 武汉市 荆门市 咸宁市 襄阳市 荆州市 黄石市 宜昌市 随州市\
鄂州市 孝感市 黄冈市 十堰市 枣阳市 老河口市 恩施市 仙桃市\
天门市 钟祥市 潜江市 麻城市 洪湖市 汉川市 赤壁市 松滋市\
丹江口市 武穴市 广水市 石首市大冶市 枝江市 应城市 宜城市\
当阳市 安陆市 宜都市 利川市"
set_hubei = revert(citys_hubei)
citys_hunan = "湖南 长沙市 郴州市 益阳市 娄底市 株洲市 衡阳市 湘潭市\
岳阳市 常德市 邵阳市 永州市 张家界市 怀化市 浏阳市\
醴陵市 湘乡市 耒阳市 沅江市 涟源市 常宁市 吉首市\
冷水江市 临湘市 汨罗市 武冈市 韶山市 湘西州"
set_hunan = revert(citys_hunan)
set_hunan.add("津市")
citys_jilin = "吉林 长春市 吉林市 通化市 白城市 四平市 辽源市 松原市 白山市\
集安市 梅河口市 双辽市 延吉市 九台市 桦甸市 榆树市 蛟河市\
磐石市 大安市 德惠市 洮南市 龙井市 珲春市 公主岭市 图们市\
舒兰市 和龙市 临江市 敦化市"
set_jilin = revert(citys_jilin)
citys_jiangsu = "江苏 南京市 无锡市 常州市 扬州市 徐州市 苏州市 连云港市 盐城市\
淮安市 宿迁市 镇江市 南通市 泰州市 兴化市 东台市 常熟市\
江阴市 张家港市 通州市 宜兴市 邳州市 海门市 溧阳市 泰兴市\
如皋市 昆山市 启东市 江都市 丹阳市 吴江市 靖江市 扬中市\
新沂市 仪征市 太仓市 姜堰市 高邮市 金坛市 句容市 灌南县 海安市"
set_jiangsu = revert(citys_jiangsu)
citys_jiangxi = "江西 南昌市 赣州市 上饶市 宜春市 景德镇市 新余市 九江市 萍乡市\
抚州市 鹰潭市 吉安市 丰城市 樟树市 德兴市 瑞金市 井冈山市\
高安市 乐平市 南康市 贵溪市 瑞昌市 东乡县 广丰县 信州区 三清山"
set_jiangxi = revert(citys_jiangxi)
citys_liaoning = "辽宁 沈阳市 葫芦岛市 大连市 盘锦市 鞍山市 铁岭市 本溪市 丹东市\
抚顺市 锦州市 辽阳市 阜新市 调兵山市 朝阳市 海城市 北票市\
盖州市 凤城市 庄河市 凌源市 开原市 兴城市 新民市 大石桥市\
东港市 北宁市 瓦房店市 普兰店市 凌海市 灯塔市 营口市"
set_liaoning = revert(citys_liaoning)
citys_shandong = "济南市 青岛市 威海市 潍坊市 菏泽市 济宁市 东营市烟台市\
淄博市 枣庄市 泰安市 临沂市 日照市 德州市 聊城市 滨州市\
乐陵市 兖州市 诸城市 邹城市 滕州市 肥城市 新泰市 胶州市\
胶南市 龙口市 平度市 莱西市 山东"
set_shandong = revert(citys_shandong)
citys_shanxi = "太原市 大同市 阳泉市 长治市 临汾市 晋中市 运城市 忻州市\
朔州市 吕梁市 古交市 高平市 永济市 孝义市 侯马市 霍州市\
介休市 河津市 汾阳市 原平市 山西 晋城市 潞城市"
set_shanxi = revert(citys_shanxi)
citys_sshanxi = "西安市 咸阳市 榆林市 宝鸡市 铜川市 渭南市 汉中市 安康市\
商洛市 延安市 韩城市 陕西 兴平市 华阴市"
set_sshanxi = revert(citys_sshanxi)
citys_sichuan = "四川 成都市 广安市 德阳市 乐山市 巴中市 内江市 宜宾市 南充市\
都江堰市 自贡市 泸州市 广元市达州市 资阳市 绵阳市 眉山市\
遂宁市 雅安市 阆中市 攀枝花市 广汉市 绵竹市 万源市 华蓥市\
江油市 西昌市 彭州市 简阳市 崇州市 什邡市 峨眉山市 邛崃市 双流县"
set_sichuan = revert(citys_sichuan)
citys_yunnan = "云南 昆明市 玉溪市 大理市 曲靖市 昭通市 保山市 丽江市 临沧市 楚雄市\
开远市 个旧市 景洪市 安宁市 宣威市 文山市 普洱市"
set_yunnan = revert(citys_yunnan)
citys_zhejiang = "浙江 杭州市 宁波市 绍兴市 温州市 台州市 湖州市 嘉兴市 金华市 舟山市\
衢州市 丽水市 余姚市 乐清市 临海市 温岭市 永康市 瑞安市 慈溪市\
义乌市 上虞市 诸暨市 海宁市 桐乡市 兰溪市 龙泉市 建德市 富德市\
富阳市 平湖市 东阳市 嵊州市 奉化市 临安市 江山市"
set_zhejiang = revert(citys_zhejiang)
citys_guangdong = "广东 广州市 深圳市 珠海市 汕头市 佛山市 韶关市 湛江市 肇庆市 江门市 茂名市 惠州市 梅州市 汕尾市 河源市 阳江市 清远市 东莞市 中山市 潮州市 揭阳市 云浮市"
set_guangdong = revert(citys_guangdong)
citys_zhuangzu = "南宁市 贺州市 玉林市 桂林市 柳州市 梧州市 北海市 钦州市 百色市\
防城港市 贵港市 河池市 崇左市 来宾市 东兴市 桂平市 北流市\
岑溪市 合山市 凭祥市 宜州市 广西"
set_zhuangzu = revert(citys_zhuangzu)
citys_neimenggu = "呼和浩特市 呼伦贝尔市 赤峰市 扎兰屯市 鄂尔多斯市 乌兰察布市\
巴彦淖尔市 二连浩特市 霍林郭勒市 包头市 乌海市 阿尔山市\
乌兰浩特市 锡林浩特市 根河市 满洲里市 额尔古纳市 牙克石市\
临河市 丰镇市 通辽市 内蒙古"
set_neimenggu = revert(citys_neimenggu)
citys_ningxia = "银川市 固原市 石嘴山市 青铜峡市 中卫市 吴忠市 灵武市 宁夏"
set_ningxia = revert(citys_ningxia)
citys_xinjiang = "乌鲁木齐市 石河子市 喀什市 阿勒泰市 阜康市 库尔勒市 阿克苏市\
阿拉尔市 哈密市 克拉玛依市 昌吉市 奎屯市 米泉市 和田市 塔城市 新疆"
set_xinjiang = revert(citys_xinjiang)
set_along = {'天津', '北京', '重庆', '上海'}
set_ga = {'香港', '澳门'}
citys_guizhou = "贵阳市 安顺市 遵义市 六盘水市 兴义市 都匀市 凯里市 毕节市 清镇市\
铜仁市 赤水市 仁怀市 福泉市 贵州"
set_guizhou = revert(citys_guizhou)
citys_gansu = "兰州市 白银市 武威市 金昌市 平凉市 张掖市 嘉峪关市 酒泉市\
庆阳市 定西市 陇南市 天水市 玉门市 临夏市 合作市 敦煌市 甘南州 甘肃"
set_gansu = revert(citys_gansu)
citys_hainan = "海口市 三亚市 万宁市 文昌市 儋州市 琼海市 东方市 五指山市 海南 "
set_hainan = revert(citys_hainan)
citys_pro = "河北省、山西省、辽宁省、吉林省、黑龙江省、江苏省、浙江省、安徽省、福建省、江西省、山东省、河南省、湖北省、湖南省、广东省\
、海南省、四川省、贵州省、云南省、陕西省、甘肃省、青海省、台湾省\
、内蒙古自治区、广西壮族自治区、西藏自治区、宁夏回族自治区、新疆维吾尔自治区\
、北京市、天津市、上海市、重庆市、香港、澳门"
set_pro = set(list(citys_pro.replace("、", " ").split(" ")))

myconf = SparkConf()
myconf.set("spark.jars.packages", "org.mongodb.spark:mongodb-spark-connector_2.12:3.0.0")
sc = pyspark.SparkContext("local", "test")
spark = SparkSession.builder.config(conf=myconf).getOrCreate()

# 需要改
df = spark.read.format("com.mongodb.spark.sql") \
    .option("uri", "mongodb://39.99.155.45:27017/job") \
    .option("collection", "Post-info") \
    .load()

# 将城市转化成list
pd = df.toPandas()
# pd = pandas.read_csv('data0.csv')
print(time.time())
co = 0
cc = 0
pd = pd.drop(
    ['_id', 'co_trade', 'co_type', 'co_url', 'id', 'info', 'otherq', 'pub_time', 'time', 'url',
     'website', 'welfare', 'exp']
    , axis=1)
# pd.to_csv('data0.csv')

pd = pd.fillna("nn")
pd = pd.drop(pd[pd.salary == "nn"].index)
pd = pd.drop(pd[pd.salary == ""].index)
pd = pd.drop(pd[pd.num == "nn"].index)
pd = pd.drop(pd[pd.num == "招若干人"].index)
# pd.to_csv('data0.csv')
for i in range(0, len(pd)):
    if pd.iloc[i]['local'] != "nn":
        if '（' not in pd.iloc[i]['co_name']:
            if '-' not in pd.iloc[i]['co_name']:
                if "CBD" not in pd.iloc[i]['local']:
                    temp = pd.iloc[i]['local'][0:2]
                    pd.iloc[i, 3] = temp
                elif "CBD" in pd.iloc[i]['local']:
                    pd.iloc[i, 3] = pd.iloc[i]['co_name'][0:2]
            else:
                fin = pd.iloc[i]['co_name'].find('-')
                pd.iloc[i, 3] = pd.iloc[i]['co_name'][fin + 1:fin + 3]
        else:
            begin = pd.iloc[i]['co_name'].find('（')
            end = pd.iloc[i]['co_name'].find('）')
            pd.iloc[i, 3] = pd.iloc[i]['co_name'][begin + 1:end]
    else:
        if '（' in pd.iloc[i]['co_name']:
            begin = pd.iloc[i]['co_name'].find('（')
            end = pd.iloc[i]['co_name'].find('）')
            pd.iloc[i, 4 - 1] = pd.iloc[i]['co_name'][begin + 1:end]
        elif '-' in pd.iloc[i]['co_name']:
            fin = pd.iloc[i]['co_name'].find('-')
            pd.iloc[i, 4 - 1] = pd.iloc[i]['co_name'][fin + 1:fin + 3]
        else:
            pd.iloc[i, 4 - 1] = pd.iloc[i]['co_name'][0:2]
    if "招" in pd.iloc[i]['num']:
        temp = pd.iloc[i]['num']
        temp = temp.replace("招", "")
        temp = temp.replace("人", "")
        pd.iloc[i, 6 - 1] = int(temp)
    if "，" in pd.iloc[i, 4]:
        pd.iloc[i, 5 - 1] = pd.iloc[i, 5 - 1].replace("，", " ")
    if "," in pd.iloc[i, 5 - 1]:
        pd.iloc[i, 5 - 1] = pd.iloc[i, 5 - 1].replace(",", " ")
    if pd.iloc[i]['edu'] is None:
        pd.iloc[i]['edu'] = "不限"
    if "K" in pd.iloc[i]['salary']:
        pd.iloc[i, 7 - 1] = pd.iloc[i]['salary'].replace("K", "")
    if "k" in pd.iloc[i]['salary']:
        pd.iloc[i, 7 - 1] = pd.iloc[i]['salary'].replace("k", "")
    if pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "以上千/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 1000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "以上万/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 10000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-3:] == "千/月":
        temp = pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-3:1]
        num1, num2 = temp.split('-')
        num1 = float(num1)
        num2 = float(num2)
        num = (num1 + num2) / 2
        num *= 1000
        pd.iloc[i, 7 - 1] = int(num)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-3:] == "万/月":
        temp = pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-3:1]
        num1, num2 = temp.split('-')
        num1 = float(num1)
        num2 = float(num2)
        num = (num1 + num2) / 2
        num *= 10000
        pd.iloc[i, 7 - 1] = int(num)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-3:] == "元/天":
        pd.iloc[i, 7 - 1] = int(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-3:1]) * 30
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-4:] == "元/小时":
        pd.iloc[i, 7 - 1] = int(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-4:1]) * 240
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "千以下/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 1000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "千以上/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 1000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "万以上/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 10000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "万以下/月":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 10000)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "万以上/年":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 10000 / 12)
    elif pd.iloc[i]['salary'] is not None and pd.iloc[i]['salary'][-5:] == "万以下/年":
        pd.iloc[i, 7 - 1] = int(float(pd.iloc[i]['salary'][-len(pd.iloc[i]['salary']):-5:1]) * 10000 / 12)
    if set_hunan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "湖南省"
    elif set_sshanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "陕西省"
    elif set_hainan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "海南省"
    elif set_gansu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "甘肃省"
    elif set_guizhou.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "贵州省"
    elif set_xinjiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "新疆维吾尔自治区"
    elif set_ningxia.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "宁夏回族自治区"
    elif set_neimenggu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "内蒙古自治区"
    elif set_zhuangzu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广州省"
    elif set_guangdong.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广东省"
    elif set_shanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山西省"
    elif set_shandong.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山东省"
    elif set_jiangxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "江西省"
    elif set_jiangsu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "江苏省"
    elif set_jilin.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "吉林省"
    elif set_heilongjiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "黑龙江省"
    elif set_hebei.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "河北省"
    elif set_henan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "河南省"
    elif set_hubei.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "湖北省"
    elif set_zhuangzu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广西壮族自治区"
    elif set_zhejiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "浙江省"
    elif set_yunnan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "云南省"
    elif set_shanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山西省"
    elif set_liaoning.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "辽宁省"
    elif set_fujian.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "福建省"
    elif set_anhui.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "安徽省"
    elif set_sichuan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "四川省"
    elif set_along.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = pd.iloc[i]['local'] + "市"
    elif set_ga.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = pd.iloc[i]['local']
    elif "区" in pd.iloc[i]['area']:
        pd.iloc[i, 0] = pd.iloc[i]['co_name'][0:2] + "市"
    if set_hunan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "湖南省"
    elif set_sshanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "陕西省"
    elif set_hainan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "海南省"
    elif set_gansu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "甘肃省"
    elif set_guizhou.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "贵州省"
    elif set_xinjiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "新疆维吾尔自治区"
    elif set_ningxia.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "宁夏回族自治区"
    elif set_neimenggu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "内蒙古自治区"
    elif set_zhuangzu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广州省"
    elif set_guangdong.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广东省"
    elif set_shanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山西省"
    elif set_shandong.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山东省"
    elif set_jiangxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "江西省"
    elif set_jiangsu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "江苏省"
    elif set_jilin.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "吉林省"
    elif set_heilongjiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "黑龙江省"
    elif set_hebei.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "河北省"
    elif set_henan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "河南省"
    elif set_hubei.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "湖北省"
    elif set_zhuangzu.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "广西壮族自治区"
    elif set_zhejiang.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "浙江省"
    elif set_yunnan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "云南省"
    elif set_shanxi.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "山西省"
    elif set_liaoning.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "辽宁省"
    elif set_fujian.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "福建省"
    elif set_anhui.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "安徽省"
    elif set_sichuan.__contains__(pd.iloc[i]['local']):
        pd.iloc[i, 0] = "四川省"
    elif not set_pro.__contains__(pd.iloc[i]['area']):
        pd.iloc[i, 0] = "nn"
    dd = pd.iloc[0:2]
    if pd.iloc[i, 0] != "nn":
        if co == 2:
            dd.to_csv('.\data\data.csv', mode='a', header=False, index=None)
            time.sleep(0.1)
            co = 0
        else:
            dd.iloc[co] = pd.iloc[i]
            co += 1
print(time.time())
