注意：由于使用了Google Web Speech API，使用前请确保可以访问Google网站应用（连接VPN）

在lab1-asr文件夹下运行asr.py文件，将跳出程序窗口：

在界面下方提示栏显示绿色的"please speak..."时，您可以说出命令。

当您的设备损坏或者未说话时，界面下方提示栏显示白色的"I didn't catch that. What did you say?"，
在等待几秒后界面重新变为绿色的"please speak..."。

当您的指令未被识别时，界面显示红色的"There is no matching operation. Please try again..."，
在等待几秒后界面重新变为绿色的"please speak..."。

当您的指令正确且被识别时，界面执行相应操作。
程序支持三个命令：
包括“play music”，“open notepad”和“open broeser”，
它们将分别打开预设音频文件，txt文档和浏览器中的HCI课程主页。

在正确识别指令前，软件将一直循环识别，直到您关闭程序窗口。