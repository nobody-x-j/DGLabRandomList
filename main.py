import asyncio
import json
import time
import random
import websockets
from loguru import logger
import sys
from pynput import keyboard
import tracemalloc
from DIY_patterns import DIY_patterns
from config import config

tracemalloc.start()

class KeyListener:
    def __init__(self, loop, caoFanNiController, PlayList):
        self.loop = loop
        self.caoFanNiController = caoFanNiController
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.PlayList = PlayList
        self.start_time = time.time()
        self.current_time = time.time() - self.start_time
        self.RandomEventGenerator = RandomEventGenerator
        
    def get_current_time(self):
        self.current_time = time.time() - self.start_time

    def on_press(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name

        randkey_list = [                                                # 可以在这里改变randkey_list中的RandKey，从而修改通道，触发范围等等
                        RandKey("A", "early", "medium", "short"),
                        RandKey("A", "medium", "high", "medium"),
                        RandKey("A", "medium", "extrem ", "long"),
                        RandKey("both", "late", "extrem", "extrem"),
                        RandKey("both", "last", "last", "last")
        ]

        if key_name == "q" or key_name == "Q" :
            randkey = randkey_list[0]
            unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
            self.PlayList.append(unit)
        
        elif key_name == "w" or key_name == "W" :
            randkey = randkey_list[1]
            unit =self.RandomEventGenerator.generate_unit_from_key(randkey)
            self.PlayList.append(unit)
            
        elif key_name == "e" or key_name == "E" :
            randkey = randkey_list[2]
            unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
            self.PlayList.append(unit)
        
        elif key_name == "r" or key_name == "R" :
            randkey = randkey_list[3]
            unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
            self.PlayList.append(unit)
        
        elif key_name == "t" or key_name == "T" :
            randkey = randkey_list[4]
            unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
            self.PlayList.append(unit)

        elif key_name == "o" or key_name == "O" or key_name == "enter" : # 30分钟项目，每5分钟提升一档
            logger.warning("正在生成30分钟项目列表")
            while self.PlayList.playtime < 1800:
                if self.PlayList.playtime < 300:
                    randkey = randkey_list[random.randint(0,2)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 600:
                    randkey = randkey_list[random.randint(1,3)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 900:
                    randkey = randkey_list[random.randint(2,4)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 1200:
                    randkey = randkey_list[random.randint(3,4)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                else:
                    randkey = randkey_list[4]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
        
        elif key_name == "p" or key_name == "P"  or key_name == "+" : # 60分钟项目，每400秒提升一档
            logger.warning("正在生成60分钟项目列表")
            while self.PlayList.playtime < 3600:
                if self.PlayList.playtime < 400:
                    randkey = randkey_list[random.randint(0,1)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 800:
                    randkey = randkey_list[random.randint(0,2)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 1200:
                    randkey = randkey_list[random.randint(1,3)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 1600:
                    randkey = randkey_list[random.randint(2,3)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 2000:
                    randkey = randkey_list[random.randint(1,4)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 2400:
                    randkey = randkey_list[random.randint(2,4)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                elif self.PlayList.playtime < 2800:
                    randkey = randkey_list[random.randint(3,4)]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
                else:
                    randkey = randkey_list[4]
                    unit = self.RandomEventGenerator.generate_unit_from_key(randkey)
                    self.PlayList.append(unit)
        
        elif key_name == "space":
            self.PlayList.playtime = 0
            logger.warning("已重置计时器，可随时添加时间项目")
        
        logger.info(f"已成功添加列表，当前列表前10个项目{self.PlayList.playlist_show[0:9]}，列表总长{len(self.PlayList.playlist_show)}")
        
        

    def on_release(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = key.name
        if key_name in self.key_pressed:
            logger.debug(f"{key_name} key released")
            del self.key_pressed[key_name]

    async def run(self):
        try:
            while True:
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            pass

class RandKey:
    def __init__(self, channel, pattern, intensity, tick) -> None:
        if channel in ["A", "B", "both"]:
            self.channel = channel
        else:
            self.channel = "both"
        if pattern in ["early", "medium", "late", "all", "last"]:
            self.pattern = pattern
        else:
            self.pattern = "all"
        if intensity in ["low", "medium", "high", "extrem", "last"]:
            self.intensity = intensity
        else:
            self.intensity = "medium"
        if tick in ["short", "medium", "long", "extrem", "last"]:
            self.tick = tick
        else:
            self.tick = "medium"



class RandomEventGenerator:
    def __init__(self) -> None:
        pass

    def generate_unit_from_key(RandKey:RandKey):
        if RandKey.channel == "both":
            channel = "both"
        else:
            if random.uniform(0,1) < config["channel_rand"]: # 概率由单通道输出变双通道输出
                channel = "both"
            else:
                channel = RandKey.channel
        
        pattern_randnum = random.randint(0,len(config["patterns_list"][RandKey.pattern]) - 1)
        pattern = config["patterns_list"][RandKey.pattern][pattern_randnum]

        intensity = random.randint(config["intensity_range"][RandKey.intensity][0], config["intensity_range"][RandKey.intensity][1])

        tick = random.randint(config["rdm_tick_range"][RandKey.tick][0], config["rdm_tick_range"][RandKey.tick][1])

        return PlayUnit(channel, pattern, intensity, tick)

class PlayUnit:
    def __init__(self, channel, pattern, intensity, tick) -> None:
        self.channel = channel
        self.pattern = pattern
        self.intensity = intensity
        self.tick = tick

class PlayList:
    def __init__(self, caoFanNiController) -> None:
        self.caoFanNiController = caoFanNiController
        self.playlist = []
        self.playlist_show = []
        self.playtime = 0
        self.current_unit = None
        self.current_play_start_time = 0
        self.current_play_length = 0
        
    def append(self, playunit:PlayUnit):
        self.playlist.append(playunit)
        self.playlist_show.append((playunit.pattern, f"持续{playunit.tick / 10}秒", f"强度{playunit.intensity}%"))
        self.playtime += playunit.tick / 10

    def remove(self, playunit:PlayUnit):
        self.playlist.remove(playunit)
        self.playlist_show.remove((playunit.pattern, f"持续{playunit.tick / 10}秒", f"强度{playunit.intensity}%"))
    
    def play(self):
        self.current_unit = self.playlist[0]
        self.current_play_length = self.current_unit.tick / 10
        self.current_play_start_time = time.time()
        if self.current_unit.channel == "both":
            asyncio.run_coroutine_threadsafe(
                self.caoFanNiController.send_caoFanNi(self.current_unit.intensity,
                                                    self.current_unit.tick, 
                                                    self.current_unit.pattern, "A"),
                self.caoFanNiController.loop
            )
            asyncio.run_coroutine_threadsafe(
                self.caoFanNiController.send_caoFanNi(self.current_unit.intensity,
                                                    self.current_unit.tick, 
                                                    self.current_unit.pattern, "B"),
                self.caoFanNiController.loop
            )
        else:
            asyncio.run_coroutine_threadsafe(
                self.caoFanNiController.send_caoFanNi(self.current_unit.intensity,
                                                    self.current_unit.tick, 
                                                    self.current_unit.pattern, self.current_unit.channel),
                self.caoFanNiController.loop
            )
        logger.warning(f"当前输出{self.playlist_show[0]}")
        self.remove(self.current_unit)
        logger.info(f"当前等待列表前10个项目{self.playlist_show[0:9]}，列表总长{len(self.playlist_show)}")
               
    async def run(self):
        try:
            while True:
                if len(self.playlist) > 0 and time.time() > self.current_play_start_time + self.current_play_length:
                    self.play()
                else:
                    await asyncio.sleep(0.1)
                
        except KeyboardInterrupt:
            pass


class CaoFanNiController:
    def __init__(self, websocket):
        self.websocket = websocket
        self.loop = asyncio.get_event_loop()

    async def send_caoFanNi(self, i, ticks, pattern_name, channel="A"):
        if i == 61:
            print("inside")
        event = asyncio.Event()
        await self.caoFanNi(i, ticks, event, pattern_name, channel)
        await event.wait()

    async def caoFanNi(self, i, ticks, event, pattern_name, channel):
        working_channel = channel
        if not working_channel is None:
            if working_channel == "A":
                n_pattern = "A_pattern_name"
                pattern_units = "A_pattern_units"
                n_intensity = "A_intensity"
                n_ticks = "A_ticks"
            if working_channel == "B":
                n_pattern = "B_pattern_name"
                pattern_units = "B_pattern_units"
                n_intensity = "B_intensity"
                n_ticks = "B_ticks"

            logger.warning(f"通道{working_channel} 强度{i} 持续{ticks/10}秒")
            i = int(i * config["channel_level_factor"][working_channel])
            if pattern_name in list(DIY_patterns.keys()):
                await self.websocket.send(json.dumps({"cmd": "set_pattern", pattern_units: DIY_patterns[pattern_name],
                                                n_intensity: i, n_ticks: ticks}))
            else:
                await self.websocket.send(json.dumps({"cmd": "set_pattern", n_pattern: pattern_name,
                                                    n_intensity: i, n_ticks: ticks}))

        await asyncio.sleep(ticks/10)
        event.set()

    async def get_max_intensive(self):
        event = asyncio.Event()
        await self.websocket.send(json.dumps({"cmd": "get_max_intensity"}))
        max_int = await self.websocket.recv()
        self.A_max, self.B_max = eval(max_int)["A_max"],  eval(max_int)["B_max"]
        await event.wait()
    
    async def send_change_max(self, delta):
        event = asyncio.Event()
        await self.websocket.send(json.dumps({"cmd":  "change_max_intensity",  "delta_intensity":delta}))
        event.set()

async def main_fn(ws):
    try:
        logger.info(f"尝试连接至{ws}")
        async with websockets.connect(ws) as websocket:
            loop = asyncio.get_event_loop()
            logger.success("Websocket连接成功")
            caoFanNiController = CaoFanNiController(websocket)
            # war_thunder = WarThunder(websocket, caoFanNiController, loop)
            playlist = PlayList(caoFanNiController)
            key_listener = KeyListener(loop, caoFanNiController, playlist)
            # mouse_listener = MouseListener(websocket, caoFanNiController)
            # await asyncio.gather(key_listener.run(), mouse_listener.run(), war_thunder.run())  ## War Thunder 没测试过，先注释了
            await asyncio.gather(
                key_listener.run(), 
                playlist.run()
                )
    except websockets.exceptions.ConnectionClosed:
        logger.error("WebSocket连接已关闭")
    except Exception as e:
        logger.error(f"发生错误：{e}")


if __name__ == "__main__":
    logger.remove()
    handler_id = logger.add(sys.stderr, level=config["level"])
    loop = asyncio.get_event_loop()
    if loop.is_running():
        logger.debug("警告：事件循环已经在运行中")
    else:
        loop.run_until_complete(main_fn(config["ws"]))
