[toc]
***
# IPython
+ jupyter notebook//启动jupyter notebook
+ import numpy as np//导入n科学计算库
+ import pandas as pd  
+ %matplotlib inline//设置inine方式在网页上显示图像
+ import matplotlib.pyplot as plt//导入可视化工具库
## numpy(科学计算库)基础使用
### numpy数组
#### 使用Python列表创建数组
+ b = np.array([[1,2,3],[1,2,3]])//列表创建数组
  - array中可以是列表、元组、数据将其中数据转换为Numpy数组。
  - b.ndim() //数组总维数，数字表示
  - b.shape //数组具体维数，元组表示
  - b.dtype //数组元素类型及大小，元组表示
  - b.size //数组元素个数
#### 使用numpy函数创建数组
+ np.zeros((3,4))//创建3行4列的0数组
+ np.ones((3,4))//创建3行4列的1数组
+ np.full((3,4),num)//创建3行4列的num值数组
+ np.aranges(10)//创建0-9的数组
+ np.linspace(0,1,10)//创建0-1的10个数组 
### numpy数组操作
+ **numpy数组多维时坐标用(1,2,n)表示,同时多维数组也支持切片操作a[2:,size]**
+ a = np.random.randint(10,30,9)为例
+ print(a % 2 == 0)//判断数组中元素是否为偶数, 返回布尔数组
+ a[a % 2 == 0]//返回数组中偶数元素
+ **numpy数组共享内存机制:B数组通过A数组创建修改B中的元素同时A中的元素也被修改了**
  - np.may_share_memory(a,b)//判断A、B是否共享内存
  - 基于共享内存需要创建独立的B数组:b = a[2:6].copy()
+ 可对数据整体进行操作:a = a + 1、a = a ** 2
+ %timeit a+1//测试代码运行时间
+ **数组之间的计算：维度相同，对应位置元素相加，维度不同，有一个维度相同会自动扩展维度（广播原则），扩展不行则报错。**
+ np.dot(a,b)//计算a、b的内积
+ a > b//比较a、b中元素大小缺位不比较,返回布尔数组
+ (a == b).all()//判断a、b中元素是否完全相等
+ (a == b).any()//判断a、b中元素是否至少有一个相等
+ **数组维度调整**
  - c.reshape(a,b)//将数组调整为为a行b列,**其中C为一维数组时a*b=C.size**
  - c.ravel()//将数组展开为一维数组
  - c.newaxis(2,3)//将数组调整为2行3列
  - c.transpose()//将数组转置
  - c.swapaxes(1,0)//生成副本并交换数组第1维和第0维
### numpy内置函数
#### random函数
+ **np.random.rand(a,b,size)**
  - 随机范围为a到b
  - size个数据(可为整数，也可(3,5)表示数组)
  - randint、uniform、同理
+ choice(a,b) //从数组a中随机选择b个元素,当a为整数是自动转换为range(a)数组。
+ randn//生成标准正态分布随机数
+ shuffle(a) //将数组a打乱
+ permutation(a) //将数组a生成副本打乱并返回副本
#### 常用函数
+ np.exp(a)//计算e的a次方
+ np.sqrt(a)//计算a的平方根
+ a.sum()//计算数组元素之和
  - a.sum(axis=0)//计算数组第0维元素之和
  - axis = 1//计算数组第1维元素之和
+ a.mean()//计算数组元素平均值
+ a.std()//计算数组元素标准差
+ a.min()//计算数组元素最小值,a.argmin()
+ a.max()//计算数组元素最大值,a.argmax()
+ **np.where(a > 0, 1, -1)//将数组a中大于0的元素替换为1,小于0的元素替换为-1**
+ np.sort(a)//对数组元素进行排序
  - np.sort(a,axis=0)//对数组第0维元素进行排序 
  - np.sort(a,axis=1,order='True')//对数组第1维元素进行排序,order指定排序的元素
+ **numpy多项式(Ax^0+Bx^1+...+Nx^n)**构建**
  - p = np.poly1d([1,-4,3])//创建多项式1-4x+3x^2
  - p.roots//求多项式的根
  - p.order//求多项式的阶数
  - p.coeffs//求多项式的系数
+ **集合操作函数**
  - np.unique(a)//求a中不重复的元素
    - a,num=np.unique(a,return_counts=True)//**返回A中不重复元素及其个数**
    - return_index=True//返回A中不重复元素及其索引
  - np.in1d(a,b)//求a中元素是否在b中
  - np.intersect1d(a,b)//求a、b中共同元素
  - np.setdiff1d(a,b)//求a中不在b中的元素
### panda文件操作
+ **文件类型**
  - DataFrame:数据表
  - array:list
  - series:一维数组
+ data = DataFrame(data,columns=['a','b'])//创建dataframe数据表,其中data为二维数组，columns为列名
  - data.set_index('a','b')//将a、b列设置为索引
  - data.to_csv('file.csv')//将dataframe数据表保存为csv文件
+ pd.to_XXX(path)//在path下创建文件中,XXX可为CSV、txt、sql、excel 
+ read_XXX(path)//从path下读取文件中,XXX可为CSV、txt、sql、excel 
+ read_table(path,sep='\t')//从path下读取文件sep指定分割符,**默认以tab为分割符,当分割符有多种时使用sep='\s+'**
  - 可选:header=n//从第n行读取列名,None不读取列名
  - 可选:encodeing='utf-8'//指定编码格式
  - 可选:nrows=n//读取前n行数据
  - 可选:skiprows=n//跳过前n行数据
+ cat file.npy//查看file.npy文件内容
+ %pyfile file.npy//查看file.npy文件内容
+ pd.load('file.npy')//从file.npy文件中读取数组
+ pd.loadtxt('file.txt')//从file.txt文件中读取数组
+ pd.save('file.txt',a)//将数组a保存到file.txt文件中
#### py.mysql
+ import pymysql
  - conn = pymysql.connect(host='localhost',user='root',password='123456',db='test',charset='utf8)//连接数据库
  - cursor1 = conn.cursor()//创建游标
  - cursor1.execute(sql)//执行sql语句
  - conn.close()//关闭连接
  - cursor1.close()//关闭游标
+ data = pd.read_sql('select * from table',conn)//从数据库中读取数据
#### excel文件操作
+ data = pd.read_excel('file.xlsx',header=None,names=;['name','age','id'],index_col='id')//从file.xlsx文件中读取数据
+ data.to_excel('file.xlsx',sheet_name='sheet1',index=False)//将data数据表保存到file.xlsx文件中


# matplotlib可视化
+ import matplotlib.pyplot as plt
+ plt.rc_params['font.sans-serif'] = ['SimHei']//设置字体为黑体
## 坐标轴绘制
+ plt.xlabel('name')//设置x轴标签
+ plt.ylabel('money')//设置y轴标签
+ plt.xticks()//设置x轴刻度,xticks(np.aranges(9),data.name)设置9个刻度标签
+ plt.yticks()//设置y轴刻度
+ plt.axis([xmin,xmax,ymin,ymax])//设置坐标轴范围
+ plt.xlim([xmin,xmax])//设置x轴范围
+ plt.ylim([ymin,ymax])//设置y轴范围
+ plt.xticks(rotation=45)//设置x轴刻度旋转角度,防止数据重叠
+ **图像附加**
  - plt.title(x,y,'title')//设置标题,x、y为标题位置,color为柱子颜色
  - //fontsize字体大小,rotation角度,ha/va对齐方式
  - plt.grid(True)//显示网格
  - plt.legend()//显示图例,loc=upper center指定图例居中,**ncol=3设置图例列数**
  - plt.show()//显示图像
+ 对图形进行操作
  - tuxing = plt.gcf()//获取当前图像
  - tuxing.sublots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1,hspace=0.2,wspace=0.2)
  - //调整子图位置,left、right、top、bottom为子图距离图像边缘的距离
  - //hspace、wspace为子图之间的距离
## 柱形图绘制
+ plt.bar(x,y,height=0.5,width=0.5,color='red',label='name')//绘制柱状图,
  - 其中x、y为数据,height为柱子高度,width为柱子宽度,color为柱子颜色,label为图例名称
+  图形顶部附加数值
  - plt.text(x,y,'name',ha='center',va='bottom')//可添加rotation旋转角度参数
  - //在(x,y)位置添加文本,ha(center、right、left)、va(center、top、bottom)为对齐方式
+ **堆叠柱形图**
  - plt.bar(x,y1,height=0.5,color='red',label='name1')
  - plt.bar(x,y2,bottom=y1,height=0.5,color='blue',label='name2')
  - //bottom=y1参数使y2的值在y1的基础上叠加
  - 堆积条形图: XY互换即可
## 饼图绘制
+ plt.pie(x,labels,colors,autopct='%1.1f%%',shadow=True,startangle=90)
  - //绘制饼图,x为数据,labels为标签**接收元组参数tuple**,colors=['r','b'],
  - labels  :(每一块)饼图外侧显示的说明文字；
  - explode :(每一块)离开中心距离；
  - startangle :起始绘制角度,默认图是从x轴正方向逆时针画起,如设定=90则从y轴正方向画起；
  - shadow  :在饼图下面画一个阴影。默认值：False，即不画阴影；
  - labeldistance :label标记的绘制位置,相对于半径的比例，默认值为1.1, 如<1则绘制在饼图内侧；
  - autopct :控制饼图内百分比设置,可以使用format字符串或者format function    '%1.1f'指小数点前后位数(没有用空格补齐)；
  - pctdistance :类似于labeldistance,指定autopct的位置刻度,默认值为0.6；
  - radius  :控制饼图半径，默认值为1；counterclock ：指定指针方向；布尔值，可选参数，默认为：True，即逆时针。将值改为False即可改为顺时针。wedgeprops ：字典类型，可选参数，默认值：None。参数字典传递给wedge对象用来画一个饼图。例如：wedgeprops={'linewidth':3}设置wedge线宽为3。
  - textprops ：设置标签（labels）和比例文字的格式；字典类型，可选参数，默认值为：None。传递给text对象的字典参数（fontsize/color）。
  - center ：浮点类型的列表，可选参数，默认值：(0,0)。图标中心位置。
  - frame ：布尔类型，可选参数，默认值：False。如果是true，绘制带有表的轴框架。
  - rotatelabels ：布尔类型，可选参数，默认为：False。如果为True，旋转每个label到指定的角度。

## 折线图绘制
+ plt.plot(x, y, **kwargs)
  - x,y:接收array型数据
  - color：'r'、'g'、'y'、'k'(黑)、'w'、'b'(蓝)
  - marker:折线形状:点标记：'.' 点标记,',' 像素标记(极小点),'o' 实心圈标记,'v' 倒三角标记,'^' 上三角标记,'>' 右三角标记,'<' 左三角标记...等等
  - linestyle:风格字符：'‐' 实线,,'‐‐' 破折线'‐.' 点划线,':' 虚线,'' ' ' 无线条
  - lineweidth:线条宽度,1.2
  - lablel:标签,"time"
  - aplha:透明度,0-1
+ 多条折线图绘制：
  - plt.plot(x,y1,color='r',label='name1')
  - plt.plot(x,y2,color='b',label='name2')
+ 平均线绘制
  - plt.axline(y=y1.mean(),color='r',linestyle='--',label='name1')
    //y1.mean()为y1的平均值
+ 画布与字图
  - fig=plt.figure()//创建画布
    - num:画布编号,默认递增
    - figsize:画布大小,默认(6.4,4.8)
    - dpi:分辨率,默认100
    - facecolor:背景颜色,默认'w'
    - edgecolor:边框颜色,默认'k'
    - frameon:是否显示边框,默认True 
  - plt.subplot(2,1,1)//添加子图,2行1列,第一个子图
    plt.pie(x,y,colors='r',label='name1')//绘制第一个子图
  - plt.subplot(211)//添加子图,2行1列,第二个子图
  - plt.subplot()
    - nrows:  行数
    - ncols: 列数
    - sharex: 共享x轴
    - sharey: 共享y轴
    - subplot_kw: 传递给add_subplot()的关键字参数
  - subplots_adjust(self, left)子图与画布位置调整
    - left:  左边界位置,0-1
    - bottom:  下边界位置,0-1
    - right:  右边界位置,0-1
    - top:  上边界位置,0-1
    - wspace:  列间距,0-1
    - hspace:  行间距,0-1
  + 条形图与折线图组成组合图：同一个图上画两个即可。
  + 图上日期标注：plt.xticks(dates,roation=45)
  + 网格线:plt.grid()
    - b : 布尔值。就是是否显示网格线的意思。
    - which : 取值为’major’, ‘minor’， ‘both’。 默认为’major’。
    - axis : 'x','y'。指定显示网格线轴,不指定就是x,y轴的网格线。
    - color : 设置网格线的颜色。
    - linestyle :设置网格线的风格，是连续实线，虚线或者其它不同的线条。
    - linewidth : 设置网格线的宽度 
  
# 实验
```python
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 假设你的 CSV 数据已经读入到一个数组 data
path = "C:\\Users\\杨雨糯\\Downloads\\directory.csv"
data = pd.read_csv(path)

# 输出数据查看
print(data)

# 提取国家和城市列的数据
countries = data['Country']  # 使用列名直接提取
cities = data['City']

# 统计不同国家的门店数量
unique_countries, country_counts = np.unique(countries, return_counts=True)

# 统计中国不同城市的门店数量
chinese_cities = cities[countries == 'China']  # 使用布尔索引
unique_chinese_cities, chinese_city_counts = np.unique(chinese_cities, return_counts=True)

# 绘制不同国家的门店数量柱状图
plt.figure(figsize=(10, 6))  # 可以设置图形大小
plt.bar(unique_countries, country_counts)
plt.xlabel('Country')
plt.ylabel('Number of Stores')
plt.title('Starbucks Stores by Country')
plt.xticks(rotation=45,fontsize=6)  # 旋转x轴标签以便更好显示
plt.tight_layout()  # 自动调整布局以避免标签重叠
plt.show()

# 绘制中国不同城市的门店数量柱状图
plt.figure(figsize=(10, 6))  # 可以设置图形大小
plt.bar(unique_chinese_cities, chinese_city_counts)
plt.xlabel('City in China')
plt.ylabel('Number of Stores')
plt.title('Starbucks Stores in Chinese Cities')
plt.xticks(rotation=45)  # 旋转x轴标签以便更好显示
plt.tight_layout()  # 自动调整布局以避免标签重叠
plt.show()
```