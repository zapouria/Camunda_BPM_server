import aiohttp
import asyncio
import time

async def main():
    session = aiohttp.ClientSession()
    while True:
        #Get the mandatory data(workerid,topicName and etc) for fetchAndLock

        resp = await session.get("http://5.189.228.43:8080/engine-rest/external-task/")
        if resp.status == 204:
            resp.close()
            break
        #Check if there is any external task
        if await resp.json():
            time.sleep(1)
            parsedJson =await resp.json()
            id = parsedJson[0]["id"]
            workerid = parsedJson[0]["workerId"]
            #In case workerid is not assigned, None is not acceptable for server
            if workerid == None:
                workerid=""
            topicName = parsedJson[0]["topicName"]
            
            #POST fetchAndLock

            url = 'http://5.189.228.43:8080/engine-rest/external-task/fetchAndLock/'
            task = {
                "workerId":workerid,
                "maxTasks":2,
                "usePriority":"true",
                "topics":
                    [{"topicName": topicName,
                    "lockDuration": 10000,
                    "variables": ["orderId"]
                    }]
                }
            resp = await session.post(url, json = task)
            print(resp.status)
            print(await resp.text())

            #Complete the process

            url = 'http://5.189.228.43:8080/engine-rest/external-task/' + id + '/complete'
            task = {
                    "workerId": workerid,
                    "variables":
                        {}
                }
            resp = await session.post(url, json = task)
            print(resp.status)
            print(await resp.text())
    session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
