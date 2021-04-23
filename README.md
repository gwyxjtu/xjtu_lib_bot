# xjtu_lib_bot
西安交通大学图书馆预约抢座位脚本（占座脚本随着图书馆预约规则的改变已经失效）

## 使用方法

在config中修改用户名和密码,personid是学号，password是密码，username是netid号码，seat_id和region分别是座位号和座位区域，cookie和headers不需要修改。座位参数详见后面参数表


修改完config.json成后直接运行reserve.py，或者修改主函数中的日期调整到第二天，并在夜间保证电脑开机，可以在第二天早上五点五十五抢到座位。

**如果座位号seat_id为空则随即预约当前region的一个座位。**



## 图书馆区域以及座位参数表

|  图书馆区域   | region  | seat_id|
|  ----  | ----  | ---- |
|北楼二层外文书库东|north2east| D001-D168 and E001-E168|
|北楼二层外文书库西|north2west| N001-N120|
|南楼二层大厅|south2| C01-C99|
|二层连廊流通大厅|north2elian| A01-A88 and B01-B88|
|北楼三层ilib西|west3B| Y001-Y132|
|北楼三层ilib东|east3A| X001-X132|
|南三|south3middle| 001-152|
|北四楼西侧|north4west| K001-K084 and L001-L168 and M001-M072|
|北四楼中间|north4middle| J001-J144|
|北四楼东侧|north4east| F021-F120 and G001-G072 and H001-H160|
|北四楼西南|north4southwest| 001-136|
|北四楼东南|north4southeast| 001-136|


## 示例config

    "username": "netid",
    "password": "netid密码",
    "person_id":"学号",
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    },
    "cookies": {},
    "seat_id":"D001",
    "region":"north2east"


预约的是北楼二层外文书库东的D001座位。


**脚本运行环境必须校内网络，可以宿舍或者STUwifi**


**请不要用它来盈利**

个人感觉图书馆抢座位的脚本很实用，其实我挺希望把这个项目做的更完善，并且一直维护下去，不过感觉学校的系统会不断的升级，而我并不是每时每刻都有用图书馆的需求，如果有同学想要一起做下去可以来联系我，gguoguo@vip.qq.com，谢谢~
