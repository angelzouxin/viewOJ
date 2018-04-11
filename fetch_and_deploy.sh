set -e
git_local=`git rev-parse HEAD`
git_remote=`git ls-remote origin master | awk -F' ' '{print $1}'`

if [ "$git_remote" == "$git_local" ];then
  echo no change && exit 0
fi

echo fetch from remote
git fetch
git reset --hard origin/master
./deploy.sh
