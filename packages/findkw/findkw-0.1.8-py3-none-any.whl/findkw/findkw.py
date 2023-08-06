import argparse
import os
import re
from pathlib import Path


class Finder(object):

    def __init__(self, dir_path, kw, name_only, is_re, return_container, rmf=None, rml=None, qr=None):
        self.path = dir_path
        self.sep = "<<<***0...>>>"
        self.kw = kw
        self.name_only = name_only
        self.is_re = is_re
        self.rmf = rmf
        self.rml = rml
        self.qr = qr
        self.return_container = return_container

    def start(self):
        f_lis = []
        for root, sub_dir, file_names in os.walk(self.path):
            f_lis += [os.path.join(root, file_name) for file_name in file_names]
        container = self.get_container(f_lis) if not self.is_re else self.get_container_re(f_lis)
        if self.return_container:
            return container
        ft = " >>> "
        for match, type_line_id in container.items():
            type_str = 'file content'
            if isinstance(type_line_id, str):
                if not self.is_re:
                    match_str = match.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                else:
                    match_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, match)
                if f'{self.sep}dir_name' in type_line_id:
                    type_str = 'folder'
                if f'{self.sep}file_name' in type_line_id:
                    type_str = 'file name'
                print(f"{ft}[ {type_str} ] [ {match_str} ]")
            else:
                lines_set = set()
                del_lines = list()
                print(f"in file [ {match} ]: ")
                for line in type_line_id:
                    line_no, line_str = line.split(self.sep)
                    if line not in lines_set:
                        lines_set.add(line)
                        if not self.is_re:
                            line_str = line_str.replace(self.kw, f"\033[0;31;48m{self.kw}\033[0m")
                        else:
                            line_str = re.sub(fr'(?P<kw>{self.kw})', self.make_re_color, line_str)
                        print(f"{ft}[ {line_no} ] [ {line_str} ]")
                    if self.rml:
                        if not self.qr:
                            is_rm = True if 'y' in input("delete this line? ").lower() else False
                            if is_rm:
                                del_lines.append(line)
                        else:
                            del_lines.append(line)
                self.delete_lines(match, del_lines)
                print()
            if self.rmf:
                mp = Path(match)
                if not self.qr:
                    is_rm = True if 'y' in input("remove the above files? ").lower() else False
                    if is_rm:
                        mp.rmdir() if mp.is_dir() else os.remove(str(mp.absolute()))
                        print(f'file: \033[0;31;48m"{match}" ✘\033[0m')
                else:
                    mp.rmdir() if mp.is_dir() else os.remove(str(mp.absolute()))
                    print(f'file: \033[0;31;48m"{match}" ✘\033[0m')

    def delete_lines(self, match, dl_lines):
        dl_lines = [x.split(self.sep) for x in dl_lines]
        line_no = {int(x[0]) for x in dl_lines if x[0] and isinstance(x[0], str) and x[0].isdigit()}
        dlp = Path(match)
        raw_lines = dlp.read_text().split("\n")
        new_lines = []
        for num, rl in enumerate(raw_lines, 1):
            if num not in line_no:
                new_lines.append(rl)
        new_file = "\n".join(new_lines)
        # os.remove(str(dlp.absolute()))
        dlp.write_text(new_file, encoding="utf-8")
        for ln, l_str in dl_lines:
            print(f'line [ \033[0;31;48m{ln}\033[0m ]: \033[0;31;48m"{l_str}" ✘\033[0m')

    @staticmethod
    def make_re_color(matched):
        res = f"\033[0;31;48m{matched.group('kw')}\033[0m"
        return res

    def get_container(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if self.kw in fsn[0]:
                    container[fsn[0]] = f'{self.sep}dir_name'
                if self.kw in fsn[1]:
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    with open(f, 'r') as rf:
                        lines = rf.readlines()
                    lines_with_kw = []
                    line_count = 0
                    for line in lines:
                        line_count += 1
                        if self.kw in line:
                            l_str = f'{line_count}{self.sep}{line.strip()}'
                            lines_with_kw.append(l_str)
                    # lines_with_kw = [f'{lines.index(x)+1}{self.sep}{x.strip()}' for x in lines if self.kw in x]
                    if lines_with_kw:
                        container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container

    def get_container_file_name_only(self):
        container = dict()
        cmd = f"find {self.path} -name '{self.kw}' "

    def get_container_re(self, lis):
        container = dict()
        for f in lis:
            if self.name_only:
                if self.sep in f:
                    f = f.replace(self.sep, ''.join([f"\\{x}" for x in self.sep]))
                fs = f.split(os.sep)
                fsn = [os.sep.join(fs[:-1]), fs[-1]]
                if re.findall(self.kw, fsn[0]):
                    container[fsn[0]] = f'{self.sep}dir_name'
                if re.findall(self.kw, fsn[1]):
                    container[os.sep.join(fsn)] = f'{self.sep}file_name'
            else:
                try:
                    with open(f, 'r') as rf:
                        lines = rf.readlines()
                    lines = [x.replace(self.sep, ''.join([f"\\{x}" for x in self.sep])) if self.sep in x else x for x in lines]
                    lines_with_kw = [f'{lines.index(x)+1}{self.sep}{x.strip()}' for x in lines if re.findall(self.kw, x)]
                    if lines_with_kw:
                        container[f] = lines_with_kw
                except Exception as E:
                    pass
        return container


def find():
    dp = ' *** 这是一个在文件夹下所有的地方查找关键字的工具，支持正则表达式'
    da = "--->   "
    parser = argparse.ArgumentParser(description=dp, add_help=True)
    parser.add_argument("-f", "--folder", type=str, dest="folder", default='', help=f'{da}需要查找的文件夹，默认运行目录')
    parser.add_argument("-k", "--keyword", type=str, dest="keyword", default='', help=f'{da}要查找的关键字，必须值')
    parser.add_argument("-r", "--re_mode", type=str, dest="re_mode", nargs='?', default='n', help=f'{da}y/n 是否以正则方式查找，默认n')
    parser.add_argument("-o", "--filename_only", type=str, dest="filename_only", nargs='?', default='n', help=f'{da}y/n 是否只查找文件夹名和文件名，默认n')
    parser.add_argument("-rmf", "--remove_file", type=str, dest="remove_file", nargs='?', default='n', help=f'{da}y/n 是否删除找到的文件，默认n')
    parser.add_argument("-rml", "--remove_line", type=str, dest="remove_line", nargs='?', default='n', help=f'{da}y/n 是否删除找到的行，默认n')
    parser.add_argument("-qr", "--quietly_remove", type=str, dest="quietly_remove", nargs='?', default='n', help=f'{da}y/n 是否不经确认直接删除，默认n')
    args = parser.parse_args()

    keyword = args.keyword
    folder = args.folder
    re_mode = args.re_mode
    remove_file = args.remove_file
    remove_line = args.remove_line
    quietly_remove = args.quietly_remove
    filename_only = args.filename_only
    remove_file = True if remove_file is None or remove_file.lower() == 'y' else False
    remove_line = True if remove_line is None or remove_line.lower() == 'y' else False
    quietly_remove = True if quietly_remove is None or quietly_remove.lower() == 'y' else False
    re_mode = True if re_mode is None or re_mode.lower() == 'y' else False
    filename_only = True if filename_only is None or filename_only.lower() == 'y' else False

    kw = keyword
    if not kw:
        raise ValueError('关键字是必须的: findkw -k xxx')

    if not folder:
        folder = os.getcwd()

    fd = Finder(folder, kw, filename_only, re_mode, False, remove_file, remove_line, quietly_remove)
    fd.start()


if __name__ == '__main__':
    fdr = Finder("/home/ga/Guardian/For-Longqi/MeeseeksBox/", 'LOG_DIR', False, False, False, False, False, False)
    fdr.start()
