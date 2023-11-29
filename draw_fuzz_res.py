import sys
import os

option = int(sys.argv[1])
if option == 0:
	cmd = "cp -r raw_fuzz_vul/* raw_fuzz/"
	os.system(cmd)
elif option == 1:
	cmd = "cp -r raw_fuzz_path/* raw_fuzz/"
	os.system(cmd)
elif option == 2:
	cmd = "cp -r raw_fuzz_speed/* raw_fuzz/"
	os.system(cmd)	

for image_id in [19061, 18627, 16157, 20880]:
# for image_id in [19061, 18627]:
	cmd = "python stat_plot/main.py -c equafl_%d.toml" %image_id
	os.system(cmd)
	if option == 0:
		copy_cmd = "cp  test/out/mjs_overall-edge-time.pdf %d_vul.pdf" %(image_id)
		os.system(copy_cmd)
	elif option == 1:
		copy_cmd = "cp  test/out/mjs_overall-edge-time.pdf %d_path.pdf" %(image_id)
		os.system(copy_cmd)
	elif option == 2:
		copy_cmd = "cp  test/out/mjs_overall-edge-time.pdf %d_speed.pdf" %(image_id)
		os.system(copy_cmd)


