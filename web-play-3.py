from flask import Flask, request, render_template
import yt_dlp
import subprocess

app = Flask(__name__)

# 使用yt-dlp設置影片下載選項
ydl_opts = {'format': 'best'}
# 設定下載選項，只下載有聲音的影片
#ydl_opts = {
#    'format': 'bestaudio/best',
#    'ignoreerrors': True,
#    'postprocessors': [{
#        'key': 'FFmpegExtractAudio',
#        'preferredcodec': 'mp3',
#        'preferredquality': '192',
#    }],
#}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        # 初始化yt-dlp物件
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # 下載影片並取得其格式資訊
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict['formats']

        # 儲存符合條件的格式資訊
        matching_formats = []
        substring='1280x'
        for format in formats:
            #if format['resolution'] == '1280x720' and format['ext'] == 'mp4' and format['filesize'] is not None:
            #if substring in format['resolution']  and format['ext'] == 'mp4' and format['filesize'] is not None:
            # format['acodec'] ==' mp4a.40.2'
            if 'format_note' in format:
                if format['format_note'] == '720p' and format['ext'] == 'mp4' and format['acodec'] is not None and format['audio_channels'] == 2 :
                    matching_formats.append(format)
            else:
                if substring in format['resolution']  and format['ext'] == 'mp4' and format['acodec'] is not None:   
                    matching_formats.append(format)
        # 取得 filesize 最小的格式資訊
        global process
        if len(matching_formats) ==1 :
            url = matching_formats[0]['url']
            process = subprocess.Popen(['ffplay','-fs','-autoexit','-codec:v', 'h264_v4l2m2m', '-codec:a', 'aac', url])
            return render_template('play.html')
        if len(matching_formats) > 1:
            smallest_format = min(matching_formats, key=lambda x: x['filesize'])
            #smallest_format = max(matching_formats, key=lambda x: x['filesize'])
            url = smallest_format['url']
            # print(matching_formats)
            #subprocess.run(['ffplay', '-fs', '-codec:v', 'h264_v4l2m2m', '-codec:a', 'aac', url])
            #print(smallest_format)
            #global process 
            process = subprocess.Popen(['ffplay','-fs','-autoexit','-codec:v', 'h264_v4l2m2m', '-codec:a', 'aac', url])
            return render_template('play.html')
        else:
            return "No matching format found."
            
    else:
        return render_template('index.html')
    
    
@app.route('/stop',methods=['GET','POST'])
def stop():
    if process.poll() is None:
       process.terminate()
       return  render_template('stop.html') 
    elif process.poll() == 0 :
       return "The video has finished playing."
    else:
       return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
