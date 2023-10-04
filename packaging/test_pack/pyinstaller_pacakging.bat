cd a_dll_bind
python setup.py build_ext --inplace
python generate_stub.py
cd ..
pyinstaller --paths test_dir ^
        --hidden-import pysome.hiddenmodule ^
        --icon dog01.ico ^
        -y --name myapp2 main.py
