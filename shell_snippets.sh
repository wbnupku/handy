# 获取脚本所在目录，只使用cd，dirname和pwd3个命令，不依赖于readlink
# 获取后并不改变运行脚本时所在目录
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "scrip_dir:", $SCRIPT_DIR
echo "where am I?", $(pwd}
