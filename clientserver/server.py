
import json
import asyncio
import websockets
import time
import init
from StoppableThread import *
from CameraControlInterface import *
from Autofocus import *

cameraQueue = asyncio.Queue()

async def websocketListen(websocket):
    return await websocket.recv()

async def cameraListen(queue):
    return await queue.get()    

async def handler(websocket, path):

    with usb1.USBContext() as usbcontext:
        with CameraControlInterface(usbcontext) as cameracontrol:
            cameracontrol.setNotificationQueue(asyncio.get_running_loop(), cameraQueue)

            while True:
                taskWebsocketListen = asyncio.create_task(websocketListen(websocket))
                taskCameraListen = asyncio.create_task(cameraListen(cameraQueue))
                done, pending = await asyncio.wait([taskWebsocketListen, taskCameraListen], return_when=asyncio.FIRST_COMPLETED)
                result = await (list(done)[0])
                list(pending)[0].cancel()
                if taskWebsocketListen in done:
                    Logger.LogInfo("websocket task completed - received data {}".format(result))
                    websocketdata = json.loads(result)
                    if websocketdata['action'] == 'autofocus':
                        autofocusparams = websocketdata['value']
                        autofocus(cameracontrol, autofocusparams['y'], autofocusparams['x'])
                        await websocket.send(json.dumps({'action': 'autofocus', 'result': 'DONE'}))
                    else:
                        camerafunc = getattr(cameracontrol, websocketdata['action'])
                        camerafunc(websocketdata['value'])
                if taskCameraListen in done:
                    Logger.LogInfo("camera completed - will send back to user {}".format(result))  
                    await websocket.send(json.dumps(result))
    
start_server = websockets.serve(handler, "localhost", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
