STEP 5 TERMUX - Unzip INSIDE ~/BH-OMNI-CORE
cd ~/BH-OMNI-CORE
unzip -o /sdcard/Download/BH-OMNI-CORE-Step5-Termux.zip
# Add vault_data.json to .gitignore - do NOT commit real vault file!
echo 'vault_data.json' >> .gitignore
echo 'security/vault_data.json' >> .gitignore
python test_phase1_step5.py # Expect 8 PASS
~/push.sh
