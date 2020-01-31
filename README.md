# IP-Proxy-Pool

I implemented it for my graduation project, [JD Distributed Crawler and Visualization System](https://github.com/fgksgf/DCVS), in order to prevent the distributed crawler from using the same IP to request the target URL frequently. 

The pool contains three sub-modules: the proxy getter, the proxy tester, and the interface module.

+ The proxy getter is responsible for regularly crawling free and high-anonymous proxies from several websites and storing them in the redis database. 

+ The proxy tester regularly checks the availability of the proxies in redis, that is, using the proxy to request a specified test link. And each proxy has a score that indicates its availability.

+ The interface module is responsible for providing APIs for external services, such as quering the number of proxies in the pool or randomly obtaining an available proxy.

**It is highly recommended that deploying this pool on a server as a independent node.**

## Usage

```bash
git clone git@github.com:fgksgf/IP-Proxy-Pool.git
docker build -t proxy-pool:0.3 .
docker run -p 5000:5000 -d proxy-pool:0.3
```

## Change Log

### 0.3 (2020-01-30)
