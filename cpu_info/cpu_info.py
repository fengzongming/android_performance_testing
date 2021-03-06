import os
import csv
import time
import configparser


class App(object):
    def __init__(self):
        # 保存执行完命令的内容
        self.content = ""

        # 保存cpu占用
        self.cpu_info = 0

        # 选择读取的配置文件(直接在这里输入文件名即可, 不要加上文件类型)
        self.config = "cpu_info_xiaoma_music"

        # 保存adb命令
        app_information = self.read_config()
        self.cpu_command = app_information[0]
        self.app_package = app_information[1]

    # 读取配置文件
    def read_config(self):
        # 读取配置文件的内容
        config = configparser.ConfigParser()
        config.read('config/' + self.config + '.ini')
        cpu_command = config.get('command', 'cpu_command')
        app_package = config.get('package', 'app_package')

        return cpu_command, app_package

    # 使用cpu监控命令
    def use_cpu_command(self):
        command = self.cpu_command + " " + "| findstr " + self.app_package
        self.content = os.popen(command)

    # 获取启动时间
    def get_cpu_info(self):
        for line in self.content.readlines():
            if "%" in line:
                self.cpu_info = line.split("%")[0]
                break
        return self.cpu_info


# 控制器类, 用于控制app的执行次数和统计启动时间
class Controller(object):
    def __init__(self, count=3):
        # 获取要执行的app
        self.app = App()

        # 获取需要循环执行的次数
        self.count = count

        # 获取app的当前时间戳和启动时间
        self.all_data = [("current_time", "cpu_info")]

    # 执行一次测试流程
    def run_one_time(self):
        self.app.use_cpu_command()
        time.sleep(5)
        cpu_info = self.app.get_cpu_info()
        time.sleep(3)
        current_time = self.get_current_time()
        self.all_data.append((current_time, cpu_info))

    # 执行多次测试流程
    def run(self):
        if self.count > 0:
            for i in range(self.count):
                self.run_one_time()

    # 把结果写入到csv文件里面
    def write_result_to_csv(self):
        csvfile = open('report/' + self.app.config + " " + self.get_current_time().replace(":", "-") + ".csv", 'w',
                       newline='')
        writer = csv.writer(csvfile)
        writer.writerows(self.all_data)
        csvfile.close()

    # 获取当前的时间戳
    @staticmethod
    def get_current_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time


if __name__ == '__main__':
    # 在Controller()里面传入执行的次数,不传的话, 默认是执行3次
    controller = Controller(2)
    controller.run()
    controller.write_result_to_csv()
