# 分布式爬虫框架 

### 一 目的 

实现一个有关google地图信息的分布式爬虫框架

### 二 功能 

- [x]  爬取google地图信息
- [x] 分布式

### 三 设计思想  

```


                                task                              
         redis/rabbitMQ/kaffa/  ===>    application.queue  ===>  handler(app, task)
                                     返回结果过滤后重新放进队列  <==    得到结果




```





### 四 使用的技术栈  

- python 3.8+ (作者的版本是3.11)
- asyncio
- playwright
- SQLAlchemy 
- pika(RabbitMQ)

### 五 开发有关  

- 克隆代码 

  ```
  git clone ....
  ```

- 目录 

  ```
  -----babikill 
    |------biubiu      #框架主要代码 
    |    |——application.py 
    |    
    |------example     #例子代码   
  ```

  

- 创建虚拟环境 

- 安装依赖库 

  ```
  cd babikill
  pip install -r requirements/dev.txt 
  
  # 安装依赖库后，需要安装 playwright相关浏览器，参考https://playwright.dev/python/docs/intro
  playwright install
  
  ```

  

- 运行例子 

  ```
  cd babikill/example
  python main.py
  ```

  
  
- 关于如何实现分布式  

  - 1 需要创建实现loop异步方法的一个类，参考 $项目目录/biubiu/starters.py 例如： 

    ```
    class PikaConsumerStarter:
         async def loop():
              # 
              pass
    ```

    

  - 2 初始化，并调用 application对象的add_starter方法加到application对象里 

    ```
    app = Application(worker_id='test-01', scope_context_manager=startup)
    # 分布式Starter
    pika_starter = PikaConsumerStarter('amqp://guest:guest@localhost:5672/%2F', app)
    app.add_starter(pika_starter)
    ```

    

  

### 六 效果图  

![](data/2.png)

![](data/1.png)





