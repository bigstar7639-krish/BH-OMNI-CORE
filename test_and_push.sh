#!/bin/bash
cd ~/BH-OMNI-CORE
python3 test_v41_s3.py || { echo "S3 FAIL - NO PUSH"; exit 1; }
python3 test_v13.py > ~/test_v13.log 2>&1 || { echo "V13 FAIL - NO PUSH"; exit 1; }
echo "ALL TESTS PASS - PUSHING"
git add .gitignore omni_chat_v41_s3.py test_v41_s3.py build_350_v13.py omni_350_v13.py test_v13.py report_v13.json REPORT_V13.md manifest_v13.json rollback_v13.sh
git commit -m "auto: tests PASS" || echo "nothing to commit"
git push origin main
