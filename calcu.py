#!/usr/bin/python3
# coding=utf-8
import os
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

class preprocessing:
    
    #private
    __files = []
    workload_ratio = []
    isa_name = []
    generated_line = []
    __count_lines = -1
    __count_all_lines = -1

    def __init__(self,base):
        self.dir = base
        self.__files = self.collect_files()
        for f in self.__files:
            self.__count_lines , self.__count_all_lines = calc_linenum(f)
            self.workload_ratio.append((self.__count_lines/self.__count_all_lines)*100)
            self.generated_line.append(self.__count_lines)
            self.isa_name.append(os.path.dirname(f).split('/')[-1])
        #print(self.__count_all_lines)

    #collect all the *.v file, return in list form
    def collect_files(self):
        filelist = []
        for parent,dirnames,filenames in os.walk(self.dir):
            for filename in filenames:
                if filename.endswith('.v'):
                    filelist.append(os.path.join(parent,filename))
        return filelist

    #Calculate the number of line in individual file
    def calc_linenum(self,file):
        with open(file) as fp:
            #f = open('./verification/ADD/wrapper.v','r')
            lines = fp.readlines()
            start = lines.index( '/* GENERATE WRAPPER */\n' )
            end = lines.index( '/* END OF WRAPPER */\n' )
            number_lines = end - start - 1
            number_all_lines = len(lines)
            #print(number_lines)
        return number_lines, number_all_lines

class draw:
    #Define private
    __list1_isa = []
    __list2_lines = []
    __list3_work_ratio = []

    def __init__(self,list1,list2,list3):
        self.__list1_isa = list1
        self.__list2_lines = list2
        self.__list3_work_ratio = list3
        self.draw_diagram()
        self.draw_table()

    def draw_diagram(self):
        reduced_workload = self.__list3_work_ratio #get from outside
        ISA = self.__list1_isa
        plt.figure(figsize=(10, 15))
        range_number = len(ISA)
        plt.barh(range(len(ISA)), reduced_workload , height=0.7, color='steelblue', alpha=0.8)
        #plt.barh(range(len(ISA)), reduced_workload , color='steelblue')
        plt.yticks(range(len(ISA)), ISA)
        plt.xlim(10,15)
        plt.xlabel("ratio of workload")
        plt.title("reduced workload by ILAng")
        for x, y in enumerate(reduced_workload):
            plt.text(y + 0.2, x - 0.1, '%s' % y)
        plt.show()

    def draw_table(self):
        data = list(zip(self.__list1_isa,self.__list2_lines,self.__list3_work_ratio))[:20]
        df = pd.DataFrame(data,columns=['ISA','Generated Line','Reduced Workload(%)'],dtype=float)
        #print(df.to_latex(index=False))
        print(df)

if __name__ == '__main__':
    #Define the dir of code
    base_path = './verification/'
    pre = preprocessing(base_path)
    draw_data = draw(pre.isa_name,pre.generated_line,pre.workload_ratio)