---
layout: post
title: Web Server Gateway Interface (wsgiref.util部分)
category: 学习笔记
tags: 编程， Python，WSGI
---
<img src="/static/blog/img/project/20160811/0.jpg" alt="django" style="width:100%;"/>
### WSGI Utilities and Reference Implementation
　　WSGI是一个介于web服务器与Python应用程序之间的标准接口，采用标准接口可以使应用程序方便的在各个web服务器间复用和移植。

　　只有web服务器工程师和软件框架的作者才需要了解和关心WSGI设计的每个细节，对于应用层来讲，只需要遵循WSGI协议来安装和使用现有的框架去编写网络程序就够了。wsgiref提供WSGI环境变量以及HTTP header的回复等的各种操作方法，以及性能评测工具。

## wsgiref.util – WSGI environment utilities
　　此模块包含操作WSGI环境变量的众多方法。WSGI环境变量是一个包含HTTP请求参数的dict，处理函数要使用一个*environ* 的参数来接收它。

* __wsgiref.util.guess_scheme(*environ*)__

	返回```wsgi.url_scheme```为“http”还是“https”，它是通过检查*environ* dict中的“HTTP”环境变量来实现的。返回值为string类型。

	此方法在创建一个CGI或CGI类（比如FastCGI）协议的装饰器时非常有用。比如服务器在收到基于SSL的请求时，在协议中会包含一个“HTTPS”的变量，其值为“1”、“yes”或“on”等，那么使用此方法将会返回一个“https”，否则就是“http”。


* __wsgiref.util.request_uri(*environ, include_query=1*)__

	返回完整的请求的URI，通过*include_query* 参数来决定是否包含query string。判定算法使用的是PEP 333中的”URL Reconstruction“。


* __wsgiref.util.application_uri(*environ*)__

	与request_uri方法类似，但这里忽略了PATH_INFO和QUERY_STRING变量。结果就是请求的应用程序对象地址的base URI。


* __wsgiref.util.shift_path_info(*environ*)__

	从PATH_INFO中移出一个单词到SCRIPT_NAME，并且将之返回。*environ* 将会以空格填补，如果需要的话必须先保存原始的PATH_INFO和SCRIPT_NAME变量。

	如果PATH_INFO再没有可以移出的部分，执行此方法就会返回一个None。

	典型情况，一个需求要处理请求URI路径的每个部分，比如遍历一系列的dict的键来修改传入的环境使其适合调用另一个位于目标URI的WSGI程序。比如，有一个WSGI程序位于/foo，而请求的URI路径是/foo/bar/baz，那么位于/foo的应用程序调用 ```shift_path_info()```，将会返回"bar"。然后环境将更新来适配位于/foo/bar的WSGI应用程序。这样一来，SCRIPT_NAME将会从/foo变成/foo/bar，PATH_INFO将从/bar/baz变成/baz。

	当PATH_INFO只剩“/”，就返回一个空的string并且给SCRIPT_NAME追加一个反斜杠，即便是空的路径被忽略或者SCRIPT_NAME没有正常的终止于反斜杠。这是故意设置的，来确保在对象遍历时应用程序能够区分以“/x/”和“/x”结尾的URI。


* __wsgiref.util.setup_testing_defaults(*environ*)__

 通过默认值来更新*environ*变量，用于测试用途。

 这个路由添加多个用于请求WSGI的参数，包括HTTP_HOST、SERVER_NAME、SERVER_PORT、REQUEST_METHOD、SCRIPT_NAME、PATH_INFO和所有在PEP 333中定义的以“wsgi.”开头的变量。只支持默认的值，并且不会替换他们当中任何已经存在的设定值。

 此方法主要用来方便的模拟一个环境用于单元测试。由于数据是模拟的，所以不应用于生产服务器和应用程序中。

 一个示例：
        from wsgiref.util import setup_testing_defaults
        from wsgiref.simple_server import make_server

        # A relatively simple WSGI application. It's going to print out the
        # environment dictionary after being updated by setup_testing_defaults

        def simple_app(environ, start_response):
            setup_testing_defaults(environ)

            status = '200 OK'
            headers = [('Content-type', 'text/plain')]

            start_response(status, headers)

            ret = ["%s: %s\n" % (key, value) for key, value in environ.iteritems()]
            return ret
        httpd = make_server('', 8000, simple_app)
        print "Serving on port 8000..."
        httpd.serve_forever()

	除了上述功能，wsgiref.util还提供了一些杂项工具：

* __wsgiref.util.is_hop_by_hop(*header_name*)__

	如果“‘header_name”是RFC 2616中定义的HTTP/1.1 “Hop-by-Hop” header，则返回True。


* ___class___ wsgiref.util.__FileWrapper(*filelike, blksize=8192*)__

	一个装饰器，用来把file-like对象转换成一个迭代器，返回的对象支持```__getitem__()```和```__iter__()```两种循环风格。当对象迭代时，可选的*blksize*参数将被传入file-like对象的```read()```方法中用来获取产生的字符串。```当read()```方法返回一个空字符串时，迭代结束，且此对象不可恢复。

	如果file-like对象有一个```close()```方法，那么转换后的对象依然有一个```close()```方法，并且在调用这个对象的```close()```方法时触发file-like对象的```close()```方法。

	示例：

		from StringIO import StringIO
		from wsgiref.util import FileWrapper

		# We're using a StringIO-buffer for as the file-like object

		filelike = StringIO("This is an example file-like object"*10)
		wrapper = FileWrapper(filelike, blksize=5)

		for chunk in wrapper:
		    print chunk

