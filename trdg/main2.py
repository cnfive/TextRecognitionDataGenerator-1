import os
import sys
import shutil
import random


class Generate:
    """
    生成器
    """

    def __init__(self,
                 path='.',
                 epoch=3,
                 batch=149,
                 blank=False,
                 max_length=38,
                 ):
        # 字体文件
        self.fonts_dir = os.path.join(path, "fonts/cn/")
        self.fonts = os.listdir(self.fonts_dir)
        # 生成的语料路径
        self.dic = os.path.join(path, "dicts/6500汉字和词典/test.txt")
        # 生成批次
        self.epoch = epoch
        # 批次大小
        self.batch = batch
        # 是否加入空格
        self.blank = blank
        # 执行文件
        self.run = os.path.join(path, "run.py")
        # 生成结果保存路径
        self.output_gen = os.path.join(path, "output", "generate")
        # 转换后结果保存路径
        self.output_tran = os.path.join(path, "output", "data")
        # 最大字符数
        self.max_length = max_length
        # 操作系统
        if 'win' in sys.platform:
            self.dot = ""
        else:
            self.dot = "'"
        self.flag = 0

    def gen_image(self, dic=None):
        """
        生成图片
        """
        for i in range(self.epoch):
            if dic is None:
                dictionary = self.dic
                with open(self.dic, 'w', encoding="utf-8") as f:
                    for j in range(self.batch):
                        # 随机产生一个最大字符长度k
                        num = random.randint(1, self.max_length)
                        k = 10 ** num
                        # 产生该随机数
                        text = str(random.randint(1, k))
                        bank_num = ''
                        for char in text:
                            # 加入空格
                            rand_int = random.randint(0, 10)
                            if rand_int > 7:
                                bank_num += ' '
                            bank_num += char
                        f.writelines(bank_num + '\n')
            else:
                with open(dic, 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                with open('temporary.txt', 'w', encoding="utf-8") as f:
                    random_lines = random.choices(lines, k=self.batch)
                    for line in random_lines:
                        f.writelines(line + '\n')
                dictionary = 'temporary.txt'
            font = random.choice(self.fonts)
            os.system(
                """python {8} -c {11} -i {9} -sw {0} -k {1} -rk -bl 2 -rbl -b 3 -d 0 -f {2} \
                --margins {3},{4},{5},{6} \
                --fit -t 8 -ft {7} -tc {12}#000000,#FFFFFF{12} --output_dir {10}""".format(
                    random.randint(0, 4), random.randint(0, 4), random.randint(28, 38), random.randint(0, 10),
                    random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), os.path.join(self.fonts_dir, font),
                    self.run, dictionary, self.output_gen, self.batch, self.dot))
            # 删除临时文件
            if os.path.isfile('temporary.txt'):
                os.remove('temporary.txt')
            self.transform()

    def transform(self, output=None):
        """
        将所生成数据转换为模型训练所需格式
        """
        if output:
            output_tran = output
        else:
            output_tran = self.output_tran
        images = [file for file in os.listdir(self.output_gen) if file != 'labels.txt']
        if not os.path.exists(output_tran):
            os.mkdir(output_tran)

        # 图片标签映射字典
        with open(os.path.join(self.output_gen, 'labels.txt'), "r", encoding='utf8') as f:
            lines = f.readlines()
        dictionary = {}
        for line in lines:
            img = line.split(' ')[0]
            separator =' '
             # 使用partition来切分字符串
            parted = line.partition(separator)
            label =parted[2]
            dictionary[img] = label

        for i in range(len(images)):
            text = dictionary[images[i]]
            shutil.move(os.path.join(self.output_gen, images[i]), os.path.join(output_tran, '{0}_{1}.jpg'.format(str(self.flag), str(i))))
            with open(os.path.join(output_tran, '{0}_{1}.txt'.format(str(self.flag), str(i))), 'w', encoding='utf8') as f:
                print(text)
                f.write(text.replace(' ', '').replace("	",""))
                print(text)
        self.flag += 1

if __name__ == '__main__':
    project_path = 'H:\\TextRecognitionDataGenerator-1-main\\trdg'
    gen = Generate(path=project_path)
    # 字典路径
    path = os.path.join(project_path, 'dicts/6500汉字和词典/test.txt')
    # 生成图片
    gen.gen_image(path)