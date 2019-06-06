FROM python:3
RUN pip install requests 
RUN pip install aiohttp
ADD Process_Server.py / 
CMD [ "python", "./Process_Server.py" ]