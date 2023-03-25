import yt_dlp

# 使用yt-dlp設置影片下載選項
ydl_opts = {'format': 'best'}

# 輸入要下載的影片網址
#url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
url = 'https://www.youtube.com/watch?v=8wU28qY-XJY'

# 初始化yt-dlp物件
ydl = yt_dlp.YoutubeDL(ydl_opts)

# 下載影片並取得其格式資訊
info_dict = ydl.extract_info(url, download=False)
formats = info_dict['formats']

# 輸出格式資訊
for format in formats:
    if 'filesize' in format:
        filesize = format['filesize']
    else:
        filesize = 'N/A'
    #print(format['format_id'], format['ext'], format['resolution'], filesize,format['acodec'],format['format_note'])
    print(format['format_id'], format['ext'], format['resolution'], filesize,format['acodec'])

#print(format)
