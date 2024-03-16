import os
import gradio as gr
from fastapi import FastAPI, APIRouter
import gradio as gr
import logging

logging.basicConfig(level=logging.INFO)


class Api:
    def __init__(self, demo: gr.Blocks, app: FastAPI):

        self.router = APIRouter()
        self.app = app
        self.demo = demo
        self.status = "start"
        self.app.add_api_route("/ping",  self.ping, methods=["GET"])
        self.app.add_api_route("/restartall", self.restartall, methods=["GET"])
        self.app.add_api_route("/stop", self.stop, methods=["GET"])


    def ping(self):
        return {"ping": "pong"}
    
    def stop(self):
        self.status = "stop"
        return {}

    def restartall(self):
        self.status = "stop"
        os.system("pm2 restart all")
        return {}

   