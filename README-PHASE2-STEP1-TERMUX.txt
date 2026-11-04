PHASE 2 STEP 1 TERMUX - Unzip INSIDE ~/BH-OMNI-CORE
cd ~/BH-OMNI-CORE
unzip -o /sdcard/Download/BH-OMNI-CORE-Phase2-Step1-Termux.zip
python test_phase2_step1.py # Expect 8 PASS
~/push.sh
