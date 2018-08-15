forfiles -p "C:\Users\delio\AppData\Local\Temp" -s -m *.png /D -1 /C "cmd /c del @path"
forfiles -p "C:\Users\delio\AppData\Local\Temp" -s -m *.pgm /D -1 /C "cmd /c del @path"