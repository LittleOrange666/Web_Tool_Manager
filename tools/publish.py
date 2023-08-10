import queue
import subprocess
import time
import threading
import pyshorteners
from pyshorteners.exceptions import ShorteningErrorException


def output_reader(proc, outq):
    for line in iter(proc.stdout.readline, b''):
        outq.put(line.decode("big5"))


class Publisher:
    def __init__(self, link, tunnel_name, static_link):
        print("Publisher=>" + link)
        cmd = "cloudflared tunnel --url " + link
        if tunnel_name is not None:
            cmd += " --name " + tunnel_name
        self.proc = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        self.outq = queue.Queue()
        if static_link is None:
            self.t = threading.Thread(target=output_reader, args=(self.proc, self.outq))
            self.t.start()
            self._url = ""
            self._completed = False
            self.sus = 0
        else:
            self._url = static_link
            self._completed = True
            self.sus = 0

    def check(self):
        while not self.outq.empty() and not self._completed:
            line = self.outq.get(block=False)
            print(line, end="")
            if "Connection" in line:
                self.sus += 1
            if ".trycloudflare.com" in line:
                self._url = line[line.find("https:"):line.find(".trycloudflare.com") + len(".trycloudflare.com")]
                self._completed = True
            if self.sus == 4:
                self.sus = 0
                self._completed = True

    def geturl(self):
        if not self._url:
            self.check()
        return self._url

    def is_completed(self):
        if not self._completed:
            self.check()
        return self._completed

    def wait_completed(self, delay=0.3):
        while not self._completed:
            self.check()
            time.sleep(delay)

    def close(self):
        self.proc.terminate()
        self.t.join()


class ToolManager:
    __slots__ = ("cmd", "port", "url", "shorturl", "running", "publisher", "process", "tunnel_name", "static_link",
                 "auto_start", "name", "wait_ok", "t")

    def __init__(self, name: str, cmd: str, port: int, tunnel_name: str | None = None, static_link: str | None = None,
                 auto_start: bool = False):
        self.cmd = cmd
        self.port = port
        self.running = False
        self.url = None
        self.shorturl = None
        self.publisher = None
        self.process = None
        self.wait_ok = False
        self.auto_start = auto_start
        self.tunnel_name = tunnel_name
        self.static_link = static_link
        self.name = name
        if auto_start:
            self.start()

    def output_reader(self):
        while True:
            for line in iter(self.process.stdout.readline, b''):
                line_str = line.decode("big5")
                if self.wait_ok:
                    if f"127.0.0.1:{self.port}" in line_str:
                        self.wait_ok = False
                print(self.name + "> " + line_str, end="")
            time.sleep(0.3)

    def _start(self):
        self.process = subprocess.Popen(self.cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
        self.t = threading.Thread(target=self.output_reader)
        self.t.start()

    def wait_completed(self, delay=0.3):
        while self.wait_ok:
            time.sleep(delay)

    def start(self):
        if not self.running:
            self.running = True
            self.wait_ok = True
            self._start()
            self.publisher = Publisher("http://127.0.0.1:" + str(self.port), self.tunnel_name, self.static_link)

    def stop(self):
        if self.running:
            self.publisher.close()
            self.process.terminate()
            self.url = None
            self.shorturl = None
            self.publisher = None
            self.process = None
            self.running = False
            self.wait_ok = False

    def restart(self):
        if self.running:
            self.process.terminate()
            self._start()
            self.wait_ok = True

    def isrunning(self):
        return self.running

    def geturl(self):
        if self.url is None:
            if self.publisher is not None:
                self.url = self.publisher.geturl()
        return self.url

    def getshorturl(self):
        if self.shorturl is None:
            url = self.geturl()
            if url is not None:
                try:
                    self.shorturl = pyshorteners.Shortener().isgd.short(url)
                except ShorteningErrorException as e:
                    print("ShorteningErrorException: " + e)
        return self.shorturl
