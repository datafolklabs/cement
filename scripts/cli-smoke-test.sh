#!/bin/bash
set -e

[ -z "$CEMENT_VERSION" ] && CEMENT_VERSION="3.0"
[ -z "$PYTHON_VERSIONS" ] && PYTHON_VERSIONS="3.8 3.9 3.10 3.11 3.12"

function smoke-test {
    pyver=$1

    echo "-------------------------------------------------------------------"
    echo "SMOKE TESTING CEMENT CLI ON PYTHON $pyver"
    echo "-------------------------------------------------------------------"
    docker stop cement-cli-smoke-test 2>&1 >/dev/null ||:
    docker rm -f cement-cli-smoke-test 2>&1 >/dev/null ||:
    docker run \
        --name cement-cli-smoke-test \
        -itd \
        -v `pwd`:/src \
        python:$pyver \
        /bin/bash
    docker exec -it cement-cli-smoke-test /bin/bash -c "cd /src ; python setup.py install"
    tmp=$(docker exec cement-cli-smoke-test /bin/bash -c "mktemp -d")

    
    ### verify help output

    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement --version")
    echo "$res" | grep "Cement Framework $CEMENT_VERSION.\d"
    echo "$res" | grep "Python $pyver.\d"
    echo "$res" | grep "Platform Linux.*"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement --help")
    echo "$res" | grep "Cement Framework Developer Tools"
    echo "$res" | grep "generate"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement -h")
    echo "$res" | grep "Cement Framework Developer Tools"
    echo "$res" | grep "generate"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement generate -h")
    echo "$res" | grep "project"
    echo "$res" | grep "todo-tutorial"
    echo "$res" | grep "plugin"
    echo "$res" | grep "script"
    echo "$res" | grep "extension"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement generate project -h")
    echo "$res" | grep "destination directory path"
    echo "$res" | grep -- "-D, --defaults"

    
    ### generate a project

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate project -D $tmp/myapp"
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; pip install -r requirements.txt"
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; python setup.py install"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "myapp --version")
    echo "$res" | grep "Cement Framework $CEMENT_VERSION\.\d"
    echo "$res" | grep "Python $pyver.\d"
    echo "$res" | grep "Platform Linux.*"

    
    ### generate a script

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate script -D $tmp/myscript"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "python $tmp/myscript/myscript.py --version")
    echo "$res" | grep "myscript v0.0.1"
    

    ### generate an extension

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate extension -D $tmp/myapp/myapp/ext"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cat $tmp/myapp/myapp/ext/ext_myextension.py")
    echo "$res" | grep "myextension_pre_run_hook"


    ### generate a plugin

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate plugin -D $tmp/myapp/myapp/plugins"
    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cat $tmp/myapp/myapp/plugins/myplugin/controllers/myplugin.py")
    echo "$res" | grep "class MyPlugin(Controller)"

    ### finish

    echo ""
    echo "SMOKE TEST FOR PYTHON $pyver COMPLETED WITHOUT ERRORS"
    echo ""
}

rm -rf tmp/cli-smoke-test.out
echo "output in tmp/cli-smoke-test.out"

for pyver in $PYTHON_VERSIONS; do
    echo -n "python $pyver . . . "
    smoke-test $pyver 2>> tmp/cli-smoke-test.out 1>> tmp/cli-smoke-test.out
    echo "ok"
done