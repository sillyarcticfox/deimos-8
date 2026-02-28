mkdir build
cd build
command -v pyinstaller >/dev/null 2>&1 || { echo "pyinstaller is not installed! pyinstaller is available on PyPI, so you can use 'pip install pyinstaller' to install it."; cd ..; rm -r build; exit 1; }
pyinstaller --onefile ../src/assemble.py
rm -r build
rm *.spec
mv dist/* ./dei8as
rm -r dist
pyinstaller --onefile ../src/emulator.py
rm -r build
rm *.spec
mv dist/* ./dei8em
rm -r dist