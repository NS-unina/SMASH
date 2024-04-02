import subprocess
import os
import sys
import time
import libtmux

def run_script_in_a_different_windows(script_path):
   # Esegui il comando tmux per aprire una nuova sessione e eseguire lo script
    terminal_command = f"gnome-terminal -- bash -c 'bash {script_path}; exec bash'"
    try:
        subprocess.run(terminal_command, shell=True)
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione dello script con tmux:", e)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore 


def run_shell_script(script_path):
    process = subprocess.run(['bash', script_path], capture_output=True, text=True)
    print(process.stdout)
    if process.returncode == 0:
        print(f"Lo script {script_path} è stato eseguito correttamente.")
    else:
        print(f"Errore durante l'esecuzione dello script {os.path.basename(script_path)}. Codice di uscita: {process.returncode}")
        sys.exit(1)

def start_flask_server(flask_server_path):
    python_process = subprocess.Popen(['nohup', 'python3', flask_server_path, '&'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2)
    if python_process.returncode is None:
        print("Il server Flask è stato avviato in background.")
    else:
        print(f"Errore durante l'avvio del server Flask. Codice di uscita: {python_process.returncode}")
        sys.exit(1)

def start_docker_compose(docker_compose_directory):
    os.chdir(docker_compose_directory)
    try:
        subprocess.run(['docker','compose', 'up', '-d'], check=True)
        print("Docker compose up completato con successo.")
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione di Docker compose up:", e)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore

def setup_docker_container(docker_directory):
    os.chdir(docker_directory)
     # Chiamata allo script setup_container.sh
    script1_path = os.path.join(docker_directory, 'setup_container.sh')
    script2_path = os.path.join(docker_directory, 'auth.sh')
    run_shell_script(script1_path)
    run_shell_script(script2_path)


def start_vagrant(vagrant_directory):
    os.chdir(vagrant_directory) 
    try:
        subprocess.run(['vagrant', 'destroy', '-f'], check=True)
        print("Vagrant destroy  completato con successo.")
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione di Vagrant destroy:", e)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore
        
    try:
        subprocess.run(['vagrant', 'up'], check=True)
        print("Vagrant up completato con successo.")
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione di Vagrant up:", e)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore



def main():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    vagrant_lan1_directory = os.path.join(current_directory,"lan1","vagrant","ubuntu")
    vagrant_lan2_directory = os.path.join(current_directory,"lan2","vagrant","ubuntu")
    docker_lan1_directory = os.path.join(current_directory,"lan1","docker")
    docker_lan2_directory = os.path.join(current_directory,"lan2","docker")
    docker_compose_lan1_directory = os.path.join(docker_lan1_directory,"docker-build")
    docker_compose_lan2_directory = os.path.join(docker_lan2_directory,"docker-build")
    
    

    
    # Costruisci il percorso completo dello script
    script1_path = os.path.join(current_directory, 'reset.sh')
    script2_path = os.path.join(current_directory, 'create_net.sh')
    script3_path = os.path.join(current_directory, 'setup.sh')

    flask_server_lan1_path = os.path.join(current_directory, 'lan1', 'app.py')
    start_controller_lan1_path = os.path.join(current_directory,'lan1', 'start_controller.sh')
    start_int_host_lan1_path = os.path.join(current_directory, 'lan1','start_int_host.sh')
    start_controller_lan2_path = os.path.join(current_directory,'lan2', 'start_controller.sh')
    start_int_host_lan2_path = os.path.join(current_directory, 'lan2','start_int_host.sh')

    
    # Chiamata allo script reset.sh
    run_shell_script(script1_path)
    # Chiamata allo script create_net.sh
    run_shell_script(script2_path)
    # Chiamata allo script setup.sh
    run_shell_script(script3_path)

    print("Topologia creata correttamente")
    time.sleep(5)
      # Avvia il server Flask in background
    print("Avvio del server Flask LAN1 in background:")
    start_flask_server(flask_server_lan1_path)

    start_docker_compose(docker_compose_lan1_directory)
    time.sleep(2)
    start_docker_compose(docker_compose_lan2_directory)
    time.sleep(7)

    setup_docker_container(docker_lan1_directory)
    time.sleep(4)
    setup_docker_container(docker_lan2_directory)

    time.sleep(5)

    run_script_in_a_different_windows(start_controller_lan1_path)
    run_script_in_a_different_windows(start_int_host_lan1_path)
    run_script_in_a_different_windows(start_controller_lan2_path)
    run_script_in_a_different_windows(start_int_host_lan2_path)
    
    time.sleep(2)
    start_vagrant(vagrant_lan1_directory)
    #start_vagrant(vagrant_lan2_directory)
   




if __name__ == "__main__":
    main()
