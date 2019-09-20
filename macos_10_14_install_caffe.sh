
# prerequisites
# brew, commandlinetools, anaconda
# 1. 遇到veclib找不到的问题
#    答：没有把默认的atlas改成openblas
# 2. 遇到pyconfig.h找不到的问题
#    答：没有uncoment .../include/python/include这一行


shelldir=''

conda create --name py27 python=2.7 jupyter numpy scipy scikit-image
conda activate py27



brew install wget
# levveldb 没有用在这个编译中，因为需要c++11特性, 在Makefile.config中去掉了
brew install -vd snappy leveldb gflags glog szip lmdb
brew install openblas
brew install hdf5 opencv
brew install boost@1.59 boost-python@1.59
brew link boost@1.59 --force
brew link boost-python@1.59 --force

cd ~/Downloads 
wget https://github.com/protocolbuffers/protobuf/archive/v3.5.1.zip
unzip protobuf-3.5.1.zip
cd protobuf-3.5.1
./autogen.sh
./configure
make
make install


cd ~/Downloads
git clone https://github.com/BVLC/caffe.git
cd caffe
cp ${shelldir}/Makefile.config Makefile.config

make -j 8
make py
make distribute


cp -r distribute/python/caffe ${ANACONDA_PREFIX}/lib/python2.7/site-packages/
cp -r distirbute/lib/libcaffe* ${ANACONDA_PREFIX}/lib

# need protobuf in conda env py27
conda install protobuf

python -c 'import caffe'
