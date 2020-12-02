function build_wheel()
{
    python3 ./setup.py bdist_wheel
}

function get_input()
{
    echo "Update currently installed version? (yes(y)/no(n))"
    read response
}

function input_check()
{
    list_y="y Y yes Yes YES"
    list_n="n N no No NO"
    if echo "$list_y" | grep -w $response > /dev/null ;
    then
        update_wheel
    elif echo "$list_n" | grep -w $response > /dev/null ;
    then
        echo "Skipping wheel update"
    else
        get_input
        input_check
    fi
}

function update_wheel()
{
    latest=$(ls -t ./dist | head -n1)
    echo Updating wheel to $latest...
    pip install ./dist/$latest --upgrade
    echo Updated wheel
}

function main()
{
    build_wheel
    get_input
    input_check
    exit 1
}

main