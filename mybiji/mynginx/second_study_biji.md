https://www.bilibili.com/video/BV1yS4y1N76R

# 开始

常用版本分为：
1、nginx开源版。nginx官网   nginx.org
2、nginx plug 商业版    nginx.com  
3、openresty    openresty.org
4、tengine      tengine.taobao.org

nginx源码编译安装
--prefix是安装的时候配置的安装路径(通过压缩包的源码安装)。在./configure的后面进行配置的。

make

make instatll

temp结尾的文件夹不是安装后产生的，是nginx启动后产生的。

![1679144489067](D:\mybiji\mynginx\img\1679144489067.png)



运行原理

![1679145702445](D:\mybiji\mynginx\img\1679145702445.png)



基本的请求流程：用户通过网络请求，worker进程去解析请求。



## nginx配置



## 虚拟主机与域名解析

![1679153650211](D:\mybiji\mynginx\img\1679153650211.png)

![1679153671381](D:\mybiji\mynginx\img\1679153671381.png)

公司使用阿里云的域名配置与解析。可以设置子域名进行配置。就是一个域名可通过设置子域名去解析到不同的服务器上。



### servername 匹配规则

![1679204168126](D:\mybiji\mynginx\img\1679204168126.png)

可以在同一个server的servername中设置多个域名。

前面的server中如果匹配上了，就不会再向后匹配了。

书写配置文件有先后顺序，如果都没匹配上，会显示第一个。

可以使用 * (通配符) 进行匹配。

例如： *.toyverse.club。 不管前面是什么，都可以匹配到。

































