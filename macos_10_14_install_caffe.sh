
# prerequisites
# brew, commandlinetools, anaconda


conda create --name py27 python=2.7 jupyter numpy scipy scikit-image
conda activate py27



brew install wget
# levveldb 没有用在这个编译中，因为需要c++11特性
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
cp Makefile.config.example Makefile.config

