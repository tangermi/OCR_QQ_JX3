from nonebot import on_command, CommandSession
import glob
import os
import re
from nonebot.command.argfilter.extractors import extract_image_urls
import urllib.request
from ocr_search import run


# on_command 装饰器将函数声明为一个命令处理器
# 这里 exam 为命令的名字，同时允许使用别名「科举」「科举考试」
@on_command('科举', only_to_me=False, aliases=('科举考试','exam'))
async def exam(session: CommandSession):
    # 从会话状态（session.state）中获取问题名称（question），如果当前不存在，则询问用户
    question = session.get('question', prompt='把题目截图给我看看')
    # 问题的答案
    exam_report = await get_answer_of_question(question)
    # 向用户发送答案
    await session.send(exam_report)

# exam.args_parser 装饰器将函数声明为 exam 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@exam.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_images

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：科举 [图片]
            session.state['question'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的问题截图（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的题目不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的问题），且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg


async def get_answer_of_question(question: str) -> str:
    # 这里简单返回答案
    urllib.request.urlretrieve(question[0], "question.jpg")
    answer = run('question.jpg')
    if len(answer.strip())<1:
        return '对不起，没有找到答案'
    return f'{answer}'