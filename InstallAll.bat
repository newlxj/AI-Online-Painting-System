cd sdweb
cmd /c npm install
pause
cd ../
cd sdweb-server
pause
python -V
python -m venv ai8-env
pause
ai8-env\Scripts\activate.bat
pip -V
pip install -r requirements.txt
echo 安装完成，如果没出现错误表示安装成功，如果出现错误请检查python pip和nodejs npm是否正确安装
echi The installation is complete. If there are no errors, it indicates successful installation. If there are errors, please check if the Python pip and nodejs npm are installed correctly
pause