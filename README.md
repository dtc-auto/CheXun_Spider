# CheXun_Spider
initial commit
一：Spiders：
1.	__init__.py：
略
2.	Brand_Spider.py：
品牌爬虫，对应SQL Server中[BDCI_CHEXUN].[stg].[CONFIG_BRANDS]表
3.  Column_Spider.py：
列名爬虫，对应SQL Server中[BDCI_CHEXUN].[stg].[CONFIG_ITEM]表
4.  Companies_Spider.py：
		公司爬虫，对应SQL Server中[BDCI_CHEXUN].[stg].[CONFIG_COMPANIES]表
5.  Configuration_Spider.py：
		配置爬虫，对应SQL Server中[BDCI_CHEXUN].[stg].[CONFIGURATION_DETAILS]表
6.  main.py：
启动文件，输出.log日志文件
7.  URL_Spider.py：
		URL爬虫：对应SQL Server中[BDCI_CHEXUN].[stg].[CONFIG_SERIES]表
二：utils：
1.	__init__.py：
略
2.	items.py：
定义所有爬虫文件中返回item的字段
3.	middlewares.py：
略
4.	pipelines.py：
将爬虫数据存入SQL Server
5.	setting：
配置参数：
	DATABASE_HOST：用于定义服务器地址
	DATABASE_SERVER_NAME：用于数据库链接时定义服务器名
	DATABASE_NAME：用于定义服务器中数据库名
	DATABASE_USER_NAME：用于定义服务器登录名
	DATABASE_USER_PASSWORD：用于定义服务器登录密码
	USER_AGENT：定义head
	STAR_SPIDER_NAME：定义本次运行时启动的Spider
	FEED_FORMAT：定义输出的文件格式（测试输出表时使用）
	FEED_URI：定义输出文件名
	INTO_SQL：设置是否启动sql写入 ‘1’ 为启动
	SAVE_SOURCE_DATA：
	设置是否启动网页源代码写入.txt ‘1’ 为启动
	（仅当Configuration_Spider启动时生效）
	FILE：设置网页源代码存储路径
	CONCURRENT_REQUESTS：设置线程数
三：其他：
	Requirements.txt：定义本程序需要使用的包
