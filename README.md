# IP-Proxy-Pool

I implemented it for my graduation project, [JD Distributed Crawler and Visualization System](https://github.com/fgksgf/DCVS), in order to prevent the distributed crawler from using the same IP to request the target URL frequently. 

The pool contains three sub-modules: the proxy getter, the proxy tester, and the interface module.

+ The proxy getter is responsible for regularly crawling free and high-anonymous proxies from several websites and storing them in the redis database. 

+ The proxy tester regularly checks the availability of the proxies in redis, that is, using the proxy to request a specified test link. And each proxy has a score that indicates its availability.

+ The interface module is responsible for providing APIs for external services, such as quering the number of proxies in the pool or randomly obtaining an available proxy.

**It is highly recommended that deploying this pool on a server as a independent node.** _Notably, this proxy pool only crawls China proxies._

## Usage

```bash
$ git clone https://github.com/fgksgf/IP-Proxy-Pool.git
$ cd IP-Proxy-Pool/

# set your own password of redis
$ vim redis.conf
$ vim proxypool/settings.py

# set your absolute path of IP-Proxy-Pool/ on line 17
$ vim docker-compose.yml

$ docker-compose up -d
```

Then you can use `docker logs <container id>` to check logs. For checking proxies, you can connect redis at 127.0.0.1:6379 via redis GUI tools.

### API

You can access `127.0.0.1:5000` to get these services:

+   `/random`: get a random proxy in the pool.
+   `/batch`: get all currently available proxies.
+   `/count`: get the number of proxies.

## Change Logs

### 1.1 (2020-02-12)

+ Mount code directory rather than copy code into docker image
+ Modify logger format
+ Change logger name
+ Add test methods for database
+ Enhance exception handler
+ Use lock to prevent getter and tester working simultaneously

### 1.0 (2020-02-01)

+   Use docker compose
+   Add more detailed comments
+   Update proxy crawlers
+   Add test methods for crawlers
+   Update python packages