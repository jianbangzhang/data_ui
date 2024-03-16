#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/12/12 11:30
# @Author  : 建邦
# @org     : whu
# @Site    :
# @File    : app_ui.py
# @Software: PyCharm

import gradio as gr
from argparse import ArgumentParser
from fastapi import FastAPI
import time
from src.api import Api
import os




parser = ArgumentParser()
parser.add_argument("--port", type=int, default=9003, help="port")
args, unknown_args = parser.parse_known_args()




from src import show_data_by_id,show_data_detail,convert_json_data


def sstalker_demo():
    with gr.Blocks(analytics_enabled=False) as sstalker_interface:
        with gr.Row():
            gr.HTML('<center style="font-size: 20px;"><b>数据中心</b></center>')
        with gr.Row():
            gr.HTML('<p style="font-size: 15px; text-align: left;">作者：jbzhang15</p>')

        with gr.Tab("读取Json原始数据"):
            with gr.Row().style(equal_height=False):
                with gr.Column(variant='panel'):
                    with gr.Row():
                        mode=gr.Radio(['mode1', 'mode2'], value="mode1", label="Json文件的格式",info="mode1=List[Dict],mode2=Dict").style(width=512)
                    with gr.Tabs(elem_id="数据展示"):
                        with gr.TabItem('数据的路径和ID'):
                            data_id = gr.Number(label='ID')
                            json_path = gr.Text(label="JSON_Path")
                            submitJsonAPI = gr.Button('处理', elem_id="sstalker_generate", variant='primary')
                            one_data_show = gr.TextArea(label="处理结果").style(width=512)

                    submitJsonAPI.click(
                        fn=show_data_by_id,
                        inputs=[mode,json_path,data_id],
                        outputs=[one_data_show]
                    )

        with gr.Tab("读取Json数据的细节"):
            with gr.Row().style(equal_height=False):
                with gr.Column(variant='panel'):
                    with gr.Row():
                        mode=gr.Radio(['mode1', 'mode2'], value="mode1", label="Json文件的格式",info="mode1=List[Dict],mode2=Dict").style(width=512)
                    with gr.Tabs(elem_id="数据展示"):
                        with gr.TabItem('数据的路径和ID'):
                            data_id = gr.Number(label='ID')
                            json_path = gr.Text(label="JSON_Path")
                            submitJsonAPI = gr.Button('处理', elem_id="sstalker_generate", variant='primary')
                            one_data_show = gr.TextArea(label="处理结果").style(width=512)

                    submitJsonAPI.click(
                        fn=show_data_detail,
                        inputs=[mode,json_path,data_id],
                        outputs=[one_data_show]
                    )

        with gr.Tab("转化Json数据，查看交互数据过程"):
            with gr.Row().style(equal_height=False):
                with gr.Column(variant='panel'):
                    with gr.Row():
                        mode=gr.Radio(['mode1', 'mode2'], value="mode1", label="Json文件的格式",info="mode1=List[Dict],mode2=Dict").style(width=512)
                    with gr.Row():
                        save_file_format=gr.Radio(['xlsx', 'csv'], value="xlsx", label="转化Json文件的格式",info="可以保存为xlsx和csv两种格式").style(width=512)
                    with gr.Tabs(elem_id="数据路径"):
                        with gr.TabItem('数据的路径和ID'):
                            json_path = gr.Text(label="JSON_Path")
                            cur_dir=os.path.dirname(os.path.abspath(__file__))
                            save_path=gr.Text(label=f"默认保存的路径:{cur_dir}")
                            submitJsonAPI = gr.Button('处理', elem_id="sstalker_generate", variant='primary')
                            msg_data_show = gr.TextArea(label="处理结果").style(width=512)

                    
                    submitJsonAPI.click(
                        fn=convert_json_data,
                        inputs=[mode,json_path,save_file_format,save_path],
                        outputs=[msg_data_show]
                    )
    return sstalker_interface





# pm2 start app_did.py --name saddid --interpreter python3  -- --port=9003
if __name__ == "__main__":

    demo = sstalker_demo()
    # demo.queue(max_size=10, api_open=True)

    if not hasattr(FastAPI, 'original_setup'):
        def fastapi_setup(self):
            self.docs_url = "/docs"
            self.redoc_url = "/redoc"
            self.original_setup()


        FastAPI.original_setup = FastAPI.setup
        FastAPI.setup = fastapi_setup
    
    def wait_on_server(api):
        while 1:
            if api.status == "stop":
                break
            time.sleep(2)

    app, local_url, share_url = demo.launch(debug=False, server_name="0.0.0.0", 
                                            server_port=args.port,
                                            prevent_thread_lock=True,
                                            show_error=True, 
                                            show_tips=True, 
                                            quiet=False, 
                                            show_api=True)
    print(f'demo app ')

    app.user_middleware = [x for x in app.user_middleware if x.cls.__name__ != 'CORSMiddleware']
    api = Api(demo, app)
    print(f'create api success')
    wait_on_server(api)
    demo.close()

