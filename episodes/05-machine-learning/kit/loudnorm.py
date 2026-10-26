"""两遍 loudnorm：−14 LUFS，真峰值 ≤ −1 dBTP（目标 −1.5 留余量）。用法：python3 loudnorm.py in.wav out.wav"""
import sys, json, re, subprocess
i, o = sys.argv[1:3]; F = 'loudnorm=I=-14:TP=-2.2:LRA=11'
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', i, '-af', F + ':print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
m = json.loads(re.findall(r'\{[^{}]*\}', r)[-1])
af = f"{F}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000"
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', i, '-af', af, '-c:a', 'pcm_s24le', o], check=True)
print('第一遍测得', m['input_i'], 'LUFS', m['input_tp'], 'dBTP')
