import os
import shutil
import time
import urllib.request
import subprocess

main_url = "https://evoworld.io/"
cdn_url = "https://cdn1.eu.evoworld.io/js/"
scripts = ["loader", "pve", "ui", "game_init", "shared", "functions", "game"]
raw_scripts = ["jquery.min", "lang", "socket.io-2.3.0", "jquery.wheelmenu"]
scripts_dir = "scripts"
deobf_cmd = "obfuscator-io-deobfuscator {input_file} -o {output_file}"

print("EvoWorld Scripts Downloader started.")

# Install deobfuscator
print("Installing deobfuscator via NPM if needed...")
subprocess.call("npm list -g obfuscator-io-deobfuscator || npm install -g obfuscator-io-deobfuscator", shell=True)
print("Done.")

# Prepare scripts directory
if os.path.exists(scripts_dir) and os.path.isdir(scripts_dir):
    shutil.rmtree(scripts_dir)
    print("Deleted scripts directory.")

os.mkdir(scripts_dir)
print("Created scripts directory.")

# Download main HTML file
html_file_path = f"{scripts_dir}/evoworld.html"
urllib.request.urlretrieve(main_url, html_file_path)

# Download and (if needed) deobfuscate scripts
timestamp = int(time.time())

for script in scripts + raw_scripts:
    filename = f"{script}.js"
    print(f"Downloading {filename}...")
    
    url = f"{cdn_url}{filename}?{timestamp}"
    file_path = f"{scripts_dir}/{filename}"
    urllib.request.urlretrieve(url, file_path)

    if script in raw_scripts:
        continue

    print(f"Deobfuscating {filename}...")
    deobf_file_path = f"{scripts_dir}/de_{filename}"
    cmd = deobf_cmd.format(input_file=file_path, output_file=deobf_file_path)
    subprocess.call(cmd, shell=True)

    os.remove(file_path)
    os.rename(deobf_file_path, file_path)
    

print("Done.")
