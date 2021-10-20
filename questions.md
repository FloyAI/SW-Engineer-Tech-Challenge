# Floy Technical Challenge

## Questions

**1. What were the reasons for your choice of API/protocol/architectural style used for the client-server communication?**
- For the API, FastAPI is a recent Python framework built on asyncio. Coupled with its light-weight nature (in terms of code written), this framework allows for faster developement especially compared to Django and Flask, the other two frameworks I've had the opportunitiy to work with. This is an advantage when dealing with a limited number of developers which results in heavier workloads being given to each individual developer.
- FastAPI starts off with HTTP protocol and can make use of other protocols such as [websockets](https://fastapi.tiangolo.com/advanced/websockets/). The former has the advantage of not needing to keep a live connection. This is an advantage if the server is going to be hosted on the cloud. In such a case, a pay-as-you-go cloud service such as GCP's [App Engine](https://cloud.google.com/appengine) would be efficient in saving costs while leaving room for scalability.
- Considering architecture, REST is an architectural pattern for API developement that's been in vogue since the early 2000s. It's main competitor is GraphQL which was released in 2015. There are several pros and cons between the [two](https://blog.api.rakuten.net/graphql-vs-rest/).
More years have been spent establishing the security protocols for REST which gives it an advantage over GraphQL. In addition, the more experience I have in REST is an advantage that will result in shorter developement time.




**2.  As the client and server communicate over the internet in the real world, what measures would you take to secure the data transmission and how would you implement them?**
- Token based authentication and a firewall rule for specific IP addresses.
- FastAPI shows how to enable [authentication](https://fastapi.tiangolo.com/tutorial/security/) in its documentation.
- Cloud service providers like [GCP](https://cloud.google.com/appengine/docs/standard/python/creating-firewalls) and AWS provide options for creating firewall rules
