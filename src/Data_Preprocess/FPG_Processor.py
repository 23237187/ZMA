__author__ = 'root'

import ast
import fileinput

class FPG_Processor:
    def __init__(self, freqSetFile, outFile, trans_num=14279.0):
        self.input_path = freqSetFile
        self.output_path = outFile
        self.trans_num = trans_num

    def run_generate_rule(self):
        L, supportData = self.convert_input_to_L_and_supportData()
        with open(self.output_path, "w") as outfile:
            self.generateRules(L, supportData, outfile)
        self.fpg_result_post_process()


    def convert_input_to_L_and_supportData(self):
        L = [[]] * 10
        supportData = dict()
        max_length = 0
        with open(self.input_path, "r") as inputfile:
            lines = inputfile.readlines()
            for line in lines:
                segments = line.strip().rsplit(",", 1)
                freq_set = ast.literal_eval(segments[0].strip())
                freq_count = ast.literal_eval(segments[1].strip())
                freq_set_length = len(freq_set)
                freq_set = frozenset(freq_set)
                supportData[freq_set] = freq_count / self.trans_num
                if freq_set_length > max_length:
                    max_length = freq_set_length
                index = freq_set_length
                if len(L[index]) == 0:
                    L[index] = [freq_set]
                else:
                    L[index].append(freq_set)

            del L[max_length + 1:]
            supportData[frozenset()] = 1.0
        return L, supportData




    def generateRules(self, L, supportData, outfile, minConf=0.0001):
        bigRuleList = list()
        for i in range(1, len((L))):
            for freqSet in L[i]:
                Hl =[frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, Hl, supportData, bigRuleList, outfile, minConf)
                else:
                    self.calcConf(freqSet, Hl, supportData, bigRuleList, outfile, minConf)
        return bigRuleList

    def calcConf(self, freqSet, H, supportData, brl, outfile, minConf=0.0001):
        prunedH = list()
        for conseq in H:
            conf = supportData[freqSet] / supportData[freqSet - conseq]
            if supportData[freqSet - conseq] == 1.0:
                continue
            if conf >= minConf:
                print(freqSet-conseq, '-->', conseq, file=outfile)
                brl.append((freqSet - conseq, conseq, conf))
                prunedH.append(conseq)
        return prunedH

    def rulesFromConseq(self, freqSet, H, supportData, brl, outfile, minconf=0.0001):
        m = len(H[0])
        if (len(freqSet) > (m + 1)):
            Hmpl = self.aprioriGen(H, m + 1)
            Hmpl = self.calcConf(freqSet, Hmpl, supportData, brl, outfile, minconf)
            if (len(Hmpl) > 1):
                self.rulesFromConseq(freqSet, Hmpl, supportData, brl, outfile, minconf)

    @staticmethod
    def aprioriGen(Lk, k):
        retList = list()
        lenLk = len(Lk)
        for i in range(lenLk):
            for j in range(i+1, lenLk):
                L1 = list(Lk[i])[:k-2]
                L2 = list(Lk[j])[:k-2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])
        return retList

    def fpg_result_post_process(self):
        for line in fileinput.input(self.output_path, inplace=True):
            print(line.replace("frozenset(", ""), end='')
        for line in fileinput.input(self.output_path, inplace=True):
            print(line.replace(")", ""), end='')

