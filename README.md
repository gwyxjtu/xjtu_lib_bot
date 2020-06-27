# xjtu_lib_bot
西安交通大学图书馆预约抢座位脚本

## 使用方法
在config中修改用户名和密码,personid是你的学号，修改完成后直接运行reserve.py。
reserve.py里面默认抢的是我最喜欢的三楼座位，如果你喜欢二楼座位，可以去运行reserve_floor_2.py进行预约

目前里面仍有一些参数我没有搞清楚，由于我能力有限，只能写死。我写死的地方有：兴庆校区图书馆(第一层认证里面的east参数)；座位我只喜欢三楼(遍历只遍历的三楼)。


**脚本运行环境必须校内网络，可以宿舍或者STUwifi**

stabel是稳定版本

2020.06.26 stable_v2更新：
1. 判断是否预约成功的验证进行升级
3. 如果用户注册但是没有去过图书馆，check_my_seat函数里面的jjj数组长度为0，会出现越界错误，v2已经解决。
2. debug，每个学号必须先登陆注册图书馆账号，如果没去过图书馆直接用，会在seat那一行报错。

2020.06.27 reserve_noon_h更新：
1. 这是一个中午离馆后可以保持座位的脚本，同样需要内网运行。
2. 增加了微信提醒的功能，需要在http://wxpusher.zjiecode.com 申请自己的API和Uid。
3. 建议使用方式，中午将电脑留在图书馆，离馆前运行该程序，修改参数weizhi为自己的座位编号，(如果中午期间网络环境稳定的话)，下午来的时候可以直接看到自己的位置。
4. 该算法是离馆前不断扫描，一单离馆立刻预约，之后每隔25min取消一次并预约一次，以维持座位的预约状态。
5. 该脚本贡献者是电气77贺明康。

## 贡献者

自动画73郭王懿，电气77贺明康

**请不要用它来盈利**

个人感觉图书馆抢座位的脚本很实用，其实我挺希望把这个项目做的更完善，并且一直维护下去，不过感觉学校的系统会不断的升级，而我并不是每时每刻都有用图书馆的需求，如果有同学想要一起做下去可以来联系我，gguoguo@vip.qq.com，谢谢~
