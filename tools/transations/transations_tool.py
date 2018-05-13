# -*-coding:utf-8-*-
import getopt
import os
import sys
import re
current_path = os.path.abspath(os.path.dirname(__file__))
project_path = os.path.abspath("{}/../..".format(current_path))
sys.path.append(project_path)
from tools.usage import usage_help
__author__ = 'Allen Woo'

class Transations():

    def main(self):

        self.cfg_path = "{}/babel.cfg".format(current_path)
        self.extract_path = "{}/apps".format(project_path)
        s_ops = "hq"
        l_ops = ["init", "update", "compile", "cfg=", "extract=", "output=", "lan=", "all-lan",
                 "get-msgid=", "re-msgstr="]
        s_opexplain = ["help","quiet:A small amount of output"]
        l_opexplain = ["init translation",
                       "update: extract and update",
                       "compile",
                       "<cfg file path>, The default:{}.\n\t\tOptional: {}/babel_py.cfg".format(self.cfg_path, current_path),
                       "<Translation extract directory>,The default: {}".format(self.extract_path),
                       "<output directory>, Output directory.\n\t\tSuce as:{}/translations/template".format(self.extract_path),
                       "<language>, Such as: en_US, zh_Hans_CN",
                       "View all languages",
                       "<path> Get 'msgid' in po file",
                       "<file:Translation completed msgid text> Fill the 'msgstr' in the po file with the translated text"
                       "\n                    (此参数指定的文件的格式和行号必须和--get-msgid导出的文件格式和行号一模一样)"]

        action = ["init, [--init --extract <path> --output <path:Such as:xxx/transations/theme> --lan en_US]",
                  "update, [--update --extract <path> --output <path:Such as:xxx/transations/theme>]",
                  "compile, [--compile --output <path:Such as:xxx/transations/theme>]",
                  "get-msgid [--get-msgid <path:Such as:xxx/transations/theme> --lan <value>]",
                  "re-msgstr [--re-msgstr <path:xxx/xxx.txt> --output <path> --lan <value>]"]

        opts, args = getopt.getopt(sys.argv[1:], s_ops, l_ops)
        func = None
        self.save_path = None
        self.quiet = ""
        self.lan = "zh_Hans_CN"
        self.msgid_tred_file_path = ""
        if not opts:
            usage_help(s_ops, s_opexplain, l_ops, l_opexplain, action=action)
        for op, value in opts:
            if op == "-q":
                self.quiet = "-q"
            elif op == "--lan":
                self.lan = value.strip()
            elif op == "--all-lan":
                os.system("pybabel --list-locales")
                sys.exit()

            elif op == "--cfg":
                self.cfg_path = value.strip()

            elif op == "--extract":
                self.extract_path = value.rstrip("/")

            elif op == "--output":
                self.save_path = value.rstrip("/")

            elif op == "--init":
                func = self.init_tr

            elif op == "--update":
                func = self.update_tr

            elif op == "--compile":
                func = self.compile_tr

            elif op == "--get-msgid":
                self.save_path = value.rstrip("/")
                func = self.get_msgid

            elif op == "--re-msgstr":
                self.msgid_tred_file_path = value.rstrip("/")
                func = self.replace_msgstr

            elif op == "-h" or op == "--help":
                usage_help(s_ops, s_opexplain, l_ops, l_opexplain, action = action)

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        func()

    def init_tr(self):

        '''
        compile transations
        '''
        self.cfg_sack()

        if not self.quiet:
            self.redirect = ""
        if self.lan:
            print("Extract...")
            print(self.extract_path)
            os.system('pybabel {} extract -F {} -o {}/messages.pot {}'.format(self.quiet,
                                                                                 self.cfg_path,
                                                                           self.save_path,
                                                                           self.extract_path))
            print("Init...")
            os.system('pybabel {} init -i {}/messages.pot -d {} -l {}'.format(self.quiet,
                                                                              self.save_path,
                                                                              self.save_path,
                                                                              self.lan))
            self.print_cfg()
            print("Success")
        else:
            print("You need to specify the language:--lan <language>\n")


    def update_tr(self):

        '''
        update transations
        '''

        self.cfg_sack()

        lc_msg_path = "{}/{}/LC_MESSAGES".format(self.save_path, self.lan)
        po_filepath = os.path.join(lc_msg_path, "messages.po")

        if not os.path.exists(po_filepath):
            print(po_filepath)
            raise Exception("Missing messages.po file, may also be wrong language(--lan). please reinitialize translation. -h")
        if not self.quiet:
            self.redirect = ""

        os.system('pybabel {} extract -F {} -k lazy_gettext -o {}/messages.pot {}'.format(self.quiet,
                                                                                             self.cfg_path,
                                                                                          self.save_path,
                                                                                          self.extract_path))
        os.system('pybabel {} update -i {}/messages.pot -d {}'.format(self.quiet, self.save_path,
                                                                         self.save_path))

        self.update_process()
        self.print_cfg()
        print("Success")

    def compile_tr(self):

        '''
        compile transations
        '''

        if not self.quiet:
            self.redirect = ""
        os.system('pybabel compile -d {} {}'.format(self.save_path, self.redirect))

    def update_process(self):

        lc_msg_path = "{}/{}/LC_MESSAGES".format(self.save_path, self.lan)
        po_filepath = os.path.join(lc_msg_path, "messages.po")
        if os.path.exists(po_filepath):
            with open(po_filepath) as rf:
                lines = rf.readlines()
                wf = open("{}_last.back".format(po_filepath), "w")
                wf.writelines(lines)
                wf.close()

            abandoned_datas = {}
            datas = {}
            l = len(lines)
            for i in range(0, l):
                if re.search(r"^#~ msgid.*", lines[i]) and lines[i + 1].strip("#~ msgid").strip().strip('""') and lines[
                    i + 1].strip("#~ msgstr").strip().strip('""'):
                    abandoned_datas[lines[i].strip("#~ ").strip()] = lines[i + 1].strip("#~ ").strip()
                elif re.search(r"^msgid.*", lines[i]) and lines[i + 1].strip("msgid").strip().strip('""') and lines[
                    i + 1].strip("msgstr").strip().strip('""'):
                    datas[lines[i].strip()] = lines[i + 1].strip()

            for i in range(0, l):
                msgid = re.search(r"^msgid.*", lines[i])
                if msgid and lines[i].strip("msgid").strip().strip('""') and not lines[i + 1].strip("msgstr").strip().strip(
                        '""'):
                    l = lines[i].strip("\n")
                    if l in abandoned_datas.keys():
                        lines[i + 1] = abandoned_datas[l] + "\n"
                    if l in datas.keys():
                        lines[i + 1] = datas[l] + "\n"

            temp_lines = lines[:]
            l = len(temp_lines)
            for i in range(0, l):
                r = re.search(r"^#~.*", temp_lines[i])
                if r:
                    lines.remove(temp_lines[i])

            wf = open(po_filepath, "w")
            wf.writelines(lines)
            wf.close()

    def cfg_sack(self):

        print("\n* [Dangerous operation] Please check if the update option is wrong\n")
        print("Extraction path: {}".format(self.extract_path))
        print("Output path: {}".format(self.save_path))
        print("Cfg file: " + self.cfg_path)
        self.print_cfg()
        print("\n")
        ch = input("Are you sure you want to use this cfg file?(Y/N): ")
        if ch.lower() not in ["yes", "y"]:
            sys.exit(0)

    def print_cfg(self):

        with open(self.cfg_path) as rf:
            print("* Extract content type[{}]:".format(os.path.split(self.cfg_path)[-1]))
            for line in rf.readlines():
                print("    "+line.strip("\n"))


    def get_msgid(self):

        lc_msg_path = "{}/{}/LC_MESSAGES".format(self.save_path, self.lan)
        po_filepath = os.path.join(lc_msg_path, "messages.po")

        result_path = "{}/result_msgid_text.txt".format(current_path)
        wf = open(result_path, "w")
        with open(po_filepath) as rf:
            last_l = ""
            lines = rf.readlines()
            lines_num = len(lines)
            for i in range(0, lines_num):
                l = lines[i]
                isc = False
                tr_exists = False
                wl = None

                if i+1 < lines_num and re.search(r'^msgstr\s".+"', lines[i+1]):
                    # 已翻译的不需要提取
                    continue

                if re.search(r"^#:\s.+:[0-9]+", last_l):

                    s = re.search("^msgid\s(.+).+", l)
                    if l and s:
                        wl = s.groups()[0].strip('"')
                    last_l = l

                elif last_l.strip() == 'msgid ""' and not re.search("^msgstr\s.+", l) and l:
                    wl = l
                    isc = True
                    for j in range(1,4):
                        if i + j < lines_num  and re.search(r'^msgstr\s.+', lines[i + j]) and re.search(r'^msgstr\s".+"', lines[i + j]):

                            # 已翻译的不需要提取
                            tr_exists = True
                            break
                if tr_exists:
                    continue

                if wl:
                    if wl.endswith("\\"):
                        wl = wl + '"'
                    wf.write("{}::: ".format(i+1) + wl + "\n")
                    if isc:
                        continue

                last_l = l
        wf.close()
        print("Result path: {}".format(result_path))

    def replace_msgstr(self):

        lc_msg_path = "{}/{}/LC_MESSAGES".format(self.save_path, self.lan)
        po_filepath = os.path.join(lc_msg_path, "messages.po")
        rfp = open(po_filepath, "r")
        polines = rfp.readlines()

        translated_text = self.msgid_tred_file_path
        with open(translated_text) as rf:
            last_text = ""
            for l in rf:
                l = l.split(":::")
                if l and len(l) > 1:
                    if not  l[0]:
                        continue
                    num = int(l[0])-1
                    text = "{}{}".format(last_text, l[1].strip())
                    if re.search("^msgstr\s(.+).+", polines[num + 1]):
                        text = text.replace('""', '')
                        if re.search(r'.+[^\\]".+', text):
                            print("The number of lines that need to be manually confirmed (.po file): \n{}: {}\n".format(num+1,text))

                        text = 'msgstr "{}"'.format(text)

                        polines[num + 1] = text.replace('""', '"') + "\n"

                        last_text = ""
                    else:
                        last_text = text


        rfp.close()
        with open(po_filepath, "w") as wf:
            wf.writelines(polines)

if __name__ == '__main__':

    trs = Transations()
    trs.main()