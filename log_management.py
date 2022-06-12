import os
import time
from time import strftime


def get_document_path(current_dir, doc_name):
    """
    生成日志文件的路径
    :param doc_name: string
        日志文件的名字
    :param current_dir: string
        系统文件的目录
    :return: string
        日志文件的绝对位置
    """
    doc_path = '\\log\\{}.txt'.format(doc_name)
    file_path = current_dir + doc_path
    return file_path


class log_management:
    def __init__(self, current_dir=os.path.dirname(os.path.abspath(__file__)), doc_name=strftime("%Y-%m-%d %H'%M'%S")):
        """
        初始化
        :param current_dir: string
            日志信息的目录，默认目录是当前py文件的目录地址
        :param doc_name: string
            日志信息的文件名，默认文件名称是年月日+时间
        """
        self._document_path = get_document_path(current_dir, doc_name)  # 当前存储文件的路径

    def write_data(self, *args):
        """
        把事件写入到日志文件中
        :param args: 需要写入的信息
        :return: None
        """
        if not os.path.exists(os.path.dirname(self._document_path)):  # 如果文件目录不在，则创建目录
            os.mkdir(os.path.dirname(self._document_path))
        for arg in args:  # 依次写入信息
            with open(self._document_path, 'a+') as f:
                data = strftime("%Y-%m-%d %H:%M:%S") + '\t' + arg + '\n'
                f.write(data)
        return None

    @property
    def data(self):
        with open(self._document_path, 'r') as f:
            data = f.read()
        return data

    @property
    def today_data(self):
        today_data = ''
        with open(self._document_path, 'r') as f:
            for data in f.readlines():
                if time.strftime("%Y-%m-%d") in data:
                    today_data = today_data + data
                else:
                    pass
        return today_data

    @property
    def document_path(self):
        return self._document_path


if __name__ == '__main__':
    obj = log_management()
    obj.write_data('测试信息1', '测试信息2')
