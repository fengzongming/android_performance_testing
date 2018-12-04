import os
import csv
import time
import configparser


class App(object):
    def __init__(self):
        # 保存执行完命令的内容
        self.content = ""

        # 保存启动时间
        self.start_time = 0

        # 选择读取的配置文件(直接在这里输入文件名即可, 不要加上文件类型)
        # self.config = "launch_time_xiaoma_radio"
        self.config = "launch_time_xiaoma_music"

        # 保存adb命令
        app_information = self.read_config()
        self.start_command = app_information[0]
        self.stop_command = app_information[1]
        self.app_package = app_information[2]
        self.app_activity = app_information[3]

    # 读取配置文件
    def read_config(self):
        # 读取配置文件的内容
        config = configparser.ConfigParser()
        config.read('config/' + self.config + '.ini')
        start_command = config.get('command', 'start_app')
        stop_command = config.get('command', 'stop_app')
        app_package = config.get('package', 'app_package')
        app_activity = config.get('activity', 'app_activity')

        return start_command, stop_command, app_package, app_activity

    # 启动App
    def start_app(self):
        command = self.start_command + " " + self.app_package + '/' + self.app_activity
        self.content = os.popen(command)

    # 停止App
    def stop_app(self):
        command = self.stop_command + " " + self.app_package
        os.popen(command)

    # 获取启动时间
    def get_launch_time(self):
        for line in self.content.readlines():
            if "ThisTime" in line:
                self.start_time = line.split(":")[1]
                break
        return self.start_time


# 控制器类, 用于控制app的执行次数和统计启动时间
class Controller(object):
    def __init__(self, count=3):
        # 获取要执行的app
        self.app = App()

        # 获取需要循环执行的次数
        self.count = count

        # 获取app的当前时间戳和启动时间
        self.all_data = [("current_time", "launch_time")]

    # 执行一次测试流程
    def run_one_time(self):
        self.app.start_app()
        time.sleep(5)
        launch_time = self.app.get_launch_time()
        self.app.stop_app()
        time.sleep(3)
        current_time = self.get_current_time()
        self.all_data.append((current_time, launch_time))

    # 执行多次测试流程
    def run(self):
        if self.count > 0:
            for i in range(self.count):
                self.run_one_time()

    # 把结果写入到report文件夹下的, csv文件里面
    def write_result_to_csv(self):
        # 生成带有当前时间的csv文件
        csv_file = open(
            'report/' + self.app.config + " " + self.get_current_time().replace(":", "-") + ".csv", 'w',
            newline='')
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()

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
