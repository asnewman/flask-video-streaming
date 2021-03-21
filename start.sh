 #!/usr/bin/bash
 
 trap ctrl_c INT

function ctrl_c() {
  echo "** Trapped CTRL-C"
}

 source ./venv/bin/activate
 python app.py
