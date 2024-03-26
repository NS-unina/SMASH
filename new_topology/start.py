import subprocess
import os
import sys
import time

def main():

    current_directory = os.path.dirname(os.path.abspath(__file__))
    vagrant_lan2_directory = os.path.join(current_directory,"lan1","vagrant","ubuntu")
    docker_lan2_directory = os.path.join(current_directory,"lan1","docker")
    docker_compose_lan2_directory = os.path.join(docker_lan2_directory,"docker-build")
    

    
    # Costruisci il percorso completo dello script
    script1_path = os.path.join(current_directory, 'reset.sh')
    script2_path = os.path.join(current_directory, 'create_net.sh')
    script3_path = os.path.join(current_directory, 'setup.sh')

    script4_path = os.path.join(docker_lan2_directory, 'setup_container.sh')
    script5_path = os.path.join(docker_lan2_directory, 'auth.sh')

    flask_server_path = os.path.join(current_directory, 'lan1', 'app.py')

    
    
    # Chiamata allo script reset.sh
    process1 = subprocess.run(['bash', script1_path], capture_output=True, text=True)
    # Stampa l'output dello script
    print(process1.stdout)

     # Esegui il controllo sul codice di uscita di reset.sh
    if process1.returncode == 0:
        print("Lo script reset.sh è stato eseguito correttamente.")
    else:
        print("Errore durante l'esecuzione dello script reset.sh. Codice di uscita:", process1.returncode)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore

    # Chiamata allo script create_net.sh
    process2 = subprocess.run(['bash', script2_path], capture_output=True, text=True)
    # Stampa l'output dello script
    print(process2.stdout)
     # Esegui il controllo sul codice di uscita di create_net.sh
    if process2.returncode == 0:
        print("Lo script create_net.sh è stato eseguito correttamente.")
    else:
        print("Errore durante l'esecuzione dello script create_net.sh. Codice di uscita:", process2.returncode)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore

    # Chiamata allo script setup.sh
    process3 = subprocess.run(['bash', script3_path], capture_output=True, text=True)

    # Stampa l'output dello script
    print(process3.stdout)
     # Esegui il controllo sul codice di uscita di setup.sh
    if process3.returncode == 0:
        print("Lo script setup.sh è stato eseguito correttamente.")
        
    else:
        print("Errore durante l'esecuzione dello script setup.sh. Codice di uscita:", process3.returncode)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore    

    print("Topologia creata correttamente")
    time.sleep(5)

    
    
      # Avvia il server Flask in background
    print("Avvio del server Flask in background:")
    python_process = subprocess.Popen(['nohup', 'python3', flask_server_path, '&'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Attendere un breve momento per il server Flask per avviarsi
    time.sleep(2)

    # Esegui il controllo sul codice di uscita
    if python_process.returncode is None:
        print("Il server Flask è stato avviato in background.")
    else:
        print("Errore durante l'avvio del server Flask. Codice di uscita: {}".format(python_process.returncode))
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore

    os.chdir(docker_compose_lan2_directory)
    try:
        subprocess.run(['docker','compose', 'up', '-d'], check=True)
        print("Docker compose up completato con successo.")
    except subprocess.CalledProcessError as e:
        print("Errore durante l'esecuzione di Docker compose up:", e)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore


    time.sleep(2)
    os.chdir(docker_lan2_directory)
    # Chiamata allo script setup_container.sh
    subprocess.call(script4_path)
    

    time.sleep(5)
     # Chiamata allo script auth.sh
    process5 = subprocess.run(['bash', script5_path], capture_output=True, text=True)
    # Stampa l'output dello script
    print(process5.stdout)

     # Esegui il controllo sul codice di uscita di setup_container.sh
    if process5.returncode == 0:
        print("Lo script auth.sh è stato eseguito correttamente.")
    else:
        print("Errore durante l'esecuzione dello script auth.sh. Codice di uscita:", process5.returncode)
        sys.exit(1)  # Esci dallo script con codice di uscita 1 in caso di errore    

    

    os.chdir(vagrant_lan2_directory)

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





if __name__ == "__main__":
    main()