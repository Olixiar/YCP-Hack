# Issues Encountered While Setting Up LLM Chatbot Using DataBricks

 From the Databricks starter application repo, we chose the databricks_DBRX_website_bot to be used in one of the other sponsored challenges to generate recommendations
 to collaborate based on tags for students, faculty, and partners of YCP. 

 When starting, we had planned to use the example code and modify parts of it to work for our datasets. However, when pip install -r requirements.txt
 we ran into issues with the dependencies conflicting with other dependencies needed in the project. 

 My Python version was (somehow) too new of a version, and when trying to downgrade, ran into other issues with git bash.

 we ultimately decided to switch to github codespaces in hopes that it would be able to handle the conflicting dependencies as we would be isolating the example code outside of our project. When running the code, we were able to successfully train the LLM, and were in the process of loading the sdxl model. 

 The error is as follows:

 Exception ignored in: <module 'threading' from '/usr/local/python/3.12.1/lib/python3.12/threading.py'>
Traceback (most recent call last):
  File "/usr/local/python/3.12.1/lib/python3.12/threading.py", line 1623, in _shutdown
    lock.acquire()
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/streamlit/web/bootstrap.py", line 44, in signal_handler
    server.stop()
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/streamlit/web/server/server.py", line 417, in stop
    self._runtime.stop()
  File "/usr/local/python/3.12.1/lib/python3.12/site-packages/streamlit/runtime/runtime.py", line 324, in stop
    async_objs.eventloop.call_soon_threadsafe(stop_on_eventloop)
  File "/usr/local/python/3.12.1/lib/python3.12/asyncio/base_events.py", line 837, in call_soon_threadsafe
    self._check_closed()
  File "/usr/local/python/3.12.1/lib/python3.12/asyncio/base_events.py", line 539, in _check_closed
    raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
terminate called without an active exception
Aborted (core dumped)



When looking for the source of the issue, and trying to understand why there was a RuntimeError, Google(and other sources) stated that our runtime error was due to working with asynchronous code and having the event loop ending too early. We spent more time trying to find the source of the event loop ending prematurely, but were unable to find the issue.