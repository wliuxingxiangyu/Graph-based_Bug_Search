#encoding=utf-8
#无需学会idapython 的使用，直接调用该类下的接口即可获得函数

#系统ida所在的路径
idapath = "/home/hz/idafree-7.0/ida64"
import os,time,commands,json
import argparse

parse = argparse.ArgumentParser()
import sys
pro_path = sys.path[0]

class getFeature:
    def __init__(self, binarypath):
        self._bin = binarypath
        self._tmpfile = pro_path + os.sep + binarypath.split('/')[-1] + str(time.time()) + '.json'
        pass

    #read json file to get features
    def _ReadFeatures(self):
        with open(self._tmpfile,'r') as f:
            for line in f.readlines():
                # print line
                x = json.loads(unicode(line,errors='ignore'))
                yield x

    def _del_tmpfile(self):
        os.remove(self._tmpfile)

    def get_Feature_all(self):
        return self.get_Feature_Function('')
        pass

    def get_Feature_Function(self, func_name):

        cmd = "TVHEADLESS=1 %s -A -S'%s/Feature_Of_Binary.py %s %s' %s" % (idapath, pro_path, self._tmpfile, func_name, self._bin)
        # print cmd
        s,o = commands.getstatusoutput(cmd)

        if s!=0 :
            print 'error occurs when extract Features from ida database file'
            print 'cmd is %s' % cmd
            print s,o
            return None

        features = list(self._ReadFeatures())
        self._del_tmpfile()
        return features

def test(args):

    binary_path = args.binaryfile
    # generate ida database file
    if args.b:
        database = '.i64'
        # from utils import generate_i64
        # cmd = 'TVHEADLESS=1 %s -B  %s' % (idapath, binary_path)

        # new format to generate ida database file : ida -c -A -Sanalysis.idc input-file
        cmd = 'TVHEADLESS=1 %s -c -A -Sanalysis.idc %s' % (idapath, binary_path)

        # database = generate_i64(binary_path, binary_path + '.i64')
        print cmd
        s,o = commands.getstatusoutput(cmd)
        if s != 0:
            print 'error occurs when generate ida database file ',s,o
            print 'program exits...'
            return
        binary_path =  binary_path.split('.')[0]+'.i64' # Zlib.so -> Zlib.i64

    func_name = ''
    out_file = ''
    if args.f:
        func_name = args.f
    if args.o:
        out_file = args.o

    gf = getFeature(binary_path)
    feature = gf.get_Feature_Function(func_name)

    if len(out_file) > 0:
        with open(out_file, 'w') as f:
            json.dump(feature, f, indent=4)
    else:
        for x in feature:
            print x


if __name__ == '__main__':
    parse.add_argument('binaryfile', help='file to be analysed')
    parse.add_argument('-f', help='function name to be handled ')
    parse.add_argument('-b', help='file to be analysed is binary file , default is ida database file', action = 'store_true' , default=False)
    parse.add_argument('-o', help='output filename')
    args = parse.parse_args()
    test(args)


