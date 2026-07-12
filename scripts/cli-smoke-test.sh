#!/bin/bash
set -e

[ -z "$CEMENT_VERSION" ] && CEMENT_VERSION="3.0"
[ -z "$PYTHON_VERSIONS" ] && PYTHON_VERSIONS="3.10 3.11 3.12 3.13 3.14"

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

    docker exec cement-cli-smoke-test /bin/bash -c "cd /src ; pip install `ls dist/cement-*.tar.gz`[cli]"
    # NOTE: no `-t` here — a pseudo-TTY makes Docker emit CRLF, and command
    # substitution keeps the trailing `\r`, corrupting every `$tmp/...` path
    # (e.g. `/tmp/tmp.XXXX\r/myapp/.venv/bin/python`). Capture clean stdout.
    tmp=$(docker exec cement-cli-smoke-test /bin/bash -c "mktemp -d")


    ### verify help output

    res=$(docker exec cement-cli-smoke-test /bin/bash -c "cement --version")
    echo "$res" | grep "Cement Framework $CEMENT_VERSION.[0-9]"
    echo "$res" | grep "Python $pyver.[0-9]"
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
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; pip install ."
    res=$(docker exec -t cement-cli-smoke-test /bin/bash -c "myapp --version")
    echo "$res" | grep "Cement Framework $CEMENT_VERSION\.[0-9]"
    echo "$res" | grep "Python $pyver.[0-9]"
    echo "$res" | grep "Platform Linux.*"


    ### generated project: green out of the box (D-04/D-05/D-07)
    #
    # The generated Makefile targets call `pdm run ...`, so the container needs
    # pdm and a pdm-managed env before we can run the project's own gates.
    # `pdm install` pulls the PEP 735 dev group (ruff/mypy/pytest). With `set -e`
    # (L2), any non-green `make comply` or `make test` fails the whole build.
    # Cost note: this adds a `pdm install` + comply + test per Python version;
    # acceptable but slower, and can be scoped via PYTHON_VERSIONS if needed.

    docker exec cement-cli-smoke-test /bin/bash -c "pip install pdm"

    # The generated project pins `cement==<this dev version>`, which is not on
    # PyPI during development. `pdm install` resolves in a fresh isolated venv
    # against PyPI only (it does not see the container-global cement from the
    # `pip install dist/...` above), so it cannot find the unpublished pin.
    # Point pdm at the locally-built dist (mounted at /src/dist) via a
    # find_links source so the pin resolves. This is a harness-only shim for
    # testing an unreleased cement: a real user installs a published cement
    # from PyPI and needs no such source, and ruff/mypy/pytest ignore
    # [[tool.pdm.source]] so `make comply`/`make test` are unaffected.
    docker exec cement-cli-smoke-test /bin/bash -c "printf '\n[[tool.pdm.source]]\nname = \"local-cement-dist\"\nurl = \"file:///src/dist\"\ntype = \"find_links\"\n' >> $tmp/myapp/pyproject.toml"

    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; pdm install"
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; make comply"
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/myapp ; make test"


    ### generate a script

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate script -D $tmp/myscript"
    res=$(docker exec -t cement-cli-smoke-test /bin/bash -c "python $tmp/myscript/myscript.py --version")
    echo "$res" | grep "myscript v0.0.1"


    ### generate an extension

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate extension -D $tmp/myapp/myapp/ext"
    res=$(docker exec -t cement-cli-smoke-test /bin/bash -c "cat $tmp/myapp/myapp/ext/ext_myextension.py")
    echo "$res" | grep "myextension_pre_run_hook"


    ### generate a plugin

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate plugin -D $tmp/myapp/myapp/plugins"
    res=$(docker exec -t cement-cli-smoke-test /bin/bash -c "cat $tmp/myapp/myapp/plugins/myplugin/controllers/myplugin.py")
    echo "$res" | grep "class MyPlugin(Controller)"


    ### generate + build/install todo-tutorial (proves D-02/D-03)
    #
    # Build/install ONLY. `pip install .` builds the todo wheel via pdm-backend
    # (regex-reads __version__, no build-time import) under PEP 517 build
    # isolation and installs its deps — a green exit proves the D-02/D-03
    # migration. Do NOT run `make test`/`make comply` on todo:
    # todo-tutorial/tests/test_main.py::test_todo deliberately `raise Exception`
    # as a tutorial stub, so a test gate would always fail. `set -e` fails the
    # build if the todo build/install is non-zero.

    docker exec cement-cli-smoke-test /bin/bash -c "cement generate todo-tutorial -D $tmp/todo"
    docker exec cement-cli-smoke-test /bin/bash -c "cd $tmp/todo ; pip install ."

    ### finish

    echo ""
    echo "SMOKE TEST FOR PYTHON $pyver COMPLETED WITHOUT ERRORS"
    echo ""
}

rm -rf tmp/cli-smoke-test.out
echo "output in tmp/cli-smoke-test.out"
docker compose exec cement pdm build

for pyver in $PYTHON_VERSIONS; do
    echo -n "python $pyver . . . "
    smoke-test $pyver 2>> tmp/cli-smoke-test.out 1>> tmp/cli-smoke-test.out
    echo "ok"
done
